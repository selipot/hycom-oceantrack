## Eulerian and Lagrangian near-surface velocity and sea surface height from one year of the global HYbrid Coordinate Ocean Model (HYCOM)

This is a description of the dataset contained in the AWS S3 bucket "hycom-25-global" available at [https://]()

This bucket contains two distinct and related datasets:

1. The first dataset in `hycom-25-global/eulerian/` consists of Eulerian (fixed grid) field variables which were generated from a 1-year simulation of the HYCOM model as described in [Arbic et al. 2022](https://dx.doi.org/10.1029/2022JC018551). The version of the dataset used for this publication can be accessed via the OSiRIS infrastructure of the University of Michigan-Ann Harbor. Details for accessing OSiRIS can be obtained by contacting Dr. Brian K. Arbic (arbic@umich.edu).
The S3 bucket described here provides an alternative distribution of the same data (except model bottom velocity data) but organized differently as cloud-optimized [zarr directory stores](https://zarr.readthedocs.io/en/stable/).

2. The second dataset in `hycom-25-global/lagrangian/` consists of Lagrangian particle trajectories advected in the velocity fields of the model at two depth (0 m and 15 m) and are not available elsewhere.

A manuscript providing further details on how the Lagrangian dataset was produced with the [Ocean Parcels software](https://oceanparcels.org) is in preparation. Once submitted this manuscript will be referenced here. In the meantime, for further information not available in this README file, please email Dr. Shane Elipot at selipot@miami.edu

#### 1. `hycom-25-global/eulerian/`

The data correspond to field variables at 8759 hourly time steps from 2014-01-01T01:00:00 to 2014-12-31T23:00:00. These data are split in 12 zarr stores containing 720 hourly steps or 60 days of data, for stores number 1 to 11, and a 12<sup>th</sup> store with 839 steps to complete the year. The data are further split between velocity data and sea surface height data for a total of 24 stores. The date range and steps of each of the two sets of 12 stores are:

| Stores | First Step Datetime              | Last Step Datetime                | Number of Steps | Indices (1-based)     |
|-----|-------------------------|-------------------------|-------|----------|
| 1   | 2014-01-01T01:00:00     | 2014-01-31T01:00:00     | 720   | 1 to 720 |
| 2   | 2014-01-31T01:00:00     | 2014-03-02T01:00:00     | 720   | 721 to 1440 |
| 3   | 2014-03-02T01:00:00     | 2014-04-01T01:00:00     | 720   | 1441 to 2160 |
| 4   | 2014-04-01T01:00:00     | 2014-05-01T01:00:00     | 720   | 2161 to 2880 |
| 5   | 2014-05-01T01:00:00     | 2014-05-31T01:00:00     | 720   | 2881 to 3600 |
| 6   | 2014-05-31T01:00:00     | 2014-06-30T01:00:00     | 720   | 3601 to 4320 |
| 7   | 2014-06-30T01:00:00     | 2014-07-30T01:00:00     | 720   | 4321 to 5040 |
| 8   | 2014-07-30T01:00:00     | 2014-08-29T01:00:00     | 720   | 5041 to 5760 |
| 9   | 2014-08-29T01:00:00     | 2014-09-28T01:00:00     | 720   | 5761 to 6480 |
| 10  | 2014-09-28T01:00:00     | 2014-10-28T01:00:00     | 720   | 6481 to 7200 |
| 11  | 2014-10-28T01:00:00     | 2014-11-27T01:00:00     | 720   | 7201 to 7920 |
| 12  | 2014-11-27T01:00:00     | 2014-12-31T23:00:00     | 839   | 7921 to 8759 |

Velocity data are contained in zarr stores `hycom12-x-rechunked-corr.zarr` with `x` from 1 to 12 and organized as follows (in the [xarray Dataset](https://docs.xarray.dev/en/stable/generated/xarray.Dataset.html) sense).

- The *dimensions* and their lengths are:

    - **Depth**: 2,
    - **Y**: 7055,
    - **X**: 9000,
    - **time**: 720 or 839.

**X** and **Y** are the non-regular tri-pole grid nodes on the spherical Earth used by HYCOM (see [Arbic et al. 2022](https://dx.doi.org/10.1029/2022JC018551)).

- The *coordinates* with dimensions of the same names and their units are:
    - **Depth** (Depth) : depth 0.0 or 15.0, m,
    - **X** (X), 1 to 9000, no unit,
    - **Y** (Y), 1 to 7055, no unit,
    - **time** (time): 0 to 719 (or 838), hours since first step.

Please note that unless automatically decoded by a software method (such as reading the zarr store with python [Xarray](https://docs.xarray.dev/en/stable/)), the units of **time** are hours since the first step of the set/store.

- The *Data variables* and their dimensions are:
    - **Latitude** (Y, X) : degree north,
    - **Longitude** (Y, X) : degree east,
    - **u** (time, Depth, Y, X): eastward_sea_water_velocity, m s-1,
    - **v** (time, Depth, Y, X): northward_sea_water_velocity, m s-1.

The [zarr chunks](https://zarr.readthedocs.io/en/stable/tutorial.html#chunk-optimizations) for the core variables **u** and **v** are (720, 1, 1, 9000) such as the data are optimized for analysis along the time dimension (and X dimension).

Sea surface height data are contained in stores `hycom12-ssh-x-rechunked-corr.zarr` with `x` from 1 to 12. These stores have the same dimensions and coordinates as the velocity data stores except for the coordinate and dimension **Depth** (Depth). Their *Data variables* are:
- **ssh** (time, Y, X): sea surface height, m,
- **steric_ssh** (time, Y, X): steric change in sea surface height, m.

The ssh is the sum of the steric ssh and the non steric ssh which can be calculated as nonsteric_ssh = ssh - steric_ssh.

#### 2. `hycom-25-global/lagrangian/`

The Lagrangian dataset is constituted of 22 [zarr stores](https://zarr.readthedocs.io/en/stable/). There are 11 stores for numerical particles advected at the surface of the model (0 m) in stores `global_hycom_0m_step_x.zarr` with `x` from 1 to 11, and 11 stores for numerical particles advected at 15 m depth in stores `global_hycom_15m_step_x.zarr` with `x` from 1 to 11. Each zarr store contains either 593,292 (0 m) or 587,225 (15 m) particle trajectories at 1440 hourly time steps or 60 days.

The first (step 1), middle (step 720), and end (step 1440) datetimes for the two 11 sets of trajectories are:

| Set/Store | First Step            | Middle Step           | End Step              |
|---|-----------------------|-----------------------|-----------------------|
|1  | 2014-01-01 01:00:00   | 2014-01-31 01:00:00   | 2014-03-02 00:00:00   |
|2  | 2014-01-31 01:00:00   | 2014-03-02 01:00:00   | 2014-04-01 00:00:00   |
|3  | 2014-03-02 01:00:00   | 2014-04-01 01:00:00   | 2014-05-01 00:00:00   |
| 4 | 2014-04-01 01:00:00   | 2014-05-01 01:00:00   | 2014-05-31 00:00:00   |
| 5 | 2014-05-01 01:00:00   | 2014-05-31 01:00:00   | 2014-06-30 00:00:00   |
| 6 | 2014-05-31 01:00:00   | 2014-06-30 01:00:00   | 2014-07-30 00:00:00   |
| 7 | 2014-06-30 01:00:00   | 2014-07-30 01:00:00   | 2014-08-29 00:00:00   |
| 8 | 2014-07-30 01:00:00   | 2014-08-29 01:00:00   | 2014-09-28 00:00:00   |
| 9 | 2014-08-29 01:00:00   | 2014-09-28 01:00:00   | 2014-10-28 00:00:00   |
| 10 | 2014-09-28 01:00:00   | 2014-10-28 01:00:00   | 2014-11-27 00:00:00   |
| 11 | 2014-10-28 01:00:00   | 2014-11-27 01:00:00   | 2014-12-27 00:00:00   |

For all Lagrangian sets/stores:

- The *Dimensions* are:

    - **traj** (593292 or 587225),
    - **obs** (1440).

- The *Coordinates* and their dimensions are:
    - **id** (traj),
    - **obs** (obs), 0 to 1439.

- The *Data Variables* and their dimensions and units are: 
    - **depth** (traj,obs): model depth, m,
    - **grounding** (traj,obs): a boolean variable which is *True* if the particle is estimated grounded, 
    - **lat** (traj,obs): latitude, degree north 
    - **lon** (traj,obs): longitude, degree east 
    - **ssh** (traj,obs): sea surface height, m,
    - **steric_ssh** (traj,obs): steric change in sea surface height, m,
    - **time** (traj,obs): hours since first step of each set, 
    - **ve** (traj,obs): eastward particle velocity, m s-1
    - **vn** (traj,obs): northward particle velocity, m s-1.


Note that grounding of particles may occur both at the beginnings and at the ends of trajectories because these trajectories were generated by advecting particle forward in time and backward in time from the middle time step.

The zarr chunks for the data variables are *(23301, 1440)* except for **grounding** *(93206, 1440)* and **time** *(9176, 45)*. As such, the data are generally optimized for analysis along the **obs** dimension, that is along trajectories (or equivalently time).

The coordinate variable **id** is a tagging number assigned to a particle by the [Ocean Parcels software](https://oceanparcels.org). The same id numbers are all found in each of the 11 sets at 0 m, and the same is true for the 11 sets at 15 m. There are 587,225 common ids between a set at 0 m and a set at 15 m. Across all sets, a unique id is associated with a particle located at a given geographical position at middle time step 720. As an example, all particles with id 105763 are located at *(lon,lat) = (-134.5, -64.75)* at time step *720* of their respective 1440-step trajectories. This has been achieved by assembling trajectories of particle advected forward in time and backward in time from a common time, starting from a common location on a regular 1/4 degree longitude-latitude grid.
