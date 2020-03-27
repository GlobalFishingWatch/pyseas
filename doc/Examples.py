# -*- coding: utf-8 -*-
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

from pyseas import maps, cm, styles, util
import pyseas.colors
from pyseas.contrib import plot_tracks
from pyseas.maps import scalebar, core, rasters
import imp

import shapely.geometry as sgeom
from shapely.prepared import prep

from pyseas.maps._monkey_patch_cartopy import monkey_patch_cartopy
from pyseas.maps import ticks


def reload():
    imp.reload(util)
    imp.reload(ticks)
    imp.reload(scalebar)
    imp.reload(pyseas.colors)
    imp.reload(cm)
    imp.reload(styles)
    imp.reload(rasters)
    imp.reload(core)
    imp.reload(maps)
    imp.reload(plot_tracks)
    imp.reload(pyseas)
reload()

# %matplotlib inline
# -

# ## Recomended Style
#
# Import maps and styles directly. For other modules, reference
# through the pyseas namespace.
#
#      import pyseas
#      from pyseas import maps, styles
#      
#  Tentative and subject to revision.

# +
# conda upgrade --channel conda-forge cartopy
# -

# ## Global Raster Plots

# !gsutil cp -n gs://machine-learning-dev-ttl-120d/named-achorages01-raster.tiff ../untracked/
img = skimage.io.imread("../untracked/named-achorages01-raster.tiff")

reload()
ax = maps.create_map(projection='country.peru')
maps.add_land(ax)

# ### Global map centered over the Pacific using Dark Style

reload()
with pyseas.context(styles.dark):
    fig = plt.figure(figsize=(18, 6))
    ax, im = maps.plot_raster(img[::10, ::10],
                                   projection='global.pacific_centered', 
                                   cmap='presence')
    maps.add_eezs(ax)

# ## Simple, Manual Colorbar

with pyseas.context(styles.dark):
    fig = plt.figure(figsize=(12,6))
    ax, im = maps.plot_raster(img[::40, ::40], cmap='fishing')
    cb = fig.colorbar(im, ax=ax, 
                      orientation='horizontal',
                      fraction=0.02,
                      aspect=40,
                      pad=0.04,
                     )

    _ = ax.set_title("distance to shore (km)", fontdict={'fontsize': 12})

# ## Auto Colorbar

reload()
with pyseas.context(styles.dark):
    fig = plt.figure(figsize=(12,7))
    maps.plot_raster_w_colorbar(img[::40, ::40], 
                                "distance to shore (km)", 
                                cmap='fishing')

reload()
with pyseas.context(styles.dark):
    fig = plt.figure(figsize=(12, 8))
    ax, im, cb = maps.plot_raster_w_colorbar(img[::40, ::40], 
                                             "distance to shore (km)", 
                                             loc="top",
                                             projection='regional.atlantic', 
                                             cmap='fishing')

reload()
with pyseas.context(styles.light):
    fig = plt.figure(figsize=(12, 8))
    ax, im, cb = maps.plot_raster_w_colorbar(img[::40, ::40], 
                                             "distance to shore (km)", 
                                             loc="top",
                                             projection='regional.atlantic', 
                                             cmap='presence')
    ax.gridlines(linewidth=0.4, zorder=0.5)

# ## Adding Gridlines

reload()
with pyseas.context(styles.dark):
    fig = plt.figure(figsize=(12, 8))
    ax, im, cb = maps.plot_raster_w_colorbar(img[::40, ::40], 
                                             "distance to shore (km)", 
                                             loc="top",
                                             projection='regional.north_pacific', 
                                             cmap='fishing')
    ax.gridlines(linewidth=0.4, zorder=0.5)
    maps.add_countries(ax)

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

plt.rcParams['axes.prop_cycle']

ssvids = sorted(set(msgs.ssvid))
ssvids

