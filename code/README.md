## File List

Here we provide samples of python scripts that were used to generate the datasets found in [**HYCOM OceanTrack:  Integrated HYCOM Eulerian Fields and Lagrangian Trajectories Dataset**](https://registry.opendata.aws/hycom-global-drifters/index.html) which is available through the AWS Open Data program. 

We provide in the `convert/` directory example python scripts that were used to convert the 8759 individual velocity files and the 8759 individual ssh files into zarr archives thanks to the [rechunker](https://github.com/pangeo-data/rechunker) python package. This library was written following the epic community [discussion](https://discourse.pangeo.io/t/best-practices-to-go-from-1000s-of-netcdf-files-to-analyses-on-a-hpc-cluster/588) that occured on [Pangeo](https://pangeo.io).

We also provide in `parcels/` some Ocean Parcels python script and LSF job script that were used to generate the simulated trajectories.

- `README.md`: this file.

- `convert/series_zarr_uv.py`:
- `convert/series_zarr_ssh.py`:

- `parcels/make-ragged-from-parcels-pra.py` : Python script used to 
    - assemble foward and backward simulations into a single zarr file,
    - calculate Lagrangian velocities using [clouddrift](https://github.com/Cloud-Drift/clouddrift),
    - create the data mask for estimated grounding (or beaching) of the particles.
 
