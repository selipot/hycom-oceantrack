# code to create common index of particles ids
import xarray as xr
import zarr
import numpy as np

# find common trajectories for each step forward
# 0 m

i = 1
file = '/projectnb/msldrift/pra-drifters/global_hycom_step_'+str(i)+'_forward.zarr'
ds = xr.open_dataset(file, decode_times=False,engine='zarr')
list_f_0m = ds.trajectory.to_numpy()
ds.close()
for i in range(2,12):
    file = '/projectnb/msldrift/pra-drifters/global_hycom_step_'+str(i)+'_forward.zarr'
    ds = xr.open_dataset(file, decode_times=False,engine='zarr')
    list_f_0m = np.intersect1d(list_f_0m,ds.trajectory.to_numpy())
    ds.close()

# 15 m    

i = 1
file = '/projectnb/msldrift/pra-drifters/global_hycom_15m_step_'+str(i)+'_forward.zarr'
ds = xr.open_dataset(file, decode_times=False,engine='zarr')
list_f_15m = ds.trajectory.to_numpy()
ds.close()
for i in range(2,12):
    file = '/projectnb/msldrift/pra-drifters/global_hycom_15m_step_'+str(i)+'_forward.zarr'
    ds = xr.open_dataset(file, decode_times=False,engine='zarr')
    list_f_15m = np.intersect1d(list_f_15m,ds.trajectory.to_numpy())
    ds.close()

# find common trajectories for each step backward
# 0 m

i = 1
file = '/projectnb/msldrift/pra-drifters/global_hycom_step_'+str(i)+'_backward.zarr'
ds = xr.open_dataset(file, decode_times=False,engine='zarr')
list_b_0m = ds.trajectory.to_numpy()
ds.close()
for i in range(2,12):
    file = '/projectnb/msldrift/pra-drifters/global_hycom_step_'+str(i)+'_backward.zarr'
    ds = xr.open_dataset(file, decode_times=False,engine='zarr')
    list_b_0m = np.intersect1d(list_b_0m,ds.trajectory.to_numpy())
    ds.close()

# 15 m

i = 1
file = '/projectnb/msldrift/pra-drifters/global_hycom_15m_step_'+str(i)+'_backward.zarr'
ds = xr.open_dataset(file, decode_times=False,engine='zarr')
list_b_15m = ds.trajectory.to_numpy()
ds.close()
for i in range(2,12):
    file = '/projectnb/msldrift/pra-drifters/global_hycom_15m_step_'+str(i)+'_backward.zarr'
    ds = xr.open_dataset(file, decode_times=False,engine='zarr')
    list_b_15m = np.intersect1d(list_b_15m,ds.trajectory.to_numpy())
    ds.close()

# list for two directions at 0 m and 15 m and intersection of 0m and 15m
list_2d_0m = np.intersect1d(list_f_0m,list_b_0m)
list_2d_15m = np.intersect1d(list_f_15m,list_b_15m)
list_2d = np.intersect1d(list_2d_0m,list_2d_15m)

np.savez('/home/selipot/pra-drifters/py/id_lists',list_2d=list_2d,list_2d_0m=list_2d_0m,list_2d_15m=list_2d_15m)