reload()
for style, style_name in [(pyseas.styles.light, 'light'), 
                          (pyseas.styles.dark, 'dark')]:
    with pyseas.context(style):
        fig = plt.figure(figsize=(10, 10))
        ax = maps.create_map(projection='regional.north_pacific')
        maps.add_land(ax)
        maps.add_plot(ax, msgs.lon, msgs.lat, msgs.ssvid)


# +
# TODO: Plotted tracks are still ugly and don't follow style guidelines
reload()

def find_ranges(lons):
    ranges = []
    i0 = 0
    for i, lon in enumerate(lons):
        if abs(lons[i0] - lon) > 180:
            ranges.append((i0, i))
            i0 = i + 1
    ranges.append((i0, len(lons)))
    return ranges
    
for style, style_name in [(pyseas.styles.light, 'light'), 
                          (pyseas.styles.dark, 'dark')]:
    with pyseas.context(style):
        cycle = iter(plt.rcParams['axes.prop_cycle'])
        fig = plt.figure(figsize=(10, 10))
        ax = maps.create_map(projection='regional.north_pacific')
        maps.add_land(ax)
        for ssvid in ssvids:
            df = msgs[(msgs.ssvid == ssvid)]
            props = next(cycle)
            for i0, i1 in find_ranges(df.lon.values):
                
                ax.plot(df.lon.iloc[i0:i1], df.lat.iloc[i0:i1], 
                              transform=maps.identity, **props, linewidth=1)
        gl = ax.gridlines(linewidth=0.4, zorder=0.5)
        extent = ax.get_extent(crs=maps.identity)
#         print(gl.xlocator.tick_values(*extent[:2]))
#         print(gl.ylocator.tick_values(*extent[2:]))
        for lon, lat, lbl, ngl in [(180, -3.8, "180°W", 0),
                                   (-120, -8.5, "120°W", 0),
                                   (-50.5, 30, "30°N", 0),
                                   (-37.0, 15, "15°N", 0),
                                  ]:
            ax.text(lon, lat, lbl, transform=maps.identity, rotation=ngl, 
                   horizontalalignment='center')
        plt.savefig('/Users/timothyhochberg/Desktop/test_tracks_{}.png'.format(
                style_name), dpi=300)
        plt.show()
# -


# ## Predefined Regional Styles

reload()
with pyseas.context(styles.light):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='regional.pacific')
    maps.add_land(ax)
    maps.add_countries(ax)
    gl = ax.gridlines(linewidth=0.4, zorder=0.5)
    extent = ax.get_extent(crs=maps.identity)
    print(gl.xlocator.tick_values(*extent[:2]))
    print(gl.ylocator.tick_values(*extent[2:]))
    for lon, lat, lbl, ngl in [(-179, 4, "180°W", 90),
                               (-155, 12, "15°N", 0)]:
        ax.text(lon, lat, lbl, transform=maps.identity, rotation=ngl
#         fontdict={'color' : 'black', 'weight': 'bold', 'size' : 10},
#         bbox=dict(facecolor='none', edgecolor='black', boxstyle='circle')
            )
    plt.show()

reload()
with pyseas.context(styles.light):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='regional.south_pacific')
    maps.add_land(ax)
    maps.add_countries(ax)
    plt.show()

reload()
with pyseas.context(styles.light):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='country.chile')
    maps.add_land(ax)
    maps.add_countries(ax)
    plt.show()

reload()
with pyseas.context(styles.dark):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='regional.south_pacific')
    maps.add_land(ax, 'regional.south_pacific')
    maps.add_countries(ax)
    plt.show()

reload()
with pyseas.context(styles.light):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='country.ecuador_with_galapagos')
    maps.add_land(ax)
    maps.add_countries(ax)
    plt.show()

reload()
with pyseas.context(styles.dark):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='country.indonesia')
    maps.add_land(ax)
    maps.add_countries(ax)
    plt.show()

# ## `contrib`

# ### Plot Tracks and Lat/Lon vs Time

