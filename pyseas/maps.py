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



projection_info = {
    # Need both "parameters" and carotpy_parameters to override
    'global.default' : dict (
            projection = cartopy.crs.EqualEarth,
            args = {'central_longitude' : 0},
            extent = None
        ),
    'global.atlantic_centered' : dict (
            projection = cartopy.crs.EqualEarth,
            args = {'central_longitude' : -40},
            extent = None
        ),
    'global.pacific_centered' : dict (
            projection = cartopy.crs.EqualEarth,
            args = {'central_longitude' : 150},
            extent = None
        ),

    'regional.north_pacific' : dict (
            projection = cartopy.crs.LambertAzimuthalEqualArea,
            args = {'central_longitude' : -165, 'central_latitude' : 25},
            extent = (-249, -71, 0, 3.3) # Update me
        ),
    'regional.pacific' : dict(
            projection = cartopy.crs.LambertAzimuthalEqualArea,
            args = {'central_longitude' : -165},
            extent = (-249, -71, -3.3, 3.3)
        ),
    'regional.indian' : dict(
            projection = cartopy.crs.LambertAzimuthalEqualArea,
            args = {'central_longitude' : 75},
            extent = (15, 145, -30, 15)
        ),

    'country.indonesia' : dict(
            projection = cartopy.crs.LambertCylindrical,
            args = {'central_longitude' : 120},
            extent = (80, 160, -15, 15)
        ),
    'country.ecuador_with_galapagos' : dict(
            projection = cartopy.crs.LambertCylindrical,
            args = {'central_longitude' : -85},
            extent = (-97, -75, -7, 5)
        ),
}


def get_projection(region_name):
    info = projection_info[region_name]
    return info['projection'](**info['args'])

def get_extent(region_name):
    # TODO: add warning (add flag so can disable when called through files that know better)
    # when in `regional_pacific` and `regional.north_pacific` regions (many any regions with
    # Overridden vales)
    return projection_info[region_name]['extent']



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


def add_figure_background(fig, color=None):
    """Set the figure background (area around plot)

    Parameters
    ----------
    fig : Figure
    color : tuple or str, optional


    """
    color = color or plt.rcParams.get('gfw.fig.background', colors.dark.background)
    fig.patch.set_facecolor('#f7f7f7')

def create_map(subplot=(1, 1, 1), 
                projection='global.default', extent=None,
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



def plot_raster_w_colorbar(raster, label='', loc='top',
                projection=cartopy.crs.EqualEarth(), hspace=0.12,
                bg_color=None, hide_axes=True, **kwargs):
    assert loc in ('top', 'bottom')
    if loc == 'top':
        hratios = [.015, 1]
        cb_ind, pl_ind = 0, 1
        anchor = 'NE'
    else:
        hratios = [1, 0.015]
        cb_ind, pl_ind = 1, 0
        anchor = 'SE'
        hspace -= 0.06

    gs = plt.GridSpec(2, 3, height_ratios=hratios, hspace=hspace, wspace=0.015)
    ax, im = plot_raster(raster, gs[pl_ind, :], projection=projection, **kwargs)
    ax.set_anchor(anchor)
    cb_ax = plt.subplot(gs[cb_ind, 2])
    cb = plt.colorbar(im, cb_ax, orientation='horizontal', shrink=0.8)
    leg_ax = plt.subplot(gs[cb_ind, 1], frame_on=False)
    leg_ax.axes.get_xaxis().set_visible(False)
    leg_ax.axes.get_yaxis().set_visible(False)
    _ = leg_ax.text(1, 0.5, label, fontdict={'fontsize': 12}, # TODO: stule
                    horizontalalignment='right', verticalalignment='center')
    return ax, im, cb 



def plot_raster(raster, subplot=(1, 1, 1), projection=cartopy.crs.EqualEarth(),
                bg_color=None, hide_axes=True, colorbar=None, 
                gridlines=False, **kwargs):
    """Draw a GFW themed map over a raster

    Parameters
    ----------
    raster : 2D array
    subplot : tuple or GridSpec
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
    extent = kwargs.get('extent')
    ax = create_map(subplot, projection, extent, bg_color, hide_axes)
    im = add_raster(ax, raster, **kwargs)
    add_land(ax)
    return  ax, im
