# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Examples of Plotting with `pyseas`

# +
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mpcolors
import cartopy.crs
import skimage.io
import cmocean
import rendered
import numpy as np
from pandas.plotting import register_matplotlib_converters
import matplotlib.font_manager as fm
register_matplotlib_converters()

from pyseas import maps, cm, styles, rasters
import pyseas.colors
from pyseas.contrib import plot_tracks
import pyseas as pycs
import imp
def reload():
    imp.reload(cm)
    imp.reload(pycs.colors)
    imp.reload(styles)
    imp.reload(maps)
    imp.reload(plot_tracks)
    imp.reload(rasters)
reload()

# %matplotlib inline
# -

# ## Global Raster Plots

# !gsutil cp -n gs://machine-learning-dev-ttl-120d/named-achorages01-raster.tiff ../untracked/
img = skimage.io.imread("../untracked/named-achorages01-raster.tiff")

# ### Global map centered over the Pacific using Dark Style

with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(18, 6))
    ax, im = maps.plot_raster(img[::10, ::10], projection='global.pacific_centered', 
                              cmap=cm.dark.presence)
    maps.add_eezs(ax)

with plt.rc_context(styles.light):
    fig = plt.figure(figsize=(18, 6))
    projection = cartopy.crs.EqualEarth(central_longitude=-160)
    ax, im = maps.plot_raster(img[::10, ::10], projection=projection, cmap=cm.dark.presence)
    maps.add_eezs(ax)

# ### Global Map with a Colorbar

# +
# TODO: Make colorbar easy

with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(18, 6))
    ax, im = maps.plot_raster(img[::10, ::10], cmap=cm.dark.fishing)
    cb_ax = fig.add_axes([0.51, 0.93, 0.15, 0.012]) 
    cb = fig.colorbar(im, cb_ax, orientation='horizontal')
    _ = ax.set_title("distance to shore (km)" + " " * 47, pad=23,
                    fontdict={'fontsize': 12, 'verticalalignment': 'center'})
# -

with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(12,6))
    ax, im = maps.plot_raster(img[::40, ::40], cmap=cm.dark.fishing)
    cb = fig.colorbar(im, ax=ax, 
                      orientation='horizontal',
                      fraction=0.02,
                      aspect=40,
                      pad=0.04,
                     )

    _ = ax.set_title("distance to shore (km)", fontdict={'fontsize': 12})

reload()
with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(12,7))
    maps.plot_raster_w_colorbar(img[::40, ::40], "distance to shore (km)", cmap=cm.dark.fishing)

with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(12,7))
    gs = plt.GridSpec(2, 3, fig, height_ratios=[.015, 1], hspace=0, wspace=0.015)
    ax, im = maps.plot_raster(img[::40, ::40], gs[1, :], cmap=cm.dark.fishing)
    cb_ax = plt.subplot(gs[0, 2])
    cb = fig.colorbar(im, cb_ax, orientation='horizontal', shrink=0.8)
    leg_ax = plt.subplot(gs[0, 1], frame_on=False)
    leg_ax.axes.get_xaxis().set_visible(False)
    leg_ax.axes.get_yaxis().set_visible(False)
    _ = leg_ax.text(1, 0.5, "distance to shore (km)", fontdict={'fontsize': 12}, 
                    horizontalalignment='right', verticalalignment='center')

with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(12,7))
    gs = plt.GridSpec(2, 3, fig, height_ratios=[1, .015], hspace=0, wspace=0.015)
    ax, im = maps.plot_raster(img[::40, ::40], gs[0, :], cmap=cm.dark.fishing)
    cb_ax = plt.subplot(gs[1, 2])
    cb = fig.colorbar(im, cb_ax, orientation='horizontal', shrink=0.8)
    leg_ax = plt.subplot(gs[1, 1], frame_on=False)
    leg_ax.axes.get_xaxis().set_visible(False)
    leg_ax.axes.get_yaxis().set_visible(False)
    _ = leg_ax.text(1, 0.5, "distance to shore (km)", fontdict={'fontsize': 12}, 
                    horizontalalignment='right', verticalalignment='center')

with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(18, 6))
    ax, im = maps.plot_raster(img[::10, ::10], cmap=cm.dark.fishing)
    cb_ax = fig.add_axes([0.615, 0.93, 0.15, 0.012]) 
    cb = fig.colorbar(im, cb_ax, orientation='horizontal')
    _ = ax.set_title(" " * 46 + "distance to shore (km)", pad=23,
                    fontdict={'fontsize': 12, 'verticalalignment': 'center'})

