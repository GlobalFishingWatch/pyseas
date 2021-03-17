# PySeas

A library to help make GFW style map plots in Python.

In the future this will likely be extended to other types of GFW plots.

*Please note all interfaces are still in flux and not guaranteed to be stable!*

## To Do

* Bulletproof Scalebar

## Installation

## Pyseas

#### Mac

Some of the dependencies are a headache to install via `pip`, so the recommended approach
is to install using Conda. The following recipe works currently:

    conda install -c conda-forge cartopy geopandas numpy matplotlib pandas h3-py \
                     jupyter jupytext scikit-image cmocean gdal netcdf4 pandas-gbq

Then `cd` to the directory that PySeas was cloned into, typically `pyseas`, and run:

    pip install -e .

This install PySeas into whatever Conda environment is active at the time it is run.
We use the `-e` option so that EEZ data and logo data can be easily installed afterwards
as described below.

### Installing EEZ data

* Download the World EEZ v11 GeoPackage from https://www.marineregions.org/downloads.php
* Unpack the zip file 
* Copy `eez_boundaries_v11.gpkg` and `eez_v11.gpkg` to `untracked/data/`

### Installing the Roboto Font

* Download Roboto from https://fonts.google.com/specimen/Roboto?selection.family=Roboto
* On OsX install using FontBook, On Linux???
* You may need to update the font-cache, it worked for me without this, but see https://scentellegher.github.io/visualization/2018/05/02/custom-fonts-matplotlib.html
* Remove the matplotlib cache dir, For me this was `~/.matplotlib`
* Restart Jupyter

### Installing Logos

* Logos should be copied to `untracked\data\logos\`
* The default logo names in styles are `black_logo.png` and `white_logo.png` for
  the light and dark styles respectively. You should either rename your logos to match
  or adjust the logo names in `data/props.json`.
* Logo style information defined in `data/props.json` should be adjusted appropriately.
   - Note that the default value for `base_scale` assumes a very large logo that 
     is downscaled.