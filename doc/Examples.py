# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Examples of Plotting with *pyseas*

# +
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mpcolors
import matplotlib.gridspec as gridspec
from pathlib import Path
import skimage.io
import pandas as pd
import cartopy
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import pyseas.maps as psm
import pyseas.contrib as psc
import pyseas.cm

# %matplotlib inline

data_dir = Path(pyseas.__file__).parents[1] / 'doc' / 'data'
# -

# ## Recomended Style
#
#      import pyseas.maps as psm

# ## Basic Mapping
#
# Projections can be specified by using any of the names found in the acompanying 
# `projection_info.md` document, or with any Cartopy projection. There are built in 
# light and dark styles, which are activated using `pyseas.context`.

with psm.context(psm.styles.dark):
    fig = plt.figure(figsize=(18, 6))
    psm.create_map(projection='regional.european_union')
    psm.add_land()

# In addition to `add_land` there a number of other features that can be added to maps
# including eezs, grid_lines, countries, logos, etc. If you add a logo, without specifying
# the image to use, you'll get the PySeas logo.

with psm.context(psm.styles.light):
    fig = plt.figure(figsize=(18, 6))
    psm.create_map(projection='country.china')
    psm.add_land()
    psm.add_countries()
    psm.add_eezs()
    psm.add_gridlines()
    psm.add_gridlabels()
    psm.add_logo(loc='upper left')
# plt.savefig('/Users/timothyhochberg/Desktop/pyseas_logo_test.png', dpi=300, 
# facecolor=plt.rcParams['pyseas.fig.background'])

# More commonly you'll want to either specify a custom logo as shown here, or set the default
# logo as shown below.

# +
light_logo = skimage.io.imread('../pyseas/data/logos/picc_black.png')

with psm.context(psm.styles.light):
    fig = plt.figure(figsize=(18, 6))
    psm.create_map(projection='country.china')
    psm.add_land()
    psm.add_countries()
    psm.add_eezs()
    psm.add_gridlines()
    psm.add_gridlabels()
    psm.add_logo(light_logo, loc='lower right', scale=0.2)
# -
# `set_default_logos` accepts Google Cloud Storage paths prefixed with 
# either `gs://` or `gcs://`. Logos loaded this way are locally cached.

# +
psm.styles.set_default_logos(light_logo='gs://pyseas/logos/logo_black.png', 
                             dark_logo='gs://pyseas/logos/logo_white.png', 
                             scale_adj=1.0, alpha=0.5)

with psm.context(psm.styles.dark):
    fig = plt.figure(figsize=(18, 6))
    psm.create_map(projection='country.china')
    psm.add_land()
    psm.add_countries()
    psm.add_eezs()
    psm.add_gridlines()
    psm.add_gridlabels()
    psm.add_logo(loc='lower right')
# -

# If region is not specified, you get the default global map as specified by the 
# projection name `global.default`. Currently that's ExactEarth centered at 0 longitude.

with psm.context(psm.styles.light):
    fig = plt.figure(figsize=(18, 6))
    psm.create_map()
    psm.add_land()
    psm.add_countries()
    psm.add_eezs()
    psm.add_gridlines()
    # Note gridlabels don't currently work on global maps

# ## Rasters
#
# There are facilities for creating and displaying rasters.

# # Grab some data and create a raster
seismic_presence = pd.read_csv(data_dir / 'seismic_presence_tenth_degree.csv.zip')
seismic_raster = psm.rasters.df2raster(seismic_presence, 'lon_index', 'lat_index', 'hours', 
                                         xyscale=10, origin='lower', per_km2=True)

# Display a raster along with standard colorbar.
pyseas._reload()
fig = plt.figure(figsize=(14, 7))
norm = mpcolors.LogNorm(vmin=0.001, vmax=10)
with psm.context(psm.styles.dark):
    with psm.context({'text.color' : 'white'}):
        ax, im = psm.plot_raster(seismic_raster, 
                                  projection='country.indonesia',
                                  cmap='presence',
                                  norm=norm,
                                  origin='lower')
        psm.add_colorbar(im, label=r"hours per $\mathregular{km^2}$",
                        width = .5)

# Display a raster along with standard colorbar.
fig = plt.figure(figsize=(14, 7))
norm = mpcolors.LogNorm(vmin=0.001, vmax=10)
with plt.rc_context(psm.styles.dark):
    ax, im = psm.plot_raster(seismic_raster, 
                              projection='country.indonesia',
                              cmap='presence',
                              norm=norm,
                              origin='lower')
    psm.add_countries()
    psm.add_eezs()
    ax.set_title('Seismic Vessel Presence Near Indonesia')
    fig.colorbar(im, ax=ax, 
                      orientation='horizontal',
                      fraction=0.02,
                      aspect=40,
                      pad=0.04,
                     )