with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(18, 6))
    ax, im = maps.plot_raster(img[::10, ::10], projection='regional.north_pacific', cmap=cm.dark.fishing)
    maps.add_countries(ax)
    maps.add_eezs(ax)
    cb_ax = fig.add_axes([0.645, 0.93, 0.15, 0.012]) 
    cb = fig.colorbar(im, cb_ax, orientation='horizontal')
    _ = ax.set_title(" " * 72 + "distance to shore (km)", pad=23,
                    fontdict={'fontsize': 12, 'verticalalignment': 'center'})

reload()
with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(12, 8))
    ax, im, cb = maps.plot_raster_w_colorbar(img[::40, ::40], "distance to shore (km)", loc="top",
                                             projection='regional.north_pacific', cmap=cm.dark.fishing)

reload()
with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(12, 8))
    ax, im, cb = maps.plot_raster_w_colorbar(img[::40, ::40], "distance to shore (km)", loc="bottom",
                                             projection='regional.north_pacific', cmap=cm.dark.fishing)

reload()
with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(12, 8))
    ax, im, cb = maps.plot_raster_w_colorbar(img[::40, ::40], "distance to shore (km)", loc="bottom",
                                             projection='regional.north_pacific', cmap=cm.dark.fishing,
                                            gridlines=True)
    ax.gridlines(linewidth=0.4, zorder=0.5)
    maps.add_countries(ax)

import geopandas as gpd
eezs = gpd.read_file("../untracked/data/eez_boundaries_v11.gpkg")

# ## Plotting Tracks

query = """
    select ssvid, lat, lon, timestamp, seg_id
    from `world-fishing-827.pipe_production_v20200203.messages_segmented_2018*`
    where _TABLE_SUFFIX between "0101" and "0131"
    and ssvid in ("413461490", "249014000", "220413000")
    and seg_id is not null
    order by timestamp
    """
msgs = pd.read_gbq(query, project_id='world-fishing-827', dialect='standard')  

# +
# TODO: Plotted tracks are still ugly and don't follow style guidelines

df = msgs[(msgs.ssvid == "220413000")]
for style in [styles.light, styles.dark]:
    with plt.rc_context(style):
        fig = plt.figure(figsize=(10, 5))
        ax = maps.create_map(projection='regional.north_pacific')
        maps.add_plot(ax, df.lon, df.lat, 'g.', transform=maps.identity)
        maps.add_land(ax)
        maps.add_eezs(ax)
        plt.show()
# -

# ## Predefined Regional Styles

reload()
with plt.rc_context(styles.light):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='regional.pacific')
    maps.add_land(ax)
    maps.add_countries(ax)
    plt.show()

reload()
with plt.rc_context(styles.light):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='regional.north_pacific')
    maps.add_land(ax)
    maps.add_countries(ax)
    plt.show()

reload()
with plt.rc_context(styles.light):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='regional.indian')
    maps.add_land(ax)
    maps.add_countries(ax)
    plt.show()

reload()
with plt.rc_context(styles.light):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='global.pacific_centered')
    maps.add_land(ax)
    maps.add_countries(ax)
    plt.show()

reload()
with plt.rc_context(styles.light):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='global.atlantic_centered')
    maps.add_land(ax)
    maps.add_countries(ax)
    plt.show()

reload()
with plt.rc_context(styles.light):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='country.ecuador_with_galapagos')
    maps.add_land(ax)
    maps.add_countries(ax)
    plt.show()

reload()
with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='country.indonesia')
    maps.add_land(ax)
    maps.add_countries(ax)
    plt.show()

# ## `contrib`

# ### Plot Tracks and Lat/Lon vs Time

df = msgs[(msgs.ssvid == "413461490")]
reload()
with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(10, 5))
    ts = [pd.Timestamp(x).to_pydatetime() for x in df.timestamp]
    ax1, ax2, ax3 = plot_tracks.plot_tracks_panel(ts, df.lon, df.lat)

# ## Publish

rendered.publish_to_github('./Examples.ipynb', 
                           'pyseas/doc', action='push')

reload()
maps.get_extent('regional.pacific')

