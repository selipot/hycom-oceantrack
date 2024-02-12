# hycom-oceantrack

This repository accompanies [**HYCOM OceanTrack:  Integrated HYCOM Eulerian Fields and Lagrangian Trajectories Dataset**](https://registry.opendata.aws/hycom-global-drifters/index.html) which is available through the AWS Open Data program. 

The animation below depicts the trajectories of nearly 588,000 particles advected for 60 days at 15 m depth within the hourly velocity field of a 1/25 degree HYCOM simulation. The particles are colored by their longitude (with a repeated colorscale) at the middle time of their 60-day trajectories. As such, during the first half of the animation you can visualize the longitudes where the particles will be at day 30. During the second half, you can visualize the longitudes where the particles used to be.

![GIF File](tutorials/traj-robinson-0-60-hsv.gif)

This repository contains:

- `data-bucket-description.md` : A description, or *README* , file of the organization and structure of the dataset in the AWS S3 bucket [`hycom-global-drifters`]().

- `tutorials/` : A collection of notebook tutorials to illustrate possible uses for the dataset.

- `code/`: A collection of python scripts that were used to create this cloud-optimized dataset. For reference only.

- `metadata-file.yaml` : The required YAML file for the [AWS Open Data Program](https://aws.amazon.com/opendata/).
