import zarr
import rechunker
import time
import os
from dask.distributed import Client
from dask_jobqueue import LSFCluster

cluster = LSFCluster(cores=1,memory="200GB",project="tidaldrift",walltime="72:00")
time.sleep(5)
print(cluster)

cluster.scale(12)
time.sleep(10)
print(cluster)

client = Client(cluster)
time.sleep(5)
print(client)

for i in range(1,13):

    source_group = zarr.open('/scratch/tidaldrift/hycom_zarr/hycom12-ssh-'+str(i)+'.zarr')
    print(source_group.tree())

    target_chunks = {
        'ssh': {'time': 720 ,'Depth' : 1, 'Y': 1, 'X': 9000},
        'steric_ssh': {'time': 720 ,'Depth' : 1, 'Y': 1, 'X': 9000}, 
        'Longitude': {'Y': 7055, 'X': 9000}, 
        'Latitude': {'Y': 7055, 'X': 9000},     
        'time': None,
        'X': None,
        'Y': None,
    }
    max_mem = '15GB'

    # deleting previous attempts
    print("Warning deleting /scratch/tidaldrift/hycom_zarr/hycom12-ssh-"+str(i)+"-rechunked*.zarr")
    os.system('rm -rf /scratch/tidaldrift/hycom_zarr/hycom12-ssh-'+str(i)+'-rechunked.zarr')
    os.system('rm -rf /scratch/tidaldrift/hycom_zarr/hycom12-ssh-'+str(i)+'-rechunked-tmp.zarr') 

    target_store = '/scratch/tidaldrift/hycom_zarr/hycom12-ssh-'+str(i)+'-rechunked.zarr'
    temp_store = '/scratch/tidaldrift/hycom_zarr/hycom12-ssh-'+str(i)+'-rechunked-tmp.zarr'
    array_plan = rechunker.rechunk(source_group, target_chunks, max_mem, target_store, temp_store=temp_store)

    print('Starting to rechunk zarr '+str(i))

    array_plan.execute()

    print('rechunking ' + str(i) + ' done')
    
    os.system('rm -rf /scratch/tidaldrift/hycom_zarr/hycom12-ssh-'+str(i)+'-rechunked-tmp.zarr') 

exit()



