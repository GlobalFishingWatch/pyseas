# PySeas

A library to make GFW style map plots in Python.

*Please note all interfaces are still in flux and not gauranteed to be stable!*

## To Do

* Make lat and lon markers with numbers easy and styleable
    - See examples for how to do it the hard way.
    - Also: https://gist.github.com/ajdawson/dd536f786741e987ae4e
* Bulletproof Scalebar
* Guides on how to highlight multiple areas
* Categorical color scheme to tell fleets apart

## Installation

Current recommendation is `pip install -e .`.
Install cartopy using `conda install -c conda-forge cartopy`
Install geopandans using `conda install -c conda-forge geopandas`

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