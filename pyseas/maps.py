"""Plotting routines for GFW 




"""

import matplotlib.pyplot as plt
import cartopy
import cartopy.feature as cfeature


land_fill = '#374a6d'
land_color = '#0A1738'

def add_land(ax, scale='10m', edgecolor=land_color, facecolor=land_fill, **kwargs):
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
                                            facecolor=edgecolor,
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
    return ax.imshow(raster, transform=cartopy.crs.PlateCarree(), 
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
        kwargs['transform'] = cartopy.crs.PlateCarree()
    ax.plot(*args,  **kwargs)


def create_map(projection=cartopy.crs.EqualEarth(), hide_axes=True):
    """Draw a GFW themed map

    Parameters
    ----------
    projection : cartopy.crs.Projection, optional
    hide_axes : bool, optional
        if `true`, hide x and y axes
    
    Returns
    -------
    GeoAxes
    """
    ax = plt.axes(projection=projection)
    if hide_axes:
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
    return ax



def plot_raster(raster, projection=cartopy.crs.EqualEarth(), hide_axes=True, **kwargs):
    """Draw a GFW themed map over a raster

    Parameters
    ----------
    raster : 2D array
    projection : cartopy.crs.Projection, optional
    hide_axes : bool
        if `true`, hide x and y axes
    
    Other Parameters
    ----------------
    Keyword args are passed on to add_raster.

    Returns
    -------
    (GeoAxes, AxesImage)
    """
    ax = create_map(projection, hide_axes)
    im = add_raster(ax, raster, **kwargs)
    add_land(ax)
    return  ax, im

