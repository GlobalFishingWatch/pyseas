import matplotlib.pyplot as plt
import cartopy
import cartopy.feature as cfeature


land_fill = '#374a6d'
land_color = '#0A1738'

def add_land(ax, scale='10m', edgecolor=color, facecolor=fill):
    land = cfeature.NaturalEarthFeature('physical', 'land', scale,
                                            edgecolor=edgecolor,
                                            facecolor=edgecolor)
    return ax.add_feature(land)

def add_raster(ax, raster, extent=(-180, 180, -90, 90), origin='upper', **kwargs):
    return ax.imshow(raster, transform=cartopy.crs.PlateCarree(), 
                        extent=extent, origin=origin, **kwargs)

def add_plot(ax, *args, **kwargs):
    if 'transform' not in kwargs:
        kwargs['transform'] = cartopy.crs.PlateCarree()
    ax.plot(*args,  **kwargs)

def create_map(projection=cartopy.crs.EqualEarth(), hide_axes=True):
    """Draw a GFW themed world map


    """
    ax = plt.axes(projection=projection)
    if hide_axes:
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
    return ax



def plot_raster(raster, projection=cartopy.crs.EqualEarth(), hide_axes=True, **kwargs):
    ax = create_map(projection, hide_axes)
    im = add_raster(ax, raster, **kwargs)
    add_land(ax)
    return  ax, im

