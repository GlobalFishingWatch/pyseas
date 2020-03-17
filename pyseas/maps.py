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
from ._monkey_patch_cartopy import monkey_patch_cartopy
import matplotlib.pyplot as plt
import cartopy
import cartopy.feature as cfeature
import os
from . import colors
import geopandas as gpd
from cartopy.feature import ShapelyFeature
import shapely

monkey_patch_cartopy()

identity = cartopy.crs.PlateCarree()

root = os.path.dirname(os.path.dirname(__file__))

# Use this alias because we might want to rework context so we aren't abusing
# matplotlib's context in the future.

# TOOD: export these into projections moduls
# TODO: and generate class structure to hold them so
# TOOD: can do projections.global.default
# TODO: but keep projections._projection_info to query directly

projection_info = {
    # Need both "parameters" and carotpy_parameters to override
    'global.default' : dict (
            projection = cartopy.crs.EqualEarth,
            args = {'central_longitude' : 0},
            extent = None,
            name = 'EqualEarth @ 0°E'
        ),
    'global.atlantic_centered' : dict (
            projection = cartopy.crs.EqualEarth,
            args = {'central_longitude' : -40},
            extent = None,
            name = 'EqualEarth @ 40°W'
        ),
    'global.pacific_centered' : dict (
            projection = cartopy.crs.EqualEarth,
            args = {'central_longitude' : 150},
            extent = None,
            name = 'EqualEarth @ 150°E'
        ),

    'regional.north_pacific' : dict (
            projection = cartopy.crs.LambertAzimuthalEqualArea,
            args = {'central_longitude' : -165, 'central_latitude' : 25},
            extent = (-249, -71, 0, 50), 
            name = 'Lambert azimuthal equal area @ 165°E,25°N'
        ),
    'regional.south_pacific' : dict (
            projection = cartopy.crs.LambertAzimuthalEqualArea,
            args = {'central_longitude' : -140, 'central_latitude' : -40}, 
            extent = (-202, -62, -65, 15), 
            name = 'Lambert azimuthal equal area @ 140°W,0°S',
            # bad_land_polys = {(0, 4)} # Specific to natural earth version
        ),
    'regional.pacific' : dict(
            projection = cartopy.crs.LambertAzimuthalEqualArea,
            args = {'central_longitude' : -165},
            extent = (-249, -71, -50, 50),
            name = "Lambert azimuthal equal area @ 165°W,0°N"
        ),
    'regional.atlantic' : dict(
            projection = cartopy.crs.LambertAzimuthalEqualArea,
            args = {'central_longitude' : -30}, 
            extent = (-80, 20, -75, 75), 
            name = 'Lambert azimuthal equal area @ 30°W,0°S',
        ),
    'regional.north_atlantic' : dict(
            projection = cartopy.crs.LambertAzimuthalEqualArea,
            args = {'central_longitude' : -30, 'central_latitude' : 35}, 
            extent = (-80, 20, -5, 75), 
            name = 'Lambert azimuthal equal area @ 30°W,0°S',
        ),
    'regional.south_atlantic' : dict(
            projection = cartopy.crs.LambertAzimuthalEqualArea,
            args = {'central_longitude' : -20, 'central_latitude' : -35}, 
            extent = (-55, 15, -55, 5), 
            name = 'Lambert azimuthal equal area @ 30°W,0°S',
        ),
    'regional.indian' : dict(
            projection = cartopy.crs.LambertAzimuthalEqualArea,
            args = {'central_longitude' : 75},
            extent = (15, 145, -30, 15),
            name = "Lambert azimuthal equal area @ 75°E,0°N"
        ),
    'regional.european_union' : dict(
            projection = cartopy.crs.AlbersEqualArea,
            args = {'central_longitude' : 15, 'central_latitude' : 50},
            extent = (-20, 50, 25, 75),
            name = "Albers equal area conic @ 15°E,50°N"    
        ),

    'country.indonesia' : dict(
            projection = cartopy.crs.LambertCylindrical,
            args = {'central_longitude' : 120},
            extent = (80, 160, -15, 15),
            name = "Lambert cylindrical @ 120°E"
        ),
    'country.ecuador_with_galapagos' : dict(
            projection = cartopy.crs.LambertCylindrical,
            args = {'central_longitude' : -85},
            extent = (-97, -75, -7, 5),
            name = "Lambert cylindrical @ 85°W"
        ),
    'country.japan' : dict(
            projection = cartopy.crs.LambertAzimuthalEqualArea,
            args = {'central_longitude' : 137, 'central_latitude' : 38},
            extent = (126, 148, 23, 53),
            name = "Lambert azimuthal equal area @ 137°E,38°N",
            hspace = 0.2
        ),
    'country.chile' : dict(
            projection = cartopy.crs.LambertAzimuthalEqualArea,
            args = {'central_longitude' : -80, 'central_latitude' : -35},
            extent = (-100, -60, -60, -10),
            name = "Lambert azimuthal equal area @ 80°W",
            hspace = 0.2
        ),
    'country.peru' : dict(
            projection = cartopy.crs.LambertAzimuthalEqualArea,
            args = {'central_longitude' : -80},
            extent = (-93, -67, -20, 2),
            name = "Lambert azimuthal equal area @ 80°W",
            hspace = 0.2
        ),
    'country.panama' : dict(
            projection = cartopy.crs.LambertAzimuthalEqualArea,
            args = {'central_longitude' : -80},
            extent = (-93, -67, -4, 21),
            name = "Lambert azimuthal equal area @ 80°W",
            hspace = 0.2
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

def get_proj_description(region_name):
    # TODO: add warning (add flag so can disable when called through files that know better)
    # when in `regional_pacific` and `regional.north_pacific` regions (many any regions with
    # Overridden vales)
    return projection_info[region_name]['name']


def add_land(ax, projection=None, scale='10m', edgecolor=None, facecolor=None, linewidth=None, **kwargs):
    """Add land to an existing map

    Parameters
    ----------
    ax : matplotlib axes object
    projection: str
        If projection is specified, try to remove problematic land polygons
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
    # geometries = list(land.geometries())
    # if isinstance(projection, str):
    #     bad_polys = projection_info[projection].get('bad_land_polys', ())
    #     if bad_polys:
    #         new_geometries = []
    #         for i, geom in enumerate(geometries):
    #             if (i,) not in bad_polys:
    #                 if geom.type == 'MultiPolygon':
    #                     polys = []
    #                     for j, p in enumerate(geom.geoms):
    #                         if (i, j) not in bad_polys:
    #                             polys.append(p)
    #                     new_geometries.append(shapely.geometry.MultiPolygon(polys))
    #                 else:
    #                     new_geometries.append(geom)
    #         geometries = new_geometries

    # region = ShapelyFeature(geometries, crs=cartopy.crs.PlateCarree(),
    #                                         edgecolor=edgecolor,
    #                                         facecolor=facecolor,
    #                                         linewidth=linewidth,
    #                                         **kwargs)
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
    if 'cmap' in kwargs and isinstance(kwargs['cmap'], str):
        src = plt.rcParams['gfw.map.cmapsrc']
        try:
            kwargs['cmap'] = getattr(src, kwargs['cmap'])
        except AttributeError:
            pass
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
                hide_axes=True,
                show_xform=True):
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
    if isinstance(projection, str):
        proj_name = projection
        if extent is None:
            extent = get_extent(proj_name)
        projection = get_projection(proj_name)
    else:
        proj_name = None


    bg_color = bg_color or plt.rcParams.get('gfw.ocean.color', colors.dark.ocean)
    if not isinstance(subplot, tuple):
        # Allow grridspec to be passed through
        subplot = (subplot,)
    ax = plt.subplot(*subplot, projection=projection)
    ax.background_patch.set_facecolor(bg_color)
    if extent is not None:
        ax.set_extent(extent, crs=identity)
    if hide_axes:
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
    if show_xform and proj_name:
        ax.text(0.0, -0.01, get_proj_description(proj_name), fontsize=9,
            horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
    return ax



def plot_raster_w_colorbar(raster, label='', loc='top',
                projection='global.default', hspace=None, wspace=0.016,
                bg_color=None, hide_axes=True, cbformat=None, **kwargs):
    assert loc in ('top', 'bottom')
    if hspace is None:
        hspace = 0.12
        if isinstance(projection, str):
            hspace = projection_info[projection].get('hspace', hspace)
    if loc == 'top':
        hratios = [.015, 1]
        cb_ind, pl_ind = 0, 1
        anchor = 'NE'
    else:
        hratios = [1, 0.015]
        cb_ind, pl_ind = 1, 0
        anchor = 'SE'
        hspace -= 0.10



    gs = plt.GridSpec(2, 3, height_ratios=hratios, hspace=hspace, wspace=wspace)
    ax, im = plot_raster(raster, gs[pl_ind, :], projection=projection, **kwargs)
    ax.set_anchor(anchor)
    cb_ax = plt.subplot(gs[cb_ind, 2])
    cb = plt.colorbar(im, cb_ax, orientation='horizontal', shrink=0.8, format=cbformat)
    leg_ax = plt.subplot(gs[cb_ind, 1], frame_on=False)
    leg_ax.axes.get_xaxis().set_visible(False)
    leg_ax.axes.get_yaxis().set_visible(False)
    leg_ax.text(1, 0.5, label, fontdict={'fontsize': 12}, # TODO: stule
                    horizontalalignment='right', verticalalignment='center')
    return ax, im, cb



def plot_raster(raster, subplot=(1, 1, 1), projection='global.default',
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
    add_land(ax, projection)
    return  ax, im
