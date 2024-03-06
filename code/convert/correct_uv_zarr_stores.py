# code to correct missing values of zarr stores
import xarray as xr
import zarr
import numpy as np
import time
from dask.distributed import Client
from dask_jobqueue import LSFCluster

cluster = LSFCluster(cores=1,memory="200GB",project="tidaldrift",walltime="72:00")
time.sleep(5)
cluster.scale(10)
time.sleep(10)
client = Client(cluster)
time.sleep(5)

datadir = '/scratch/tidaldrift/hycom_zarr/'
outdir = '/projectnb/msldrift/hycom/zstore/'

for i in range(1,13):

    # consolidate the zarr store
    zarr.consolidate_metadata(datadir + 'hycom12-' + str(i) + '-rechunked.zarr')

    dsr = xr.open_zarr(datadir + 'hycom12-'+str(i)+'-rechunked.zarr',consolidated=True)

    # for some reasons Latitude/Longitude are Data variables; remove those because the masking operation below messes with these
    dsr_masked = dsr.drop_vars(['Latitude','Longitude'])

    # mask the values based on min max of u; should work
    dsr_masked = dsr_masked.where(np.logical_and(dsr_masked.u>=dsr.u.valid_range[0],dsr_masked.u<=dsr.u.valid_range[1]))

    # put back Latitude,Longitude as coordinates
    dsr_masked = dsr_masked.assign(Latitude=dsr["Latitude"],Longitude=dsr["Longitude"])

    # rewrite/append the zarr store
    dsr_masked.to_zarr(outdir + 'hycom12-' + str(i) + '-rechunked-corr.zarr',mode="w")

    print('Done correcting zarr' + str(i))

    dsr_masked.close()
    dsr.close()
