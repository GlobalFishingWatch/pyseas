
<h4>
<img src="gfw_logo.png" alt="GFW Logo" height="40"  valign="middle"/>
Global Fishing Watch
</h4>

# PySeas

A library to make GFW style maps in Python.

## Using Pyseas

### Via UV

Install [UV](https://docs.astral.sh/uv/) if you don't already have it.

    git clone https://github.com/GlobalFishingWatch/pyseas.git
    cd pyseas
    uv sync

Then run `uv run jupyter notebook`, or `uv run python` for a shell, either of
which will have `pyseas` available.

All dependencies (including `cartopy`, `geopandas`, and `rasterio`) install
cleanly from PyPI wheels — no system GDAL/GEOS/PROJ install is required.

### As a dependency in another UV project

PySeas isn't published to PyPI, so add it as a Git dependency. From the other
project's directory:

    uv add "git+https://github.com/GlobalFishingWatch/pyseas.git"

This adds the following to that project's `pyproject.toml`:

```toml
[project]
dependencies = [
    "pyseas",
    # ...
]

[tool.uv.sources]
pyseas = { git = "https://github.com/GlobalFishingWatch/pyseas.git" }
```

(Equivalently, add those two snippets by hand and run `uv sync`.)

By default this tracks the tip of the repo's default branch. For a reproducible,
pinned install, add `--rev <commit-sha>` (or `--tag <tag>`) to the `uv add`
command above, which records a `rev =` (or `tag =`) key in `tool.uv.sources`
instead of tracking a moving branch.

As with using PySeas directly, no system GDAL/GEOS/PROJ install is needed —
`cartopy`, `geopandas`, and `rasterio` all resolve from PyPI wheels.

## Documentation

Examples of common plotting tasks are shown in [pyseas/doc/Examples.md](pyseas/doc/Examples.md),
or on [github](https://github.com/GlobalFishingWatch/rendered/blob/master/pyseas/pyseas/doc/Examples.md).

## Acknowledgments

* EEZ boundaries are drawn using *World EEZ v11* from [Marine Regions](https://www.marineregions.org/)
  licensed under [CC-BY](https://creativecommons.org/licenses/by/4.0/).

* The *Roboto* fonts from [Google](https://fonts.google.com/specimen/Roboto) licensed under
  [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