# `add_colorbar` can be used with subplots. Here we just plot the same 
# thing twice and add a colorbar to the last plot.

import pyseas; pyseas._reload()
fig = plt.figure(figsize=(14, 14))
norm = mpcolors.LogNorm(vmin=0.001, vmax=10)
gs = gridspec.GridSpec(2, 1)
with plt.rc_context(psm.styles.dark):
    with psm.context({'text.color' : 'white'}):
        for i in range(2):
            ax, im = psm.plot_raster(seismic_raster, 
                                     subplot=gs[i, 0],
                                      projection='country.indonesia',
                                      cmap='presence',
                                      norm=norm,
                                      origin='lower')
            ax.set_title(f'Seismic Vessel Presence Near Indonesia - {i + 1}')
        psm.add_colorbar(im, label=r"hours per $\mathregular{km^2}$ ")

import pyseas; pyseas._reload()
fig = plt.figure(figsize=(14.7, 7.6))
norm = mpcolors.LogNorm(vmin=0.001, vmax=10)
gs = gridspec.GridSpec(2, 2, hspace=0, wspace=0.02)
with plt.rc_context(psm.styles.dark):
    with psm.context({'text.color' : (0.5, 0.5, 0.5)}):
        for i in range(2):
            for j in range(2):
                ax, im = psm.plot_raster(seismic_raster, 
                                         subplot=gs[i, j],
                                          projection='country.indonesia',
                                          cmap='presence',
                                          norm=norm,
                                          origin='lower')
        psm.add_colorbar(im, ax=ax, label=r"hours per $\mathregular{km^2}$", 
                 width=1.7, height=0.035, wspace=0.0025, valign=0.2)

# Display a raster along with standard colorbar.
pyseas._reload()
fig = plt.figure(figsize=(14, 7))
norm = mpcolors.LogNorm(vmin=0.001, vmax=10)
with psm.context(psm.styles.dark):
    with psm.context({'text.color' : 'white'}):
        ax, im = psm.plot_raster(seismic_raster, 
                                          projection='global.default',
                                  cmap='presence',
                                  norm=norm,
                                  origin='lower')
        psm.add_colorbar(im, label=r"hours per $\mathregular{km^2}$", loc='bottom')

# ### H3 Discrete Global Grids
#
# There is also support for rendering data defined in terms of H3 DGG as rasters
#
# N.B. this relies on `h3.unstable`, so might require modification to work in the future.

fishing_h3_6 = pd.read_csv(data_dir / 'fishing_h3_lvl6.csv.zip')
h3cnts_6_b = {np.uint64(int(x.h3, 16)) : x.cnt for x in fishing_h3_6.itertuples()}

fig = plt.figure(figsize=(14, 7))
norm = mpcolors.LogNorm(1, 40000)
with psm.context(psm.styles.dark):
    ax, im = psm.plot_h3_data(h3cnts_6_b, 
                              projection=cartopy.crs.LambertAzimuthalEqualArea
                                                   (central_longitude=10, central_latitude=60),
                              extent=(3.8, 25.0, 65.0, 75.4),
                              cmap='presence',
                              norm=norm)
    psm.add_countries()
    psm.add_eezs()
    ax.set_title('H3 data example')
    fig.colorbar(im, ax=ax, 
                      orientation='horizontal',
                      fraction=0.02,
                      aspect=40,
                      pad=0.04,
                     )

# ## Plotting Tracks

# There are two base functions for plotting vessel tracks. `maps.plot` is
# a simple wrapper around `plt.plot` that plots tracks specified in lat/lon,
# but is otherwise identical `plt.plot`. The alternative, `maps.add_plot` can plot plot tracks
# with multiple subsegments, using different styles for each subsegment.
#
# Both of these support creation of legends. However, the second requires a bit
# of manual intervention.

position_msgs = pd.read_csv(data_dir / 'position_messages.csv.zip')
position_msgs['timestamp'] = pd.to_datetime(position_msgs.timestamp)

# Note the use of `maps.find_projection` to find an appropriate projection and extents
# based on lat/lon data.

