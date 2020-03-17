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
import pyseas as pyseas, pyseas as pycs
import imp

import shapely.geometry as sgeom
from shapely.prepared import prep

# def _rings_to_multi_polygon(self, rings, is_ccw):
#         exterior_rings = []
#         interior_rings = []
#         for ring in rings:
#             if ring.is_ccw != is_ccw:
#                 interior_rings.append(ring)
#             else:
#                 exterior_rings.append(ring)

#         polygon_bits = []

#         # Turn all the exterior rings into polygon definitions,
#         # "slurping up" any interior rings they contain.
#         for exterior_ring in exterior_rings:
#             polygon = sgeom.Polygon(exterior_ring)
#             prep_polygon = prep(polygon)
#             holes = []
#             for interior_ring in interior_rings[:]:
#                 if prep_polygon.contains(interior_ring):
#                     holes.append(interior_ring)
#                     interior_rings.remove(interior_ring)
#                 elif polygon.crosses(interior_ring):
#                     # Likely that we have an invalid geometry such as
#                     # that from #509 or #537.
#                     holes.append(interior_ring)
#                     interior_rings.remove(interior_ring)
#             polygon_bits.append((exterior_ring.coords,
#                                  [ring.coords for ring in holes]))

#         # # Any left over "interior" rings need "inverting" with respect
#         # # to the boundary.
#         # if interior_rings:
#         #     boundary_poly = self.domain
#         #     x3, y3, x4, y4 = boundary_poly.bounds
#         #     bx = (x4 - x3) * 0.1
#         #     by = (y4 - y3) * 0.1
#         #     x3 -= bx
#         #     y3 -= by
#         #     x4 += bx
#         #     y4 += by
#         #     for ring in interior_rings:
#         #         # Use shapely buffer in an attempt to fix invalid geometries
#         #         polygon = sgeom.Polygon(ring).buffer(0)
#         #         if not polygon.is_empty and polygon.is_valid:
#         #             x1, y1, x2, y2 = polygon.bounds
#         #             bx = (x2 - x1) * 0.1
#         #             by = (y2 - y1) * 0.1
#         #             x1 -= bx
#         #             y1 -= by
#         #             x2 += bx
#         #             y2 += by
#         #             box = sgeom.box(min(x1, x3), min(y1, y3),
#         #                             max(x2, x4), max(y2, y4))

#         #             # Invert the polygon
#         #             polygon = box.difference(polygon)

#         #             # Intersect the inverted polygon with the boundary
#         #             polygon = boundary_poly.intersection(polygon)

#         #             if not polygon.is_empty:
#         #                 polygon_bits.append(polygon)

#         if polygon_bits:
#             multi_poly = sgeom.MultiPolygon(polygon_bits)
#         else:
#             multi_poly = sgeom.MultiPolygon()
#         return multi_poly
from pyseas._monkey_patch_cartopy import monkey_patch_cartopy


def reload():
    imp.reload(cartopy.crs)
    monkey_patch_cartopy()
#     cartopy.crs.Projection._rings_to_multi_polygon = _rings_to_multi_polygon
    imp.reload(cm)
    imp.reload(pycs.colors)
    imp.reload(styles)
    imp.reload(maps)
    imp.reload(plot_tracks)
    imp.reload(rasters)
    imp.reload(pycs)
reload()

# %matplotlib inline

# +
# conda upgrade --channel conda-forge cartopy
# -

# ## Global Raster Plots

# !gsutil cp -n gs://machine-learning-dev-ttl-120d/named-achorages01-raster.tiff ../untracked/
img = skimage.io.imread("../untracked/named-achorages01-raster.tiff")

# ### Global map centered over the Pacific using Dark Style

reload()
with pyseas.context(styles.dark):
    fig = plt.figure(figsize=(18, 6))
    ax, im = maps.plot_raster(img[::10, ::10],
                                   projection='global.pacific_centered', 
                                   cmap='presence')
    maps.add_eezs(ax)

# ## Simple, Manual Colorbar

with pycs.context(styles.dark):
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
with pycs.context(styles.dark):
    fig = plt.figure(figsize=(12,7))
    maps.plot_raster_w_colorbar(img[::40, ::40], 
                                "distance to shore (km)", 
                                cmap='fishing')

reload()
with pycs.context(styles.dark):
    fig = plt.figure(figsize=(12, 8))
    ax, im, cb = maps.plot_raster_w_colorbar(img[::40, ::40], 
                                             "distance to shore (km)", 
                                             loc="top",
                                             projection='regional.north_pacific', 
                                             cmap='fishing')

# ## Adding Gridlines

reload()
with pycs.context(styles.dark):
    fig = plt.figure(figsize=(12, 8))
    ax, im, cb = maps.plot_raster_w_colorbar(img[::40, ::40], 
                                             "distance to shore (km)", 
                                             loc="top",
                                             projection='regional.north_pacific', 
                                             cmap='fishing')
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
    with pycs.context(style):
        fig = plt.figure(figsize=(10, 5))
        ax = maps.create_map(projection='regional.north_pacific')
        maps.add_plot(ax, df.lon, df.lat, 'g.', transform=maps.identity)
        maps.add_land(ax)
        maps.add_eezs(ax)
        plt.show()
