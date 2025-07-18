
<h4>
<img src="gfw_logo.png" alt="GFW Logo" height="40"  valign="middle"/>
Global Fishing Watch
</h4>

# PySeas

A library to make GFW style maps in Python.

## Using Pyseas

### Via Pixi

Install Pixi as shown [here].

Then run either `pixi shell` or `pixi run jupyter notebook`. This will start a shell
or run a notebook in a mininal environment that includes `pyseas`.

This environment is decribed in the `pyproject.toml` file and is best modified using
`pixi add`. For more information see [info.sh](info.sh)

### Using Conda

Some of the dependencies do not install cleanly via `pip`, so the recommended approach
is to install them using Conda. The following recipes is currently preferred:

    git clone https://github.com/GlobalFishingWatch/pyseas.git
    cd pyseas

Then, to install in new Conda environment named `pyseas`:

    conda create -c conda-forge -y -n pyseas python=3.11 cartopy gdal
    conda activate pyseas
    pip install -e .

Or, to install in an existing Conda environment:

    conda activate CONDA-ENV-NAME
    conda install -c conda-forge -y -n CONDA-ENV-NAME python=3.11 cartopy gdal
    pip install -e .

If you are not interested in the `Examples` notebooks, you may omit `-e` and
avoid the in-place install.

## Documentation

Examples of common plotting tasks are shown in [pyseas/doc/Examples.md](pyseas/doc/Examples.md),
or on [github](https://github.com/GlobalFishingWatch/rendered/blob/master/pyseas/pyseas/doc/Examples.md).

## Acknowledgments

* EEZ boundaries are drawn using *World EEZ v11* from [Marine Regions](https://www.marineregions.org/)
  licensed under [CC-BY](https://creativecommons.org/licenses/by/4.0/).

* The *Roboto* fonts from [Google](https://fonts.google.com/specimen/Roboto) licensed under
  [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