# Simple track plotting analogous to plt.plot
with psm.context(psm.styles.light):
    fig = plt.figure(figsize=(8, 8))
    df = position_msgs[position_msgs.seg_id == '249014000-2018-01-21T16:36:23.000000Z']
    projinfo = psm.find_projection(df.lon, df.lat)
    psm.create_map(projection=projinfo.projection)
    psm.add_land()

    psm.plot(df.lon.values, df.lat.values, label='first')
    psm.plot(df.lon.values, df.lat.values + 0.1, label='second')
    psm.plot(df.lon.values - 0.3, df.lat.values, color='purple', linewidth=3, label='third')
    
    plt.legend()

# One can use `add_plot` to display multiple plots at once or to display a single
# plot with multiple states. In the first case one uses `break_on_change=False` and
# in the second `break_on_change=True`. In either case, the value of the `props`
# argument controls the color of plotted line segments. `break_on_change` controls 
# how whether lines with a given `props` values are broken when the value changes.

# Use add plot, to display multiple tracks at once.
with psm.context(psm.styles.light):
    fig = plt.figure(figsize=(8, 8))
    df = position_msgs[position_msgs.ssvid != 220413000]
    projinfo = psm.find_projection(df.lon, df.lat)
    psm.create_map(projection=projinfo.projection, extent=projinfo.extent)
    psm.add_land()
    handles = psm.add_plot(df.lon.values, df.lat.values, df.ssvid, break_on_change=False)
    plt.legend(handles.values(), handles.keys())

# Use add plot, to display tracks with multiple values
# this simple example leaves gaps between the segments
# Generating an appropriate set of props is a bit tricky --
# here we use the built in fishing props.
with psm.context(psm.styles.light):
    fig = plt.figure(figsize=(8, 8))
    df = position_msgs[position_msgs.ssvid == 413461490]
    projinfo = psm.find_projection(df.lon, df.lat)
    psm.create_map(projection=projinfo.projection, extent=projinfo.extent)
    psm.add_land()
    handles = psm.add_plot(df.lon.values, df.lat.values, df.speed > 7, break_on_change=True,
                            props=psm.styles._fishing_props)
    plt.legend(handles.values(), ['speed <= 7 knots', 'speed > 7 knots'])

# ## Panels
#
# There are a couple of convenience functions that package up add_plot
# for a couple of common cases. These also support adding subsidiary 
# time/other-parameter plots and both functions will automatically choses
# and appropriate projection and extents based on the input data
# using `maps.find_projection`.
#
# The first of these `multi_track_panel` is specialized for plotting multiple
# tracks at once.

# +
df = position_msgs[(position_msgs.ssvid == 413461490)]
with psm.context(psm.styles.panel):
    fig = plt.figure(figsize=(12, 12))
    info = psc.multi_track_panel(df.timestamp, df.lon, df.lat, df.seg_id,
                plots=[{'label' : 'lon', 'values' : df.lon},
                       {'label' : 'lat', 'values' : df.lat}])
    plt.legend(info.legend_handles.values(), [x.split('-', 1)[1].rstrip('.000000000Z') 
                                              for x in info.legend_handles.keys()])

# There is some basic functionality for combining multiple panels as shown below.
# -

df = position_msgs[(position_msgs.ssvid == 413461490)]
with psm.context(psm.styles.panel):
    fig = plt.figure(figsize=(18, 18))
    gs = gridspec.GridSpec(2, 2)
    
    psc.multi_track_panel(df.timestamp, df.lon, df.lat, df.seg_id,
                plots=[{'label' : 'lon', 'values' : df.lon},
                       {'label' : 'lat', 'values' : df.lat}],
                gs=gs[0, 0], label_angle=-30)
    
    psc.multi_track_panel(df.timestamp, df.lon, df.lat, df.seg_id,
                plots=[{'label' : 'lon', 'values' : df.lon},
                       {'label' : 'lat', 'values' : df.lat}],
                gs=gs[0, 1], label_angle=30)
    
    psc.multi_track_panel(df.timestamp, df.lon, df.lat, df.seg_id,
                plots=[{'label' : 'lon', 'values' : df.speed}],
                gs=gs[1, 0], label_angle=30)
    
    psc.multi_track_panel(df.timestamp, df.lon, df.lat, df.seg_id,
                plots=[{'label' : 'lon', 'values' : df.speed}],
                gs=gs[1, 1], label_angle=30)

