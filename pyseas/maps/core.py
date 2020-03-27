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
import cartopy.mpl.gridliner
import json
import os
from .. import colors
import geopandas as gpd
import numpy as np
from cartopy.feature import ShapelyFeature
import shapely
from shapely.geometry import MultiLineString
from . import ticks


monkey_patch_cartopy()

identity = cartopy.crs.PlateCarree()

root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Use this alias because we might want to rework context so we aren't abusing
# matplotlib's context in the future.


# TOOD: export these into projections moduls
# TODO: and generate class structure to hold them so
# TOOD: can do projections.global.default
# TODO: but keep projections.projection_info to query directly

_projections = {
    'EqualEarth' : cartopy.crs.EqualEarth,
    'LambertAzimuthalEqualArea' : cartopy.crs.LambertAzimuthalEqualArea,
    'AlbersEqualArea' : cartopy.crs.AlbersEqualArea,
    'LambertCylindrical' : cartopy.crs.LambertCylindrical,
}

def load_projections():

    path = os.path.join(root, 'data/projection_info.json')
    with open(path) as f:
        info = json.load(f)
    for k, v in info.items():
        v['projection'] = _projections[v['projection']]
        info[k] = v
    return info

projection_info = load_projections()


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



def _build_multiline_string_coords(x, y, mask, break_on_change, x_is_lon=True):
    assert len(x) == len(y) == len(mask) , (len(x),  len(y), len(mask))
    i = 0
    ml_coords = []
    last_x = None
    crds = []
    while i < len(mask):

        while i < len(mask) and not mask[i]:
            i += 1

        if last_x is None:
            last_x = x[i]

        while (i < len(mask)) and mask[i]:
            if x_is_lon:
                if abs(x[i] - last_x) > 180:
                    ml_coords.append(crds)
                    crds = []
            crds.append((x[i], y[i]))
            last_x = x[i]
            i += 1

        if break_on_change:
            ml_coords.append(crds)
            crds = []


    ml_coords.append(crds)

    ml_coords = [x for x in ml_coords if len(x) > 1]
    return ml_coords
        

def add_plot(ax, lon, lat, kind=None, props=None, break_on_change=False, *args, **kwargs):
    """Add a plot to an existing map

    Parameters
    ----------
    ax : matplotlib axes object
    lon : sequence of float
    lat : sequence of float
    kind : sequence of hashable, optional
        Length must match lon/lat and values are used to index into the
        `props` map.
    props : dict, optional.
        Maps `kind` of first and last point of each segment to plot style.
         By default, sorted values from `kind`
        are mapped to 'axes.prop_cycle'. `props` for segments between 
        points with different `kind` value are looked up under `None`.
        If `None` is missing, these points are not plotted.
    
    Other Parameters
    ----------------
    Keyword args are passed on to ax.plot.

    TODO: more detail

    This function hides the need to specify the transform in the common
    case. Unless the transform is specified it defaults to PlateCarree,
    which is generally what you want.

    Returns
    -------
    A list of Line2D objects.
    """
    assert len(lon) == len(lat)
    if 'transform' not in kwargs:
        kwargs['transform'] = identity
    if kind is None:
        kind = np.ones(len(lon))
    else:
        kind = np.asarray(kind)
        assert len(kind) == len(lon)

    if props is None:
        raw_kinds = sorted(set(kind))
        props = {(k, k) : v for (k, v) in zip(raw_kinds, plt.rcParams['gfw.map.trackprops'])}
    kinds = list(props.keys())

    for k1, k2 in kinds:
        if (k1, k2) not in props:
            continue
        mask1 = (kind == k1)
        if k2 == k1:
            mask2 = mask1
        else:
            mask2 = (kind == k2)

        mask = np.zeros_like(mask1)
        mask[:-1] = mask1[:-1] & mask2[1:]
        mask[1:] |= mask1[:-1] & mask2[1:]

        if mask.sum():
            ml_coords = _build_multiline_string_coords(lon, lat, mask, break_on_change)   
            mls = MultiLineString(ml_coords)
            ax.add_geometries([mls], crs=identity, **props[k1, k2])


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
    fig.patch.set_facecolor(color)

# TODO: allow side ticks drawn on to be set

def add_gridlines(ax, zorder=0.5, **kwargs):
    for name in ['linewidth', 'linestyle', 'color', 'alpha']:
        if name not in kwargs:
            kwargs[name] = plt.rcParams['grid.' + name]
    return ax.gridlines(zorder=zorder, **kwargs)

def add_gridlabels(ax, gl, lons=None, lats=None, fig=None, **kwargs):
    if fig is None:
        fig = plt.gcf()
    extent = ax.get_extent(crs=identity)
    if lons is None:
        lons = gl.xlocator.tick_values(*extent[:2])
        if 180 and -180 in lons:
            lons = list(lons)
            del lons[lons.index(-180)]
            lons = np.array(lons)
    if lats is None:
        lats = gl.ylocator.tick_values(*extent[2:])
    fig.canvas.draw()
    ax.xaxis.set_major_formatter(ticks.LONGITUDE_FORMATTER) 
    ax.yaxis.set_major_formatter(ticks.LATITUDE_FORMATTER)
    ticks.lambert_xticks(ax, lons)
    ticks.lambert_yticks(ax, lats)

def create_map(subplot=(1, 1, 1), 
                projection='global.default', 
                extent=None,
                bg_color=None, 
                hide_axes=True,
                show_xform=False,
                proj_descr=None):
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
        if proj_descr is None:
            proj_descr = get_proj_description(projection)
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
        ax.set_extent(extent, crs=identity)
    if hide_axes:
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
    if show_xform and proj_descr:
        # TODO: stylize fontsize (gfw.maps.projlabelsize?)
        ax.text(0.0, -0.01, proj_descr, fontsize=9, weight=plt.rcParams['axes.labelweight'],
            color=plt.rcParams['axes.labelcolor'],
            horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
    return ax



def plot_raster_w_colorbar(raster, label='', loc='top',
                projection='global.default', hspace=None, wspace=0.016,
                bg_color=None, hide_axes=True, cbformat=None, **kwargs):
    assert loc in ('top', 'bottom')
    if hspace is None:
        hspace = 0.12
        if isinstance(projection, str):
            hspace = projection_info[projection].get('pyseas.colorbar.hspace', hspace)
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
