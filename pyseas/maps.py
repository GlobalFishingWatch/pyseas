"""Plotting routines for GFW 


Examples
--------

Plot a world raster with a custom colormap

    _ = maps.plot_raster(img, cmap=pyseas.cm.reception)


Plot a world raster with the map centered over the pacific
(Note that the raster is still assumed to extend from -180 to 180)

    projection = cartopy.crs.EqualEarth(central_longitude=180)
    _ = maps.plot_raster(img, projection=projection)


Add a `colorbar` to a raster plot

    ax, im = maps.plot_raster(img)
    cb = fig.colorbar(im, orientation='vertical', shrink=0.8)


See also `contrib.plot_tracks` for examples of using `add_plot`

"""
import matplotlib.pyplot as plt
import cartopy
import cartopy.feature as cfeature
from . import colors

identity = cartopy.crs.PlateCarree()


def add_land(ax, scale='10m', edgecolor=colors.dark.border, facecolor=colors.dark.land, **kwargs):
    """Add land to an existing map

    Parameters
    ----------
    ax : matplotlib axes object
    scale : str, optional
        Resolution of NaturalEarth data to use ('10m’, ‘50m’, or ‘110m').
    edgecolor : str or tuple, optional
        Color to use for the landmass edges.
    facecolor : str or tuple, optional
        Color to use for the landmass faces.
    
    Other Parameters
    ----------------
    Keyword args are passed on to NaturalEarthFeature.

    Returns
    -------
    FeatureArtist
    """
    land = cfeature.NaturalEarthFeature('physical', 'land', scale,
                                            edgecolor=edgecolor,
                                            facecolor=facecolor,
                                            **kwargs)
    return ax.add_feature(land)


def add_raster(ax, raster, extent=(-180, 180, -90, 90), origin='upper', **kwargs):
    """Add a raster to an existing map

    Parameters
    ----------
    ax : matplotlib axes object
    raster : 2D array
    extent : tuple of int, optional
        (lon_min, lon_max, lat_min, lat_max) of the raster
    origin : str, optional
        Location of the raster origin ['upper' or 'lowers']
    
    Other Parameters
    ----------------
    Keyword args are passed on to imshow.

    Returns
    -------
    AxesImage
    """
    return ax.imshow(raster, transform=identity, 
                        extent=extent, origin=origin, **kwargs)


def add_plot(ax, *args, **kwargs):
    """Add a plot to an existing map

    Parameters
    ----------
    ax : matplotlib axes object
    
    Other Parameters
    ----------------
    Keyword args are passed on to ax.plot.

    This function hides the need to specify the transform in the common
    case. Unless the transform is specified it defaults to PlateCarree,
    which is generally what you want.

    Returns
    -------
    A list of Line2D objects.
    """
    if 'transform' not in kwargs:
        kwargs['transform'] = identity
    ax.plot(*args,  **kwargs)


def create_map(subplot=(1, 1, 1), projection=cartopy.crs.EqualEarth(), 
               bg_color=colors.dark.ocean, hide_axes=True):
    """Draw a GFW themed map

    Parameters
    ----------
    subplot : tuple or GridSpec
    projection : cartopy.crs.Projection, optional
    bg_color : str or tuple, optional
    hide_axes : bool, optional
        if `true`, hide x and y axes
    
    Returns
    -------
    GeoAxes
    """
    if not isinstance(subplot, tuple):
        # Allow grridspec to be passed through
        subplot = (subplot,)
    ax = plt.subplot(*subplot, projection=projection)
    ax.background_patch.set_facecolor(bg_color)

    if hide_axes:
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
    return ax



def plot_raster(raster, subplot=(1, 1, 1), projection=cartopy.crs.EqualEarth(),
                bg_color=colors.dark.ocean, hide_axes=True, **kwargs):
    """Draw a GFW themed map over a raster

    Parameters
    ----------
    raster : 2D array
    projection : cartopy.crs.Projection, optional
    bg_color : str or tuple, optional
    hide_axes : bool
        if `true`, hide x and y axes
    
    Other Parameters
    ----------------
    Keyword args are passed on to add_raster.

    Returns
    -------
    (GeoAxes, AxesImage)
    """
    ax = create_map(subplot, projection, bg_color, hide_axes)
    im = add_raster(ax, raster, **kwargs)
    add_land(ax)
    return  ax, im

