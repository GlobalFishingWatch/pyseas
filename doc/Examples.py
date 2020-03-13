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
from pandas.plotting import register_matplotlib_converters
import matplotlib.font_manager as fm
register_matplotlib_converters()

from pyseas import maps, colors, cm, styles, grid as gridmod
from pyseas.contrib import plot_tracks
import imp
def reload():
    imp.reload(colors)
    imp.reload(styles)
    imp.reload(maps)
    imp.reload(cm)
    imp.reload(plot_tracks)
    imp.reload(gridmod)
reload()

# %matplotlib inline
# -

# ## Global Raster Plots

# !gsutil cp -n gs://machine-learning-dev-ttl-120d/named-achorages01-raster.tiff ../untracked/
img = skimage.io.imread("../untracked/named-achorages01-raster.tiff")

# ### Global map centered over the Pacific using Dark Style

with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(18, 6))
    ax, im = maps.plot_raster(img[::10, ::10], projection='global.pacific_centered', cmap=cm.presence)
    maps.add_eezs(ax)

with plt.rc_context(styles.light):
    fig = plt.figure(figsize=(18, 6))
    projection = cartopy.crs.EqualEarth(central_longitude=-160)
    ax, im = maps.plot_raster(img[::10, ::10], projection=projection, cmap=cm.presence)
    maps.add_eezs(ax)

# ### Global Map with a Colorbar

# +
# TODO: Make colorbar easy

with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(18, 6))
    ax, im = maps.plot_raster(img[::10, ::10], cmap=cm.fishing)
    cb_ax = fig.add_axes([0.51, 0.93, 0.15, 0.012]) 
    cb = fig.colorbar(im, cb_ax, orientation='horizontal')
    _ = ax.set_title("distance to shore (km)" + " " * 47, pad=23,
                    fontdict={'fontsize': 12, 'verticalalignment': 'center'})
# -

with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(12,6))
    ax, im = maps.plot_raster(img[::40, ::40], cmap=cm.fishing)
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
    maps.plot_raster_w_colorbar(img[::40, ::40], "distance to shore (km)", cmap=cm.fishing)

with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(12,7))
    gs = plt.GridSpec(2, 3, fig, height_ratios=[.015, 1], hspace=0, wspace=0.015)
    ax, im = maps.plot_raster(img[::40, ::40], gs[1, :], cmap=cm.fishing)
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
    ax, im = maps.plot_raster(img[::40, ::40], gs[0, :], cmap=cm.fishing)
    cb_ax = plt.subplot(gs[1, 2])
    cb = fig.colorbar(im, cb_ax, orientation='horizontal', shrink=0.8)
    leg_ax = plt.subplot(gs[1, 1], frame_on=False)
    leg_ax.axes.get_xaxis().set_visible(False)
    leg_ax.axes.get_yaxis().set_visible(False)
    _ = leg_ax.text(1, 0.5, "distance to shore (km)", fontdict={'fontsize': 12}, 
                    horizontalalignment='right', verticalalignment='center')

with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(18, 6))
    ax, im = maps.plot_raster(img[::10, ::10], cmap=cm.fishing)
    cb_ax = fig.add_axes([0.615, 0.93, 0.15, 0.012]) 
    cb = fig.colorbar(im, cb_ax, orientation='horizontal')
    _ = ax.set_title(" " * 46 + "distance to shore (km)", pad=23,
                    fontdict={'fontsize': 12, 'verticalalignment': 'center'})

with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(18, 6))
    ax, im = maps.plot_raster(img[::10, ::10], projection='regional.north_pacific', cmap=cm.fishing)
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
                                             projection='regional.north_pacific', cmap=cm.fishing)

reload()
with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(12, 8))
    ax, im, cb = maps.plot_raster_w_colorbar(img[::40, ::40], "distance to shore (km)", loc="bottom",
                                             projection='regional.north_pacific', cmap=cm.fishing)

reload()
with plt.rc_context(styles.dark):
    fig = plt.figure(figsize=(12, 8))
    ax, im, cb = maps.plot_raster_w_colorbar(img[::40, ::40], "distance to shore (km)", loc="bottom",
                                             projection='regional.north_pacific', cmap=cm.fishing,
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
grid_presence = pd.read_gbq(query, project_id='world-fishing-827', dialect='standard')  

reload()
grid = gridmod.df2grid(grid_presence, 'lon_bin', 'lat_bin', 'hours', xyscale=10)

reload()
plt.rc('text', usetex=False)
fig = plt.figure(figsize=(14, 10))
norm = mpcolors.LogNorm(vmin=0.01, vmax=1000)
with plt.rc_context(styles.dark):
    ax, im, cb = maps.plot_raster_w_colorbar(np.minimum(grid, 1000), 
                                       "hours of presence per ???",
                                        projection='global.default',
                                       cmap=cm.dark.presence,
                                      norm=norm,
                                      loc='bottom')
    maps.add_countries(ax)
    maps.add_eezs(ax)
    ax.set_title('Seismic Vessels')
    maps.add_figure_background(fig)
plt.savefig('/Users/timothyhochberg/Desktop/test_plot.png', dpi=300)

reload()
grid2 = gridmod.df2grid(grid_presence, 'lon_bin', 'lat_bin', 'hours', xyscale=10, origin='lower')

reload()
plt.rc('text', usetex=False)
fig = plt.figure(figsize=(14, 10))
norm = mpcolors.LogNorm(vmin=0.01, vmax=1000)
with plt.rc_context(styles.light):
    ax, im, cb = maps.plot_raster_w_colorbar(np.minimum(grid2, 1000), 
                                       "hours of presence per ???",
                                        projection='global.default',
                                       cmap=cm.dark.presence,
                                      norm=norm,
                                      origin='lower',
                                      loc='bottom')
    maps.add_countries(ax)
    maps.add_eezs(ax)
    ax.set_title('Seismic Vessels')
    maps.add_figure_background(fig)
plt.savefig('/Users/timothyhochberg/Desktop/test_plot_2.png', dpi=300)