# Indian Ocean
with plt.rc_context(styles.light):
    fig = plt.figure(figsize=(10, 5))
    projection = cartopy.crs.LambertAzimuthalEqualArea(75, 0)
    ax = maps.create_map(projection=projection)
    maps.add_land(ax)
    maps.add_eezs(ax)
    maps.add_countries(ax)
    ax.set_extent((15, 145, -30, 15))
    plt.show()

# Indian Ocean
with plt.rc_context(styles.light):
    fig = plt.figure(figsize=(10, 5))
    projection = cartopy.crs.LambertAzimuthalEqualArea(75, 0)
    ax = maps.create_map(projection=projection)
    maps.add_land(ax)
    maps.add_eezs(ax)
    maps.add_countries(ax)
    ax.set_extent((15, 145, -30, 15))
    plt.show()

reproj_eez = gpd.read_file('/Users/timothyhochberg/Downloads/eez_ee_160.gpkg')

with plt.rc_context(styles.light):
    fig = plt.figure(figsize=(18, 6))
    projection = cartopy.crs.EqualEarth(central_longitude=160)
    ax = maps.create_map(projection=projection)
    maps.add_land(ax)
    ax.add_geometries(reproj_eez.geometry, crs=projection, edgecolor='w', alpha=1, linewidth=1)

with plt.rc_context(styles.light):
    fig = plt.figure(figsize=(18, 6))
    projection = cartopy.crs.PlateCarree(central_longitude=160)
    ax = maps.create_map(projection=projection)
    maps.add_land(ax)
#     ax.add_geometries(reproj_eez.geometry, crs=projection, edge

query = """
with seismic as 
(select distinct ssvid from (
select ssvid, v  from `gfw_research.vi_ssvid_v20200312` cross join
unnest(registry_info.best_known_vessel_class) v
 ) where v = 'seismic_vessel'
 ),
 good_segs as (select seg_id from `gfw_research.pipe_v20190502_segs`  where 
 good_seg and not overlapping_and_short
 and positions > 20)
 select 
 floor(lat*10) lat_bin,
 floor(lon*10) lon_bin,
 sum(hours) hours,
 sum(if(nnet_score>.5,1,0)) fishing_hours
 from `gfw_research.pipe_v20190502` 
 join seismic
 using(ssvid)
 where date between timestamp("2019-01-01") and timestamp("2019-12-31")
 and seg_id in (select seg_id from good_segs)
 group by lat_bin, lon_bin
 """
df_presence = pd.read_gbq(query, project_id='world-fishing-827', dialect='standard')  

raster = rasters.df2raster(df_presence, 'lon_bin', 'lat_bin', 'hours', xyscale=10)

reload()
fig = plt.figure(figsize=(10, 10))
norm = mpcolors.LogNorm(vmin=0.01, vmax=1000)
with maps.context(styles.dark):
    ax, im, cb = maps.plot_raster_w_colorbar(raster, 
                                       "hours of presence per ???",
                                        projection='regional.north_pacific',
                                       cmap='presence',
                                      norm=norm,
                                      loc='bottom')
    maps.add_countries(ax)
    ax.set_title('Seismic Vessels')
    maps.add_figure_background(fig)
plt.savefig('/Users/timothyhochberg/Desktop/test_plot.png', dpi=300)

reload()
fig = plt.figure(figsize=(14, 10))
norm = mpcolors.LogNorm(vmin=0.01, vmax=1000)
with maps.context(styles.dark):
    ax, im, cb = maps.plot_raster_w_colorbar(raster, 
                                       "hours of presence per ???",
                                        projection='country.indonesia',
                                       cmap='presence',
                                      norm=norm,
                                      loc='bottom')
    maps.add_countries(ax)
    maps.add_eezs(ax)
    ax.set_title('Seismic Vessels')
    maps.add_figure_background(fig)
plt.savefig('/Users/timothyhochberg/Desktop/test_plot.png', dpi=300)

reload()
grid2 = pycs.rasters.df2raster(grid_presence, 'lon_bin', 'lat_bin', 'hours', xyscale=10, origin='lower')

reload()
plt.rc('text', usetex=False)
fig = plt.figure(figsize=(14, 10))
norm = mpcolors.LogNorm(vmin=0.01, vmax=1000)
with plt.rc_context(styles.light):
    ax, im, cb = maps.plot_raster_w_colorbar(np.minimum(grid2, 1000), 
                                       "hours of presence per ???",
                                        projection='regional.north_pacific',
                                       cmap='presence',
                                      norm=norm,
                                      origin='lower',
                                      loc='bottom')
    maps.add_countries(ax)
    maps.add_eezs(ax)
    ax.set_title('Seismic Vessels')
    maps.add_figure_background(fig)