df = position_msgs[(position_msgs.ssvid == 413461490)]
with psm.context(psm.styles.panel):
    fig = plt.figure(figsize=(18, 18))
    gs = gridspec.GridSpec(1, 2, figure=fig)
    
    psc.multi_track_panel(df.timestamp, df.lon, df.lat, df.seg_id,
                plots=[{'label' : 'lon', 'values' : df.lon},
                       {'label' : 'lat', 'values' : df.lat}],
                gs=gs[0])
    
    psc.multi_track_panel(df.timestamp, df.lon, df.lat, df.seg_id,
                plots=[{'label' : 'lon', 'values' : df.lon},
                       {'label' : 'lat', 'values' : df.lat}],
                gs=gs[1])


# The second panel type, `track_state_panel`, plots single tracks with multiple states. For instance,
# fishing/non-fishing, loitering/non-loitering, etc.

df = position_msgs[(position_msgs.ssvid == 413461490)].reset_index()
with psm.context(psm.styles.panel):
    fig = plt.figure(figsize=(12, 12))
    info = psc.track_state_panel(df.timestamp, df.lon, df.lat, df.speed > 7.0,
                    plots = [{'label' : 'speed (knots)', 'values' : df.speed, 'min_y' : 0}])

# Both panel types have a number of options including `annotations` and
# `add_night_shades`.

df = position_msgs[(position_msgs.ssvid == 413461490)].reset_index()
with psm.context(psm.styles.panel):
    fig = plt.figure(figsize=(12, 12))
    info = psc.track_state_panel(df.timestamp, df.lon, df.lat, df.speed > 7.0,
                                        annotations=5, add_night_shades=True,
                    plots = [{'label' : 'speed (knots)', 'values' : df.speed, 'min_y' : 0}])

# ## Miniglobe
#
# The miniglobe gets its own section by virtue of being one of the most complex
# pieces internally, despite its relative outward simplicity. The miniglobe can
# be specified to either have an AOI indicated or a marker at the specified location.

with psm.context(psm.styles.dark):
    fig = plt.figure(figsize=(10, 10))
    ax = psm.create_map(projection='country.indonesia')
    psm.add_land(ax)
    psm.add_countries(ax)
    psm.add_miniglobe(loc='upper left')
    plt.show()

with psm.context(psm.styles.dark):
    fig = plt.figure(figsize=(10, 10))
    ax = psm.create_map(projection='country.indonesia')
    psm.add_land(ax)
    psm.add_countries(ax)
    psm.add_miniglobe(loc='lower right', central_marker='*')
    plt.show()

# ## Plotting Gaps
#
# See [PlotGap.ipynb](https://github.com/GlobalFishingWatch/rendered/blob/master/pyseas/doc/contrib/PlotGap.ipynb)
#
# (or if navigating from within a clone of the repo, go directly to the file [here](contrib/PlotGap.ipynb))

# ## Saving Plots
#
# Plots can be saved in the normal way, using `plt.savefig`. If a background
# is needed, the standard facecolor can be applied as shown below.

# +
# plt.savefig('/path/to/file.png', dpi=300, facecolor=plt.rcParams['pyseas.fig.background'])

# +
import pandas as pd

q = """
SELECT *
FROM `scratch_jaeyoon.fishing_effort_known_vs_unknown_midhighres_v20210320`
"""
df = pd.read_gbq(q, project_id='world-fishing-827', dialect='standard')

df_all = df[df["fishing_hours_all"].notnull()]
df_known = df[df["fishing_hours_known_vessels"].notnull()]
# -

df_all.head()

grid_known = psm.rasters.df2raster(df_known, 'lon_bin', 'lat_bin', 
                                     'fishing_hours_known_vessels', 
                                     xyscale=5, per_km2=True)
grid_total = psm.rasters.df2raster(df_all, 'lon_bin', 'lat_bin', 
                                     'fishing_hours_all', 
                                     xyscale=5, per_km2=True)
grid_ratio = np.divide(grid_known, grid_total, out=np.zeros_like(grid_known), 
                       where=grid_total!=0)



# +
pyseas._reload()
from pyseas.maps import bivariate

cmap = bivariate.TransparencyBivariateColormap(pyseas.cm.misc.blue_orange)

