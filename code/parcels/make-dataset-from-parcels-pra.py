# code to create 60-day long Lagrangian datasets from parcels outputs, calculate velocities, estimate grounding
import xarray as xr
import numpy as np
import zarr
import dask
from datetime import datetime, timedelta
from clouddrift.kinematics import velocity_from_position
from clouddrift.sphere import recast_lon180
import sys

# define the step from input
j = int(sys.argv[1])

file1 = '/projectnb/msldrift/pra-drifters/global_hycom_step_'+str(j)+'_forward.zarr'
file2 = '/projectnb/msldrift/pra-drifters/global_hycom_step_'+str(j)+'_backward.zarr'
ds1 = xr.open_zarr(file1, decode_times=False)
ds2 = xr.open_zarr(file2, decode_times=False)
print("Opening "+file1)
print("Opening "+file2)

# select common trajectories for the surface (0m)
dum = np.load('/home/selipot/pra-drifters/py/id_lists.npz')
list_2d_0m = dum["list_2d_0m"]

# select the common trajectories
ds1 = ds1.sel(trajectory=list_2d_0m)
ds2 = ds2.sel(trajectory=list_2d_0m)

# create the datetime vector
dum = np.ravel(np.concatenate((np.flip(ds2.time[0:1,:].data,axis=1),ds1.time[0:1,1:-1].data),axis=1))
dum = np.array(dum) # need to convert dask array to numpy array to use the following
start_date = datetime(2014, 1, 1, 1, 0, 0)
datetime_vector = [start_date + timedelta(seconds=i) for i in dum]

# Assemble the 60-day dataset
chunks = {0:'auto',1:-1} # that is, do not chunk along the obs dimension
coords = {}
coords["obs"] = (["obs"],np.array(np.arange(0,1440),dtype='int32'))
coords["id"] = (["traj"],ds1.trajectory.data)
data_vars = {}
data_vars["lat"] = (["traj","obs"],np.concatenate((np.flip(ds2.lat.data,axis=1),ds1.lat[:,1:-1].data),axis=1).rechunk(chunks=chunks))
data_vars["lon"] = (["traj","obs"],np.concatenate((np.flip(ds2.lon.data,axis=1),ds1.lon[:,1:-1].data),axis=1).rechunk(chunks=chunks))
data_vars["depth"] = (["traj","obs"],np.concatenate((np.flip(ds2.DPTH.data,axis=1),ds1.DPTH[:,1:-1].data),axis=1).rechunk(chunks=chunks))
data_vars["ssh"] = (["traj","obs"],np.concatenate((np.flip(ds2.SSH.data,axis=1),ds1.SSH[:,1:-1].data),axis=1).rechunk(chunks=chunks))
data_vars["steric_ssh"] = (["traj","obs"],np.concatenate((np.flip(ds2.SSSH.data,axis=1),ds1.SSSH[:,1:-1].data),axis=1).rechunk(chunks=chunks))
data_vars["time"] = (["traj","obs"],dask.array.from_array(np.tile(datetime_vector,(ds1["trajectory"].size,1)),chunks=data_vars["lat"][1].chunksize))
attrs = {}
attrs["parcels_mesh"] = ds1.attrs['parcels_mesh']
attrs["parcels_versions"] = ds1.attrs['parcels_version']
attrs["feature_type"] = ds1.attrs['feature_type']

ds = xr.Dataset(coords=coords,data_vars=data_vars,attrs=attrs)

# calculate forward velocities; time is in seconds
u,v = xr.apply_ufunc(
        velocity_from_position,  # first the function
        ds.lon.load(),
        ds.lat.load(),
        ds.time.load(),
        input_core_dims=[["obs"],["obs"], ["obs"]],
        output_core_dims=[["obs"], ["obs"]],
        vectorize=True,
)

# make sure u and v are chunked
u = u.chunk(chunks=data_vars["lat"][1].chunksize)
v = v.chunk(chunks=data_vars["lat"][1].chunksize)