plt.savefig('/Users/timothyhochberg/Desktop/test_plot_2.png', dpi=300)

min_lon = 0
min_lat = -55
max_lon = 150
max_lat = 33
q = '''with fishing_vessels
as 
(select ssvid,best.best_vessel_class vessel_class
from `gfw_research.vi_ssvid_byyear_v20200115` 
where on_fishing_list_best 
and activity.overlap_hours < 24
and not activity.offsetting 
and activity.fishing_hours > 10
and year = 2019
),
good_segs as (
select seg_id from `gfw_research.pipe_v20190502_segs` 
where good_seg and not overlapping_and_short 
and positions > 20),
activity_table as (
select distinct lat, lon, nnet_score2, hours,
ssvid, seg_id from `gfw_research.pipe_v20190502_fishing` 
where date between timestamp("2019-01-10") and timestamp("2020-01-01")
)
select floor(lat*4) lat_bin,
floor(lon*4) lon_bin,
vessel_class,
sum(if(nnet_score2>.5, hours,0)) fishing_hours,
sum(hours) hours
from activity_table
join fishing_vessels
using(ssvid)
where lon between {min_lon} and {max_lon} 
and lat between {min_lat} and {max_lat}
and seg_id in (select seg_id from good_segs)
group by lat_bin, lon_bin, vessel_class'''.format(min_lon=min_lon,
                                                 min_lat=min_lat,
                                                 max_lon=max_lon,
                                                 max_lat=max_lat)
df_fishing = pd.read_gbq(q, project_id='world-fishing-827')

# +
reload()
min_lon = 0
min_lat = -55
max_lon = 150
max_lat = 33

grid_fishing  = pycs.grid.df2raster(df_fishing, 'lon_bin', 'lat_bin', 'fishing_hours', xyscale=4,
                                     extent = [min_lon, max_lon, min_lat, max_lat])
grid_fishing_longlines  = pycs.grid.df2raster(df_fishing[df_fishing.vessel_class=='drifting_longlines'],
                                                'lon_bin', 'lat_bin', 'fishing_hours', xyscale=4,
                                               extent = [min_lon, max_lon, min_lat, max_lat])
grid_fishing_presence  = pycs.grid.df2raster(df_fishing, 'lon_bin', 'lat_bin', 'hours', xyscale=4,
                                              extent = [min_lon, max_lon, min_lat, max_lat])
grid_fishing_vessel_presence_longlines = pycs.grid.df2raster(df_fishing[df_fishing.vessel_class=='drifting_longlines'],
                                                'lon_bin', 'lat_bin', 'hours', xyscale=4,
                                                              extent = [min_lon, max_lon, min_lat, max_lat])
with plt.rc_context(pycs.styles.dark): #, plt.rc_context({'gfw.border.linewidth' : 0}):
    fig_min_value = 5
    fig_max_value = 5000
    projection = cartopy.crs.LambertAzimuthalEqualArea(75, 0)
    cmap = pycs.cm.dark.presence
    norm = mpcolors.LogNorm(vmin=fig_min_value, vmax=fig_max_value)
    fig = plt.figure(figsize=(10, 10))
    ax, im, colorbar = pycs.maps.plot_raster_w_colorbar(grid_fishing_presence,
                            "hours of presence of fishing vessels per 0.25 degree square",   cmap=cmap,
                            loc='bottom',  
                            extent = [min_lon + 0.01, max_lon, min_lat, max_lat],
                            norm = norm, 
                            projection=projection)
    pycs.maps.add_eezs(ax)
    ax.set_extent((15, 145, -30, 15))
    ax.set_title("Fishing Activity in the Indian Ocean and Study Area")
#     ax.add_geometries([overpasses], crs = ccrs.PlateCarree(),
#                   alpha=1, facecolor='none', edgecolor='red') # for Lat/Lon data.
    

# +
def reverse(code):
    c1 = code[1:3]
    c2 = code[3:5]
    c3 = code[5:7]
    vals = (255 - int(c, 16) for c in [c1, c2, c3])
    return '#' + ''.join(hex(x)[2:] for x in vals)

reverse('#0c276c')