df = msgs[(msgs.ssvid == "413461490")]
reload()
with pyseas.context(styles.dark):
    fig = plt.figure(figsize=(10, 5))
    ts = [pd.Timestamp(x).to_pydatetime() for x in df.timestamp]
    ax1, ax2, ax3 = plot_tracks.plot_tracks_panel(ts, df.lon, df.lat)

# ## Publish

# +
# rendered.publish_to_github('./Examples.ipynb', 
#                            'pyseas/doc', action='push')
# -

# ## Below this point is messy

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

reload()
raster = maps.rasters.df2raster(df_presence, 'lon_bin', 'lat_bin', 'hours', xyscale=10, per_km2=True)

reload()
fig = plt.figure(figsize=(10, 10))
norm = mpcolors.LogNorm(vmin=0.01, vmax=100)
with pyseas.context(styles.dark):
    projection = cartopy.crs.EqualEarth(central_longitude=-165)
    ax, im, cb = maps.plot_raster_w_colorbar(raster, 
                                       "hours of presence per km2",
                                        projection='regional.pacific',
                                       cmap='presence', 
                                      norm=norm,
                                      loc='bottom')
    cb.set_ticks([1, 10, 100, 1000, 1000])
    maps.add_countries(ax)
    ax.set_title('Seismic Vessels')
    maps.add_figure_background(fig)
plt.savefig('/Users/timothyhochberg/Desktop/test_plot.png', dpi=300)

