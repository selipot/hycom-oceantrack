## File List

Here we provide samples of python scripts that were used to generate the datasets found in [**HYCOM OceanTrack:  Integrated HYCOM Eulerian Fields and Lagrangian Trajectories Dataset**](https://registry.opendata.aws/hycom-global-drifters/index.html) which is available through the AWS Open Data program. 

In the `convert/` directory, we provide example python scripts that were used to convert individual velocity and Sea Surface Height (SSH) NetCDF files into zarr archives thanks to the [rechunker](https://github.com/pangeo-data/rechunker) Python package. This library was written following the epic community [discussion](https://discourse.pangeo.io/t/best-practices-to-go-from-1000s-of-netcdf-files-to-analyses-on-a-hpc-cluster/588) that occured on [Pangeo](https://pangeo.io).

We also provide in `parcels/` some [Ocean Parcels](https://oceanparcels.org) Python scripts and LSF job script that were used to generate the simulated trajectories.

- `README.md`: this file.

- `convert/series_zarr_uv.py`: Scripts to create 11 zarr archives from the original 8759 individual velocity NetCDF files.

- `convert/series_zarr_ssh.py`: Scripts to create 11 zarr archives from the original 8759 individual SSH NetCDF files.

- `convert/rechunk_[uv,ssh]_series.py`: Scripts to re-chunk the zarr stores. 

- `convert/correct_[uv,ssh]_zarr_stores.py`: Scripts to correct the outputs from the rechunker. 

- `parcels/global_hycom_15m_step_i.py` : Python script used with the Ocean Parcels software to advect particles in the HYCOM velocity fields. Note that this script uses the HYCOM fields saved as NetCDF files, not as zarr stores such as the ones found in [**HYCOM OceanTrack**](https://registry.opendata.aws/hycom-global-drifters/index.html). The same script was used to advect particles *backward* in time by simply negating the `dt` variable in this code.

- `parcels/select-particles-for-saving.py` : Python script used to select the particles ids which will can be found in all sets at each depth.

- `parcels/make-ragged-from-parcels-pra.py` : Python script used to 
    - assemble foward and backward simulations into a single zarr file,
    - calculate Lagrangian velocities using [clouddrift](https://github.com/Cloud-Drift/clouddrift),
    - create the data mask for estimated grounding (or beaching) of the particles.

    This script was used to assemble the 0 m trajectories. A similar script was used to assemble the 15 m trajectories. 
