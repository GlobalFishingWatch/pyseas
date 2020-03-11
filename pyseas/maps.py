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
import os
from . import colors
import geopandas as gpd

identity = cartopy.crs.PlateCarree()

root = os.path.dirname(os.path.dirname(__file__))



regional_projections = {
    'pacific' : dict(
            projection = cartopy.crs.EqualEarth,
            args = {'central_longitude' : -165},
            extent = (-249, -71, -3.3, 3.3)
        )
}


def get_projection(region_name):
    info = regional_projections[region_name]
    return info['projection'](**info['args'])

def get_extent(region_name):
    return regions[region_name]['extent']



def add_land(ax, scale='10m', edgecolor=None, facecolor=None, linewidth=None, **kwargs):
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
    linewidth : float, optional
        Width of land edge in points
    
    Other Parameters
    ----------------
    Keyword args are passed on to NaturalEarthFeature.

    Returns
    -------
    FeatureArtist
    """
    edgecolor = edgecolor or plt.rcParams.get('gfw.border.color', colors.dark.border)
    facecolor = facecolor or plt.rcParams.get('gfw.land.color', colors.dark.land)
    linewidth = linewidth or plt.rcParams.get('gfw.border.linewidth', 0.4)
    land = cfeature.NaturalEarthFeature('physical', 'land', scale,
                                            edgecolor=edgecolor,
                                            facecolor=facecolor,
                                            linewidth=linewidth,
                                            **kwargs)
    return ax.add_feature(land)

def add_countries(ax, scale='10m', edgecolor=None, facecolor=None, linewidth=None, **kwargs):
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
    linewidth : float, optional
        Width of land edge in points
    
    Other Parameters
    ----------------
    Keyword args are passed on to NaturalEarthFeature.

    Returns
    -------
    FeatureArtist
    """
    edgecolor = edgecolor or plt.rcParams.get('gfw.border.color', colors.dark.border)
    facecolor = facecolor or plt.rcParams.get('gfw.land.color', colors.dark.land)
    linewidth = linewidth or plt.rcParams.get('gfw.border.linewidth', 0.4)
    land = cfeature.NaturalEarthFeature('cultural', 'admin_0_boundary_lines_land', scale,
                                            edgecolor=edgecolor,
                                            facecolor=facecolor,
                                            linewidth=linewidth,
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


_eezs = {}

def add_eezs(ax, use_boundaries=True, facecolor='none', edgecolor=None, linewidth=None, alpha=1):
    """Add EEZs to an existing map

    Parameters
    ----------
    ax : matplotlib axes object
    use_boundaries : bool, optional
        use the boundaries version of EEZs which is smaller and faster, but not as detailed.
    facecolor : str, optional
    edgecolor: str or tuple, optional
        Can be styled with 'gfw.eez.bordercolor'
    linewidth: float, optional
        Can be styled with 'gfw.eez.linewidth'
    alpha: float, optional


    Returns
    -------
    FeatureArtist
    """
    if use_boundaries:
        path = os.path.join(root, 'untracked/data/eez_boundaries_v11.gpkg')
    else:
        path = os.path.join(root, 'untracked/data/eez_v11.gpkg')
    if path not in _eezs:
        try:
            _eezs[path] = gpd.read_file(path)
        except FileNotFoundError:
            raise FileNotFoundError('Eezs must be installed into the `untracked/data/` directory')

    eezs = _eezs[path]
    edgecolor = edgecolor or plt.rcParams.get('gfw.eez.bordercolor', colors.dark.eez)
    linewidth = linewidth or plt.rcParams.get('gfw.eez.linewidth', 0.4)

    return ax.add_geometries(eezs.geometry, crs=identity,
                  alpha=alpha, facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth)


def create_map(subplot=(1, 1, 1), 
                projection=None, extent=None,
                bg_color=None, 
                hide_axes=True):
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
    if projection is None:
        # TODO: maybe just theme default projection
        central_longitude = plt.rcParams.get('gfw.eez.centrallongitude', 0)
        projection = cartopy.crs.EqualEarth(central_longitude=central_longitude)
    elif isinstance(projection, str):
        if extent is None:
            extent = get_extent(projection)
        projection = get_projection(projection)


    bg_color = bg_color or plt.rcParams.get('gfw.ocean.color', colors.dark.ocean)
    if not isinstance(subplot, tuple):
        # Allow grridspec to be passed through
        subplot = (subplot,)
    ax = plt.subplot(*subplot, projection=projection)
    ax.background_patch.set_facecolor(bg_color)
    if extent is not None:
        ax.set_extent(extent)
    if hide_axes:
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
    return ax



def plot_raster(raster, subplot=(1, 1, 1), projection=cartopy.crs.EqualEarth(),
                bg_color=None, hide_axes=True, **kwargs):
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