reload()
fig = plt.figure(figsize=(14, 10))
norm = mpcolors.LogNorm(vmin=0.01, vmax=1)
with pyseas.context(styles.dark):
    ax, im, cb = maps.plot_raster_w_colorbar(raster, 
                                       "hours of presence per km2",
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
raster2 = maps.rasters.df2raster(df_presence, 'lon_bin', 'lat_bin', 'hours', 
                                 xyscale=10, origin='lower', per_km2=True)

reload()
plt.rc('text', usetex=False)
fig = plt.figure(figsize=(14, 10))
norm = mpcolors.LogNorm(vmin=0.01, vmax=1)
with plt.rc_context(styles.light):
    ax, im, cb = maps.plot_raster_w_colorbar(raster2, 
                                       "hours of presence per km2",
                                        projection='regional.south_pacific',
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

grid_fishing_presence  = maps.rasters.df2raster(df_fishing, 'lon_bin', 'lat_bin', 'hours', xyscale=4,
                                              extent = [min_lon, max_lon, min_lat, max_lat],
                                                per_km2=True, scale=60)

with plt.rc_context(styles.dark): 
    fig_min_value = 1
    fig_max_value = 100
    norm = mpcolors.LogNorm(vmin=fig_min_value, vmax=fig_max_value)
    fig = plt.figure(figsize=(10, 10))
    ax, im, colorbar = maps.plot_raster_w_colorbar(
                            grid_fishing_presence,
                            "seconds per square km",   
                            cmap='presence',
                            loc='bottom',  
                            extent = [min_lon + 0.01, max_lon, min_lat, max_lat],
                            norm = norm, 
                            projection='regional.indian')
    pyseas.maps.add_eezs(ax)
    pyseas.maps.add_countries(ax)
    ax.set_extent((15, 145, -30, 15), crs=maps.identity)
    ax.set_title("Fishing Vessel Presence in the Indian Ocean overlaid with Study Area")
#     ax.add_geometries([overpasses], crs = ccrs.PlateCarree(),
#                   alpha=1, facecolor='none', edgecolor='red') # for Lat/Lon data.
    
# -
reload()
with pyseas.context(pyseas.styles.dark):
    fig = plt.figure(figsize=(12, 8))
    ts = [pd.Timestamp(x).to_pydatetime() for x in df.timestamp]
    ax1, ax2, ax3 = plot_tracks.plot_tracks_panel(ts, df.lon, df.lat, df['ssvid'] )
    maps.add_figure_background(fig)
    fig.suptitle(df['ssvid'].iloc[0] + ' - tracks ' , y=0.93) 
    plt.show()


query = """
WITH 

good_segs as (
select seg_id from `gfw_research.pipe_v20190502_segs` 
where good_seg and not overlapping_and_short 
and positions > 20),

source as (
select ssvid, vessel_id, timestamp, lat, lon, course, speed, elevation_m
FROM
    `pipe_production_v20190502.position_messages_2018*`
where seg_id in (select * from good_segs)
),

ssvid_list as (
select distinct ssvid from 
source
where ssvid in (SELECT cast(id as string) FROM machine_learning_dev_ttl_120d.det_info_mmsi_v20200124
                where split=0)
order by farm_fingerprint(ssvid)
limit 2
)

SELECT
source.*, score.nnet_score as nnet_score
from source
LEFT JOIN
    `machine_learning_dev_ttl_120d.fd_vid_20200320_results_*` score
  ON
    source.vessel_id = score.vessel_id
    AND source.timestamp BETWEEN score.start_time
    AND score.end_time
where ssvid in (select * from ssvid_list)
order by timestamp
"""
fishing_df = pd.read_gbq(query, project_id='world-fishing-827', dialect='standard')  

# +
reload() # >>>

ssvids = sorted(set(fishing_df.ssvid))[1:]

with pyseas.context(pyseas.styles.light):
    for ssvid in ssvids:
        ssvid_df = fishing_df[fishing_df.ssvid == ssvid]
        ssvid_df = ssvid_df.sort_values(by='timestamp')
        if not len(ssvid_df):
            continue
            
        proj, extent, descr = plot_tracks.find_projection(ssvid_df.lon, ssvid_df.lat)
        fig = plt.figure(figsize=(10, 10))
        ax = maps.create_map(projection=proj, proj_descr=descr)

        gl = ax.gridlines(linewidth=0.4, zorder=0.5, alpha=0.5)        
        
        ax.set_extent(extent, crs=maps.identity)
        
#         print(gl.xlocator.tick_values(*extent[:2]))
#         print(gl.ylocator.tick_values(*extent[2:]))
        for lon, lat, lbl, ngl in [
                                    (30, -46.2, "30°E", 0),
                                    (40, -48.5, "40°E", 0),
                                    (50, -50, "50°E", 0),
                                    (60, -50.7, "60°E", 0),
                                    (70, -50.8, "70°E", 0),

                                   (81.4, -42, "42°S", 0),
                                   (80.1, -36, "36°S", 0),
                                   (79, -30, "30°S", 0),
                                   (78, -24, "24°S", 0),
                                   (77.4, -18, "18°S", 0),
                                   (77, -12, "12°S", 0),


#                                    (-37.0, 15, "15°N", 0),
                                  ]:
            ax.text(lon, lat, lbl, transform=maps.identity, rotation=ngl, 
                   horizontalalignment='center')
        maps.add_land(ax)
        maps.add_countries(ax)
        is_fishing = (ssvid_df.nnet_score.values > 0.5)      
        
        maps.add_plot(ax, ssvid_df.lon.values, ssvid_df.lat.values, is_fishing, 
                      props=styles.dark['gfw.map.fishingprops'], break_on_change=True)
        
        ax.set_extent(extent, crs=maps.identity)
#         maps.add_scalebar(ax, extent)

#         ax.set_title(ssvid)
        maps.add_figure_background(fig)

        plt.savefig('/Users/timothyhochberg/Desktop/test_grid.png', dpi=300)

        plt.show()
# -

from scipy.signal import medfilt

# +
reload()

ssvids = sorted(set(fishing_df.ssvid))[1:]

# TODO: figure out style for dark panel (use gfw.panel.background as color)
# See Juan Carlos's example in this post: 
# https://globalfishingwatch.slack.com/archives/CUW93UNLS/p1585062098015100
# (Obvious things: background, and line/tick colors)
with pyseas.context(pyseas.styles.light):
    with pyseas.context({'gfw.fig.background' : 'white',
                         'gfw.ocean.color' : 'white',
                          'gfw.fig.background' : 'white'}):
        for ssvid in ssvids:

            dfn = fishing_df[fishing_df.ssvid == ssvid]
            dfn = dfn.sort_values(by='timestamp')
            is_fishing = (dfn.nnet_score > 0.5)      

            fig = plt.figure(figsize=(12, 12))
            info = plot_tracks.plot_fishing_panel(dfn.timestamp, dfn.lon,
                                     dfn.lat, is_fishing,
                                     plots = [
#                     {'label' : 'lon', 'values' : dfn.lon},
#                     {'label' : 'lat', 'values' : dfn.lat}, 
                    {'label' : 'speed (knots)', 'values' : medfilt(dfn.speed.values,11), 
                        'min_y' : 0},
                    {'label' : 'depth (km)', 'values' : -dfn.elevation_m / 1000,
                        'min_y' : 0, 'invert_yaxis' : True},                       
                                     ],
                                     map_ratio=6,
                                     annotations=7,
                                    annotation_y_shift=0.5)

            maps.add_scalebar(info.map_ax, info.extent)
            maps.add_figure_background(fig)

            plt.savefig('/Users/timothyhochberg/Desktop/test_fpanel.png', dpi=300,
                       facecolor=plt.rcParams['gfw.fig.background'])

            plt.show()
# -

hex(255 - int('9b', 16)) #7b7464

# +
reload()

ssvids = sorted(set(fishing_df.ssvid))[1:]

# TODO: figure out style for dark panel (use gfw.panel.background as color)
# See Juan Carlos's example in this post: 
# https://globalfishingwatch.slack.com/archives/CUW93UNLS/p1585062098015100
# (Obvious things: background, and line/tick colors)

edge_color = '#EEEEEE'  #'#7b7464'

with pyseas.context(pyseas.styles.dark):
    with pyseas.context({'gfw.fig.background' : pyseas.colors.dark.ocean,
#                          'xtick.color' : '#848b9b',
#                          'ytick.color' : '#848b9b',
                         'xtick.color' : edge_color,
                         'ytick.color' : edge_color,                       
                         'axes.edgecolor' :edge_color,
                        }):
        for ssvid in ssvids:

            dfn = fishing_df[fishing_df.ssvid == ssvid]
            dfn = dfn.sort_values(by='timestamp')
            is_fishing = (dfn.nnet_score > 0.5)      

            fig = plt.figure(figsize=(12, 12))
            info = plot_tracks.plot_fishing_panel(dfn.timestamp, dfn.lon,
                                     dfn.lat, is_fishing,
                                     plots = [
                    {'label' : 'lon', 'values' : dfn.lon},
                    {'label' : 'lat', 'values' : dfn.lat}, 
                    {'label' : 'speed (knots)', 'values' : medfilt(dfn.speed.values,11), 
                        'min_y' : 0},
                    {'label' : 'depth (km)', 'values' : -dfn.elevation_m / 1000,
                        'min_y' : 0, 'invert_yaxis' : True}, 
                                     ],
                                     map_ratio=6)

            maps.add_scalebar(info.map_ax, info.extent)
            maps.add_figure_background(fig)
            info.map_ax.outline_patch.set_edgecolor(plt.rcParams['axes.edgecolor'])

            plt.savefig('/Users/timothyhochberg/Desktop/test_fpanel.png', dpi=300,
                       facecolor=plt.rcParams['gfw.fig.background'])

            plt.show()
# -

extent
list(np.linspace(113.2, 114.2, 11))

    ax.gridlines(xlocs=xticks, ylocs=yticks, linewidth=0.4, zorder=0.5, alpha=0.5)        

# +
#         print(gl.xlocator.tick_values(*extent[:2]))
#         print(gl.ylocator.tick_values(*extent[2:]))

# +
import cartopy.mpl.gridliner


# TODO: allow side ticks drawn on to be set

def get_gridlocs(lim):
    return cartopy.mpl.gridliner.degree_locator.tick_values(*lim)
    
def add_gridlines(ax, zorder=0.5, **kwargs):
    if lons is None:
        lons = gl.xlocator.tick_values(*extent[:2])
    if lats is None:
        lats = gl.ylocator.tick_values(*extent[2:])
    for name in ['linewidth', 'linestyle', 'color', 'alpha']:
        if name not in kwargs:
            kwargs[name] = plt.rcParams['grid.' + name]
    return ax.gridlines(zorder=zorder, xlocs=lons, ylocs=lats, **kwargs)

def add_gridlabels(fig, ax, gl, lons=None, lats=None, **kwargs):
    extent = ax.get_extent(crs=maps.identity)
    if lons is None:
        lons = gl.xlocator.tick_values(*extent[:2])
    if lats is None:
        lats = gl.ylocator.tick_values(*extent[2:])
    fig.canvas.draw()
    ax.xaxis.set_major_formatter(ticks.LONGITUDE_FORMATTER) 
    ax.yaxis.set_major_formatter(ticks.LATITUDE_FORMATTER)
    ticks.lambert_xticks(ax, lons)
    ticks.lambert_yticks(ax, lats)


# -

reload()
df = df.sort_values(by='timestamp')
n =120
reload()
with pyseas.context(pyseas.styles.dark):
    fig = plt.figure(figsize=(9, 9), frameon=True)
    ax = maps.create_map(projection='regional.european_union')
    gl = maps.add_gridlines(ax, color='white', alpha=0.7)
    maps.add_raster(ax, img[::40, ::40])
    maps.add_gridlabels(ax, gl)
    maps.add_land(ax)
    maps.add_countries(ax)
    plt.savefig('/Users/timothyhochberg/Desktop/test_grids.png', dpi=300,
               facecolor=plt.rcParams['gfw.fig.background'])
    plt.show()


# +
reload()

ssvids = sorted(set(fishing_df.ssvid))[1:]

# TODO: figure out style for dark panel (use gfw.panel.background as color)
# See Juan Carlos's example in this post: 
# https://globalfishingwatch.slack.com/archives/CUW93UNLS/p1585062098015100
# (Obvious things: background, and line/tick colors)
with pyseas.context(pyseas.styles.light):
    with pyseas.context({'gfw.fig.background' : 'white',
                         'gfw.ocean.color' : 'white',
                          'gfw.fig.background' : 'white'}):
        for ssvid in ssvids:

            dfn = fishing_df[fishing_df.ssvid == ssvid]
            dfn = dfn.sort_values(by='timestamp')
            is_fishing = (dfn.nnet_score > 0.5)      

            fig = plt.figure(figsize=(12, 12))
            info = plot_tracks.plot_fishing_panel(dfn.timestamp, dfn.lon,
                                     dfn.lat, is_fishing,
                                     plots = [
#                     {'label' : 'lon', 'values' : dfn.lon},
#                     {'label' : 'lat', 'values' : dfn.lat}, 
                    {'label' : 'speed (knots)', 'values' : medfilt(dfn.speed.values,11), 
                        'min_y' : 0},
                    {'label' : 'depth (km)', 'values' : -dfn.elevation_m / 1000,
                        'min_y' : 0, 'invert_yaxis' : True},                       
                                     ],
                                     map_ratio=6,
                                     annotations=7,
                                    annotation_y_shift=0.5)

#             maps.add_scalebar(info.map_ax, info.extent)
            gl = maps.add_gridlines(info.map_ax)
            maps.add_gridlabels(info.map_ax, gl, lat_side='right', lon_side='top')
            maps.add_figure_background(fig)

            plt.savefig('/Users/timothyhochberg/Desktop/test_fpanel.png', dpi=300,
                       facecolor=plt.rcParams['gfw.fig.background'])

            plt.show()
# -


