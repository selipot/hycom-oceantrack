[![DOI](https://zenodo.org/badge/749082395.svg)](https://zenodo.org/doi/10.5281/zenodo.11193405)

# hycom-oceantrack

This repository accompanies [**HYCOM OceanTrack:  Integrated HYCOM Eulerian Fields and Lagrangian Trajectories Dataset**](https://registry.opendata.aws/hycom-global-drifters/index.html) which is available through the AWS Open Data program. 

The animation below depicts the trajectories of nearly 588,000 particles advected for 60 days at 15 m depth within the hourly velocity field of a 1/25 degree HYCOM simulation. The coloring of the particles is determined by their longitude, using a repeating color scale, at the halfway point of their 60-day journeys. This means that in the first half of the animation, you are able to see the longitudinal positions the particles will reach by day 30. In the latter half, you are able to see the longitudinal positions where the particles were at day 30.

![GIF File](tutorials/traj-robinson-0-60-hsv.gif)

This repository contains:

- `data-bucket-description.md` : A description, or *README* , file of the organization and structure of the dataset in the AWS S3 bucket [`hycom-global-drifters`]().

- `tutorials/` : A collection of notebook tutorials to illustrate possible uses for the dataset.

- `code/`: A collection of python scripts that were used to create this cloud-optimized dataset. For reference only.

- `metadata-file.yaml` : The required YAML file for the [AWS Open Data Program](https://aws.amazon.com/opendata/).
