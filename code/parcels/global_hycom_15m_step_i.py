# global experiment, 1/4 degree, step one from 31-Jan-2014 01:00:00, sampling SSH, steric SSH, Depth
# 15 m depth advection

# parcels
from parcels import VectorField, Field, SummedField, FieldSet, ParticleSet, Variable, ScipyParticle, JITParticle, AdvectionRK4, plotTrajectoriesFile, ParcelsRandom, ErrorCode

# open data to validate
from netCDF4 import Dataset
from glob import glob

# others
import numpy as np
from datetime import timedelta, datetime
import xarray as xr
import os
import tempfile
print(tempfile.gettempdir())
import sys

# define the case
i = int(sys.argv[1])

# define all fieldsets
# file locations
dirin = '/projectnb/msldrift/hycom/'
uvfiles = dirin + 'uv/102_archv.2014_*_*_uv_0+15m.nc'
sshfiles = dirin + 'ssh/102_archs.2014_*_*_ssh_0m.nc'
bathyfile = dirin + '102_archv.bathy.nc'

#os.environ['TMPFILE'] = '/scratch/tidaldrift/'
tempfile.tempdir = '/scratch/tidaldrift/'
print(tempfile.gettempdir())

# create dictionaries 
filenames1 = {'U': uvfiles,
             'V': uvfiles}
filenames2 = {'SSH': sshfiles,'SSSH': sshfiles}
filenames3 = {'DPTH': bathyfile}

# map u, v, to the names in the velocity files
variables1 = {'U': 'u',
             'V': 'v'}
variables2 = {'SSH' : 'ssh',
              'SSSH' : 'steric_ssh'}
variables3 = {'DPTH' : 'bathymetry'}

# map lon, lat, depth, time to the names in the velocity files
dimensions1 = {'depth':'Depth',
              'lon': 'Longitude',
              'lat': 'Latitude'
              }
dimensions2 = {'lon': 'Longitude',
              'lat': 'Latitude'
              }

# select one layer (0 for surface, 1 for 15m deep)
indices = {'depth': [1]}

# recreate the time dimension
timestamps = np.expand_dims(np.arange('2014-01-01T01', '2015-01-01T00', dtype='datetime64[h]'),axis=1)

print(uvfiles)
print(sshfiles)
print(bathyfile)
print(len(timestamps))

# define the fieldset from files
fieldset = FieldSet.from_netcdf(filenames1, variables1, dimensions1, indices, mesh='spherical',allow_time_extrapolation=False,deferred_load=True,timestamps=timestamps)

# create an extra field for SSH
sshfieldset = FieldSet.from_netcdf(filenames2,variables2,dimensions2,mesh='spherical',allow_time_extrapolation=False,deferred_load=True,timestamps=timestamps)

# create extra field for bathymetry
bathyfieldset = FieldSet.from_netcdf(filenames3,variables3,dimensions2,mesh='spherical',allow_time_extrapolation=True,deferred_load=True,timestamps=timestamps[0:1])

fieldset.add_field(sshfieldset.SSH)
fieldset.add_field(sshfieldset.SSSH)
fieldset.add_field(bathyfieldset.DPTH)

# add periodic condition
fieldset.add_periodic_halo(zonal=True)

# create particle set: quarter degree

t0 = i*30*24*60*60 # time of the release [s]
x = np.arange(-180,180,.25)
y = np.arange(-70,75.25,.25)
plon,plat = np.meshgrid(x,y, indexing='ij')
plon = plon.flatten()
plat = plat.flatten()
ptime = np.ones(len(plon)) * timedelta(seconds=int(t0)).total_seconds()

# initialization
pset = ParticleSet.from_list(fieldset=fieldset,pclass=JITParticle,lon=[],lat=[],time=[])

class SampleParticleInitZero(JITParticle):            # Define a new particle class
    ssh = Variable('SSH', initial=0)                  # Variable 'SSH' initially zero
    sssh = Variable('SSSH', initial=0)                  # Variable 'SSSH' initially zero
    dpth = Variable('DPTH', initial=0)                  # Variable 'DPTH' initially zero    
    
# initialization for sampling I think
pset = ParticleSet(fieldset=fieldset, pclass=SampleParticleInitZero,lon=plon,lat=plat,time=ptime)

# define the sampling kernel
def Sample(particle, fieldset, time):
         particle.SSH = fieldset.SSH[time, particle.depth, particle.lat, particle.lon]
         particle.SSSH = fieldset.SSSH[time, particle.depth, particle.lat, particle.lon]
         particle.DPTH = fieldset.DPTH[time, particle.depth, particle.lat, particle.lon]

sample_kernel = pset.Kernel(Sample)    # Casting the Sample function to a kernel

# function to delete particle when out of bounds
def DeleteParticle(particle, fieldset, time):
    particle.delete()

# remove particle where there is no velocity (on land?); suggested by Philippe Miron
def RemoveOnLand(particle, fieldset, time):
    u, v = fieldset.UV[time, particle.depth, particle.lat, particle.lon]
    if math.fabs(u) < 1e-12:
        particle.delete()
        
# execute once to remove particles on land
pset.execute(RemoveOnLand, dt=0, recovery={ErrorCode.ErrorOutOfBounds: DeleteParticle})

# execute once for initial sampling
pset.execute(sample_kernel, dt=0)

# advection parameters
runtime = timedelta(days=30)           # advection integration time
dt = timedelta(minutes=20)                       # advection timestep
outputdt = timedelta(hours=1)                    # output frequency
outfile = '/projectnb/msldrift/pra-drifters/global_hycom_15m_step_'+str(i)+'_forward' # output file name

# output files for the trajectories
output_file = pset.ParticleFile(name=outfile, outputdt=outputdt)

# define the kernel
kernel1 = pset.Kernel(AdvectionRK4)

# run the whole thing
pset.execute(kernel1 + sample_kernel,          # the kernels (define how particles move)
     runtime=runtime,                         # the total length of the run
     dt=dt,                                   # the timestep of the kernel
     recovery={ErrorCode.ErrorOutOfBounds: DeleteParticle},
     output_file=output_file)