# convert velocities to m/s instead of meter per ns
ds["ve"] = 1e9*u.astype('float32')
ds["vn"] = 1e9*v.astype('float32')

# recast longitudes in [180,180)
ds["lon"]= xr.DataArray(recast_lon180(ds["lon"].data), dims=ds["lon"].dims)

# assign attributes
# no need to assign attributes for time variable which is taken care of by datetime and zarr
# when loading the data as an xarray dataset

ds['lat'].attrs['standard_name'] = 'latitude'
ds['lat'].attrs['units'] = 'degrees_north'

ds['lon'].attrs['standard_name'] = 'longitude'
ds['lon'].attrs['units'] = 'degrees_east'

ds['depth'].attrs['standard_name'] = 'depth_below_geoid'
ds['depth'].attrs['units'] = 'm'

ds['ssh'].attrs['standard_name'] = 'sea_surface_height_above_geoid'
ds['ssh'].attrs['units'] = 'm'

ds['steric_ssh'].attrs['standard_name'] = 'steric_change_in_sea_surface_height'
ds['steric_ssh'].attrs['units'] = 'm'

ds['ve'].attrs['standard_name'] = 'eastward_sea_water_velocity'
ds['ve'].attrs['units'] = 'm s-1'

ds['vn'].attrs['standard_name'] = 'northward_sea_water_velocity'
ds['vn'].attrs['units'] = 'm s-1'

# calculate speed
s = ((ds["ve"]**2+ds["vn"]**2)**0.5).load()

# Estimate grounding

# Define a threshold and a period length
ts = 0.003
days = 1

# create a mask as large as the array of data
mask = np.full(np.shape(s), False, dtype=bool)

for i in range(s.shape[0]):
    # Find the indices where the array is less than the threshold
    indices = np.where(s[i,:] < ts)[0]
    if indices.size != 0:
        # Find the start indices of consecutive sequences
        start_indices = np.where(np.diff(indices, prepend=indices[0]-2) != 1)[0]
        # Find the end indices of consecutive sequences
        end_indices = np.roll(start_indices, -1) - 1
        end_indices[-1] = len(indices) - 1
        # Extract the consecutive sequences if they end before obs 720
        # and if they start after 720
        sequences_start = [indices[start:end+1] for start, end in zip(start_indices, end_indices) if indices[end] < 720]
        sequences_end = [indices[start:end+1] for start, end in zip(start_indices, end_indices) if indices[start] > 720]

        cutoff_obs_pre = np.array([np.nan])
        cutoff_obs_post = np.array([np.nan])

        # Iterate over the start sequences in reverse order to find the pre cut off
        for seq in reversed(sequences_start):
            # Check if the length of the sequence is greater than 24
            if len(seq) > 24*days:
                # get the last element of the sequence
                cutoff_obs_pre = seq[-1]
                break

        # Iterate over the end sequences in order to find the post cut off
        for seq in sequences_end:
            # Check if the length of the sequence is greater than 24
            if len(seq) > 24*days:
                # get the last element of the sequence
                cutoff_obs_post = seq[0]
                break
        if ~np.isnan(cutoff_obs_pre):
            mask[i,:cutoff_obs_pre] = True
        if ~np.isnan(cutoff_obs_post):
            mask[i,cutoff_obs_post:] = True
        # now mask is True where there is grounding/beach

ds["grounding"] = (["traj","obs"],mask)
ds["grounding"].attrs['comment'] = 'True if particle is estimated grounded'

# force rechunk seems needed:
ds = ds.chunk(chunks={'traj':'auto','obs':-1})
# hard force the size of the chunk for time variable: does not work so I am giving up on this
# ds["time"] = ds["time"].chunk(chunks={'traj':'auto','obs':1440})

ds.to_zarr('/projectnb/msldrift/pra-drifters/aws/global_hycom_0m_step_'+str(j)+'.zarr',mode="w",safe_chunks=False)