# -

# ## Predefined Regional Styles

reload()
with pycs.context(styles.light):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='regional.pacific')
    maps.add_land(ax)
    maps.add_countries(ax)
    plt.show()

reload()
with pycs.context(styles.light):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='regional.south_pacific')
    maps.add_land(ax)
    maps.add_countries(ax)
    plt.show()

reload()
with pycs.context(styles.light):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='country.chile')
    maps.add_land(ax)
    maps.add_countries(ax)
    plt.show()

reload()
with pycs.context(styles.dark):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='regional.south_pacific')
    maps.add_land(ax, 'regional.south_pacific')
    maps.add_countries(ax)
    plt.show()

reload()
with pycs.context(styles.light):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='country.ecuador_with_galapagos')
    maps.add_land(ax)
    maps.add_countries(ax)
    plt.show()

reload()
with pycs.context(styles.dark):
    fig = plt.figure(figsize=(10, 10))
    ax = maps.create_map(projection='country.indonesia')
    maps.add_land(ax)
    maps.add_countries(ax)
    plt.show()

# ## `contrib`

# ### Plot Tracks and Lat/Lon vs Time

df = msgs[(msgs.ssvid == "413461490")]
reload()
with pycs.context(styles.dark):
    fig = plt.figure(figsize=(10, 5))
    ts = [pd.Timestamp(x).to_pydatetime() for x in df.timestamp]
    ax1, ax2, ax3 = plot_tracks.plot_tracks_panel(ts, df.lon, df.lat)

# ## Publish

rendered.publish_to_github('./Examples.ipynb', 
                           'pyseas/doc', action='push')

# ## Below this point is messy

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
raster = rasters.df2raster(df_presence, 'lon_bin', 'lat_bin', 'hours', xyscale=10, per_km2=True)

reload()
fig = plt.figure(figsize=(10, 10))
norm = mpcolors.LogNorm(vmin=0.01, vmax=100)
with pycs.context(styles.dark):
    projection = cartopy.crs.EqualEarth(central_longitude=-165)
    ax, im, cb = pycs.maps.plot_raster_w_colorbar(raster, 
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
with pycs.context(styles.dark):
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
raster2 = pycs.rasters.df2raster(df_presence, 'lon_bin', 'lat_bin', 'hours', 
                                 xyscale=10, origin='lower', per_km2=True)

reload()
plt.rc('text', usetex=False)
fig = plt.figure(figsize=(14, 10))
norm = mpcolors.LogNorm(vmin=0.01, vmax=1)
with plt.rc_context(styles.light):
    ax, im, cb = maps.plot_raster_w_colorbar(raster2, 
                                       "hours of presence per km2
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

grid_fishing_presence  = pycs.rasters.df2raster(df_fishing, 'lon_bin', 'lat_bin', 'hours', xyscale=4,
                                              extent = [min_lon, max_lon, min_lat, max_lat],
                                                per_km2=True, scale=60)

with plt.rc_context(pycs.styles.dark): 
    fig_min_value = 1
    fig_max_value = 100
    norm = mpcolors.LogNorm(vmin=fig_min_value, vmax=fig_max_value)
    fig = plt.figure(figsize=(10, 10))
    ax, im, colorbar = pycs.maps.plot_raster_w_colorbar(
                            grid_fishing_presence,
                            "seconds per square km",   
                            cmap='presence',
                            loc='bottom',  
                            extent = [min_lon + 0.01, max_lon, min_lat, max_lat],
                            norm = norm, 
                            projection='regional.indian')
    pycs.maps.add_eezs(ax)
    pycs.maps.add_countries(ax)
    ax.set_extent((15, 145, -30, 15), crs=maps.identity)
    ax.set_title("Fishing Vessel Presence in the Indian Ocean overlaid with Study Area")
#     ax.add_geometries([overpasses], crs = ccrs.PlateCarree(),
#                   alpha=1, facecolor='none', edgecolor='red') # for Lat/Lon data.
    
# -





import cartopy.feature as cfeature
land = cfeature.NaturalEarthFeature('physical', 'land', scale='10m')

geometries = list(land.geometries())

for i, geom in enumerate(geometries):
    print(i, geom.geom_type)
    if geom.geom_type == 'Polygon':
        for k, x in enumerate(geom.interiors):
            if x.is_ccw != geom.exterio.is_ccw:
                print(i, k)
    else:
        for j, poly in enumerate(geom):
            for k, x in enumerate(poly.interiors):
                if x.is_ccw != poly.exterior.is_ccw:
                    print(i, j, k)

with pysea
fig = plt.figure(figsize=(12, 8))
ts = [pd.Timestamp(x).to_pydatetime() for x in df.timestamp]
ax1, ax2, ax3 = plot_tracks.plot_tracks_panel(ts, df.lon, df.lat, df['ssvid'] )
fig.suptitle(df['ssvid'].iloc[0] + ' - tracks ' , y=0.93)    #+ new_msgs.iloc[0].which
plt.show()
                  