with psm.context(psm.styles.dark):
    fig = plt.figure(figsize=(15, 15), dpi=300, facecolor='white')
    ax = psm.create_map((projection='regional.north_pacific')
    psm.add_land(ax)

    norm1 = mpcolors.LogNorm(vmin=0.01, vmax=10, clip=True)
    norm2 = mpcolors.Normalize(vmin=0.0, vmax=1.0, clip=True)
    
    bivariate.add_bivariate_raster(grid_ratio, grid_total, cmap, norm1, norm2)
    
    cb_ax = bivariate.add_bivariate_colorbox(cmap, norm1, norm2,
                                            xlabel='fraction of matched fishing hours',
                                            ylabel='total fishing hours',
                                            yformat='{x:.2f}')
    
    plt.title("Fishing Effort by Identified vs. Unidentified Vessels (2019-2020)", 
              fontsize=12)
    
    plt.show()


# -

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mpcolors
import matplotlib.gridspec as gridspec
from operator import add
​
import pyseas
pyseas._reload()
import pyseas.maps as psm
​
# Set plot parameters and styling
psm.use(psm.styles.chart_style)
plt.rcParams['figure.figsize'] = (10, 6)
​
# Show all dataframe rows
pd.set_option("max_rows", 20)
# -
​
ownership_by_mmsi_table = 'world-fishing-827.scratch_jenn.ownership_by_mmsi_2012_2020_v20210601'
public_fishing_effort_table = 'global-fishing-watch.gfw_public_data.fishing_effort_byvessel_v2'
​
​
## Gets gridded fishing effort for non-overlapping MMSI with the specified ownership type and geartype.
## Default values are used to allow the user to not specify one or both of 
## the parameters, in which case the query will will not parse out effort by that attribute.
def get_gridded_fishing_effort(ownership_type=None, geartype=None):
    
    if not ownership_type:
        ownership_check = 'TRUE'
    else:
        ownership_check = ownership_type
​
    if not geartype:
        geartype_check = 'TRUE'
    elif isinstance(geartype, str):
        geartype_check = f'geartype = "{geartype}"'
    elif isinstance(geartype, list):
        geartype_check = f'geartype IN UNNEST({geartype})'
    else:
        print("Invalid geartype")
        sys.exit()
    
    
    q = f'''
    WITH 
​
    ## Get the fishing vessels of interest (i.e. foreign owned, domestic owned, etc)
    ## Remove MMSI that have identities with overlapping time ranges
    fishing_identities_of_interest AS (
        SELECT 
        mmsi,
        first_timestamp,
        last_timestamp,
        FROM `{ownership_by_mmsi_table}`
        WHERE is_fishing
        AND {ownership_check}
        AND {geartype_check}
        AND NOT timestamp_overlap
    ),
​
    ## Get the fishing activity for each mmsi and their time ranges
    ## The DISTINCT is crucial as it prevent duplication of fishing activity
    ## When multiple identities are attached to one MMSI and have
    ## overlapping time ranges.
    fishing_of_interest AS (
        SELECT DISTINCT
        b.*
        FROM fishing_identities_of_interest a
        LEFT JOIN `{public_fishing_effort_table}` b
        ON a.mmsi = b.mmsi
        AND b.date BETWEEN DATE(a.first_timestamp) AND DATE(a.last_timestamp)
        WHERE b.fishing_hours IS NOT NULL
    ),
​
    ## Group by grid cells
    fishing_of_interest_gridded AS (
        SELECT
        cell_ll_lat * 10 as cell_ll_lat,
        cell_ll_lon * 10 as cell_ll_lon,
        SUM(fishing_hours) AS fishing_hours,
        FROM fishing_of_interest
        GROUP BY cell_ll_lat, cell_ll_lon
    ),
​
    fishing_total_gridded AS (
        SELECT
        cell_ll_lat * 10 as cell_ll_lat,
        cell_ll_lon * 10 as cell_ll_lon,
        SUM(fishing_hours) AS total_fishing_in_cell,
        SUM(fishing_hours)/(SELECT SUM(fishing_hours) FROM `{public_fishing_effort_table}`) as effort_weight,
        COUNT(mmsi) as num_mmsi,
        FROM `{public_fishing_effort_table}`
        GROUP BY cell_ll_lat, cell_ll_lon
    )
​
    SELECT
    cell_ll_lat,
    cell_ll_lon,
    num_mmsi,
    fishing_hours,
    total_fishing_in_cell,
    IFNULL(SAFE_DIVIDE(fishing_hours, total_fishing_in_cell), 0) AS fishing_hours_prop,
    IFNULL(SAFE_DIVIDE(fishing_hours, total_fishing_in_cell), 0) * effort_weight AS fishing_hours_prop_weighted,
    FROM fishing_of_interest_gridded 
    JOIN fishing_total_gridded USING (cell_ll_lat, cell_ll_lon) 
    WHERE cell_ll_lat IS NOT NULL and cell_ll_lon IS NOT NULL
    '''
​
    return pd.read_gbq(q, project_id='world-fishing-827', dialect='standard')
​
​
​
# ##### Foreign
​
df_public_fishing_effort_foreign = get_gridded_fishing_effort('is_foreign')
​
# #### Total
​
# # +
q = f'''
SELECT
cell_ll_lat * 10 as cell_ll_lat,
cell_ll_lon * 10 as cell_ll_lon,
SUM(fishing_hours) AS total_fishing_in_cell,
COUNT(mmsi) as num_mmsi,
FROM `{public_fishing_effort_table}`
GROUP BY cell_ll_lat, cell_ll_lon
'''
​
df_public_fishing_effort_total = pd.read_gbq(q, project_id='world-fishing-827', dialect='standard')
# -
​
# ### Rasterize and calculate ratios
​
# # +
grid_foreign = pyseas.maps.rasters.df2raster(df_public_fishing_effort_foreign, 'cell_ll_lon', 'cell_ll_lat', 
                                     'fishing_hours', xyscale=10, per_km2=True)
grid_total = pyseas.maps.rasters.df2raster(df_public_fishing_effort_total, 'cell_ll_lon', 'cell_ll_lat', 
                                     'total_fishing_in_cell', xyscale=10, per_km2=True)
​
grid_foreign_ratio = np.divide(grid_foreign, grid_total, out=np.zeros_like(grid_foreign), where=grid_total!=0)
# -
​
​
import imp
imp.reload(pyseas)
pyseas._reload()
from pyseas.maps import bivariate
cmap = bivariate.TransparencyBivariateColormap(pyseas.cm.misc.blue_orange)
with psm.context(psm.styles.dark):
    fig = plt.figure(figsize=(15, 15), dpi=300, facecolor='white')
    ax = psm.create_map()
    psm.add_land(ax)
    norm1 = mpcolors.LogNorm(vmin=0.1, vmax=25.2, clip=True)
    norm2 = mpcolors.Normalize(vmin=0.0, vmax=1.0, clip=True)
    colorized_raster = cmap(norm2(grid_foreign_ratio), norm1(grid_total))
    psm.add_raster(colorized_raster)
    cb_ax = bivariate.add_bivariate_colorbox(cmap, norm1, norm2,
                                     xlabel='fraction of matched fishing hours',
                                    ylabel='total fishing hours', fontsize=8,
                                     height=0.4, loc = (0.8, -0.45),
                                    yformat='{x:.2f}')
    plt.title("Fishing Effort by Identified vs. Unidentified Vessels (2019-2020)", 
              fontsize=12)
    plt.show()
​
import imp
imp.reload(pyseas)
pyseas._reload()
from pyseas.maps import bivariate
cmap = bivariate.TransparencyBivariateColormap(pyseas.cm.misc.blue_orange)
with psm.context(psm.styles.dark):
    fig = plt.figure(figsize=(15, 15), dpi=300, facecolor='white')
    ax = psm.create_map()
    psm.add_land(ax)
    norm1 = mpcolors.LogNorm(vmin=0.01, vmax=25.2, clip=True)
    norm2 = mpcolors.LogNorm(vmin=0.01, vmax=1.0, clip=True)
    colorized_raster = cmap(norm2(grid_foreign_ratio), norm1(grid_total))
    psm.add_raster(colorized_raster)
    cb_ax = bivariate.add_bivariate_colorbox(cmap, norm1, norm2,
                                     xlabel='fraction of matched fishing hours',
                                    ylabel='total fishing hours', fontsize=8,
                                     height=0.4, loc = (0.8, -0.45),
                                    yformat='{x:.2f}')
    plt.title("Fishing Effort by Identified vs. Unidentified Vessels (2019-2020)", 
              fontsize=12)
    plt.show()
​
# ## Comparing the normalization
#
# When using linear, it doesn't set any masked values. When using log, it does. This means that the colorized_raster gets a blueish values in spaces that don't have values whereas those same cells get set to transparent (0,0,0,0) in the log version.
​
# #### Linear
​
norm2 = mpcolors.Normalize(vmin=0.0, vmax=1.0, clip=True)
norm2(grid_foreign_ratio)
​
colorized_raster = cmap(norm2(grid_foreign_ratio), norm1(grid_total))
colorized_raster
​
# #### Log
​
norm2 = mpcolors.LogNorm(vmin=0.01, vmax=1.0, clip=True)
norm2(grid_foreign_ratio)
​
colorized_raster = cmap(norm2(grid_foreign_ratio), norm1(grid_total))
colorized_raster
​


