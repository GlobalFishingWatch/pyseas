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

# !cp ~/Desktop/named-achorages01-raster.tiff untracked

# +
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs
import skimage.io
import cmocean
import rendered

from pyseas import maps, colors, cm, styles
import imp
imp.reload(colors)
imp.reload(styles)
imp.reload(maps)
imp.reload(cm)

# %matplotlib inline
# -

# ## Global Raster Plots

# !gsutil cp -n gs://machine-learning-dev-ttl-120d/named-achorages01-raster.tiff ../untracked/
img = skimage.io.imread("../untracked/named-achorages01-raster.tiff")

# ### Global map using a custom colormap.

fig = plt.figure(figsize=(18, 6))
_ = maps.plot_raster(img[::10, ::10], cmap=cm.reception)

# ### Global map centered over the Pacific

fig = plt.figure(figsize=(18, 6))
projection = cartopy.crs.EqualEarth(central_longitude=-160)
ax, im = maps.plot_raster(img[::10, ::10], projection=projection)

# ### Global Map with a Colorbar

fig = plt.figure(figsize=(18, 6))
ax, im = maps.plot_raster(img[::10, ::10])
cb = fig.colorbar(im, orientation='vertical', shrink=0.8, pad=0.02, 
                  label='distance to shore (km)')

# ## Use a context manager to switch to light style

with plt.rc_context(styles.light):
    fig = plt.figure(figsize=(18, 6))
    ax, im = maps.plot_raster(img[::10, ::10], cmap=cm.presence)

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

df = msgs[(msgs.ssvid == "220413000")]
for style in [styles.light, styles.dark]:
    with plt.rc_context(style):
        fig = plt.figure(figsize=(10, 5))
        projection = cartopy.crs.PlateCarree(central_longitude=200)
        ax = maps.create_map(projection=projection)
        maps.add_plot(ax, df.lon, df.lat, 'g.', transform=maps.identity)
        maps.add_land(ax)
        ax.set_extent((110, 250, 0, 90))
        plt.show()

rendered.publish_to_github('./Examples.ipynb', 
                           'pyseas/doc', action='push')
