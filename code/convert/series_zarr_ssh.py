import dask
import xarray as xr
import sys

# read list of files and make a list
datadir = '/projectnb/msldrift/hycom/'
filelist = open(datadir+'ssh_filelist','r')
contents = filelist.readlines()
filelist.close()
files = []
for i in contents:
    files.append(i.rstrip('\n'))

# list of indices
ind = []
for k in range(0,11):
    ind.append(range(k*720,720*(k+1)))
ind.append(range(720*11,8759))

# read files
timeseries_dir = '/scratch/tidaldrift/hycom_zarr/'
for k in range(1,12):
    sys.stdout.write('working on zarr shh '+str(k+1))
    ind_tmp = [files[i] for i in ind[k]]
    print('opening model files')
    model = xr.open_mfdataset([f'/projectnb/msldrift/hycom/ssh/{i}' for i in ind_tmp]).drop(['nonsteric_ssh'])
    model = model.rename({'MT':'time'})
    print('opening zarr')
    model.to_zarr(timeseries_dir + 'hycom12-ssh-'+str(k+1)+'.zarr')
    sys.stdout.write('ssh zarr ' + str(k+1) + ' done')

exit()
