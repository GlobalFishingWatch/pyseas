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
import matplotlib.offsetbox as mplobox
import cartopy
import cartopy.feature as cfeature
import cartopy.mpl.gridliner
import json
import os
from .. import props
from .. import styles
import geopandas as gpd
import numpy as np
from cartopy.feature import ShapelyFeature
import shapely
from shapely.geometry import MultiLineString
from skimage import io as skio
from . import ticks


monkey_patch_cartopy()

identity = cartopy.crs.PlateCarree()

root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

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
    return projection_info[region_name]['extent']

def get_proj_description(region_name):
    return projection_info[region_name]['name']


def add_land(ax=None, scale='10m', edgecolor=None, facecolor=None, linewidth=None, **kwargs):
    """Add land to an existing map

    Parameters
    ----------
    ax : matplotlib axes object, optional
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
    if ax is None:
        ax = plt.gca()
    edgecolor = edgecolor or plt.rcParams.get('pyseas.border.color', props.dark.border.color)
    facecolor = facecolor or plt.rcParams.get('pyseas.land.color', props.dark.land.color)
    linewidth = linewidth or plt.rcParams.get('pyseas.border.linewidth', 0.4)
    land = cfeature.NaturalEarthFeature('physical', 'land', scale,
                                            edgecolor=edgecolor,
                                            facecolor=facecolor,
                                            linewidth=linewidth,
                                            **kwargs)
    return ax.add_feature(land)

def add_countries(ax=None, scale='10m', edgecolor=None, facecolor=None, linewidth=None, **kwargs):
    """Add land to an existing map

    Parameters
    ----------
    ax : matplotlib axes object, optional
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
    if ax is None:
        ax = plt.gca()
    edgecolor = edgecolor or plt.rcParams.get('pyseas.border.color', props.dark.border.color)
    facecolor = facecolor or plt.rcParams.get('pyseas.land.color', props.dark.land.color)
    linewidth = linewidth or plt.rcParams.get('pyseas.border.linewidth', 0.4)
    land = cfeature.NaturalEarthFeature('cultural', 'admin_0_boundary_lines_land', scale,
                                            edgecolor=edgecolor,
                                            facecolor=facecolor,
                                            linewidth=linewidth,
                                            **kwargs)
    return ax.add_feature(land)


def add_raster(raster, ax=None, extent=(-180, 180, -90, 90), origin='upper', **kwargs):
    """Add a raster to an existing map

    Parameters
    ----------
    ax : matplotlib axes object, optional
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
    if ax is None:
        ax = plt.gca()
    if 'cmap' in kwargs and isinstance(kwargs['cmap'], str):
        src = plt.rcParams['pyseas.map.cmapsrc']
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

        if i < len(mask) and last_x is None:
            last_x = x[i]

        while i < len(mask) and mask[i]:
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
        

def add_plot(lon, lat, kind=None, props=None, ax=None, break_on_change=False, *args, **kwargs):
    """Add a plot to an existing map

    Parameters
    ----------
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
    ax : matplotlib axes object, optional
    break_on_change : bool, optional
        Whether to create a new segment when kind changes. Generally True for fishing plots
        and False for vessel plots.
    
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
    if ax is None:
        ax = plt.gca()
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
        props = {(k, k) : v for (k, v) in zip(raw_kinds, plt.rcParams['pyseas.map.trackprops'])}
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

def add_eezs(ax=None, use_boundaries=True, facecolor='none', edgecolor=None, linewidth=None, alpha=1):
    """Add EEZs to an existing map

    Parameters
    ----------
    ax : matplotlib axes object, optional
    use_boundaries : bool, optional
        use the boundaries version of EEZs which is smaller and faster, but not as detailed.
    facecolor : str, optional
    edgecolor: str or tuple, optional
        Can be styled with 'pyseas.eez.bordercolor'
    linewidth: float, optional
        Can be styled with 'pyseas.eez.linewidth'
    alpha: float, optional


    Returns
    -------
    FeatureArtist
    """
    if ax is None:
        ax = plt.gca()
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
    edgecolor = edgecolor or plt.rcParams.get('pyseas.eez.bordercolor', props.dark.eez.color)
    linewidth = linewidth or plt.rcParams.get('pyseas.eez.linewidth', 0.4)

    return ax.add_geometries(eezs.geometry, crs=identity,
                  alpha=alpha, facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth)


def add_figure_background(fig=None, color=None):
    """Set the figure background (area around plot)

    Parameters
    ----------
    fig : Figure, optional
    color : tuple or str, optional
    """
    if fig is None:
        fig = plt.gcf()
    color = color or plt.rcParams.get('pyseas.fig.background', props.dark.background.color)
    fig.patch.set_facecolor(color)


_current_gridlines = None
def add_gridlines(ax=None, zorder=0.5, **kwargs):
    """Add latitude and longitude lines to plot

    Parameters
    ----------
    ax : Axes, optional
    zorder: float, optional
        By default, lines are placed over water, but under land


    Other Parameters
    ----------------
    Keyword args are passed on to ax.gridlines

    Returns
    -------
    Gridliner
    """
    global _current_gridlines
    if ax is None:
        ax = plt.gca()
    for name in ['linewidth', 'linestyle', 'color', 'alpha']:
        if name not in kwargs:
            kwargs[name] = plt.rcParams['grid.' + name]
    _current_gridlines = ax.gridlines(zorder=zorder, **kwargs)
    return _current_gridlines

def add_gridlabels(gl=None, lons=None, lats=None, ax=None, fig=None, 
                    lon_side='bottom', lat_side='left'):
    """Add latitude and longitude labels to plot

    Parameters
    ----------
    gl : Gridliner returned from `add_gridlines`
    lons : sequence of float
    lats : sequence of float
    ax : Axes, optional
    fig : Figure, optional
    lon_side : str, optional
        'top' or 'bottom (default)
    lat_side : str, optional
        'right' or 'left' (default)
    ax : Axes, optional

    Other Parameters
    ----------------
    Keyword args are passed on to ax.gridlines

    """
    if gl is None:
        gl = _current_gridlines
    if fig is None:
        fig = plt.gcf()
    if ax is None:
        ax = plt.gca()
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
    ticks.draw_xticks(ax, lons, side=lon_side)
    ticks.draw_yticks(ax, lats, side=lat_side)


_last_projection = None

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
    global _last_projection
    if isinstance(projection, str):
        if proj_descr is None:
            proj_descr = get_proj_description(projection)
        if extent is None:
            extent = get_extent(projection)
        _last_projection = projection
        projection = get_projection(projection)
    else:
        _last_projection = None

    bg_color = bg_color or plt.rcParams.get('pyseas.ocean.color', props.dark.ocean.color)
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
        ax.text(0.0, -0.01, proj_descr, fontsize=plt.rcParams.get('pyseas.map.projlabelsize'), 
            weight=plt.rcParams['axes.labelweight'],
            color=plt.rcParams['axes.labelcolor'],
            horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
    ax.outline_patch.set_edgecolor(plt.rcParams['axes.edgecolor'])
    return ax


def add_logo(ax=None, name=None, scale=1, loc='upper left', alpha=None, box_alignment=None):
    """
    TODO: document

    """
    if name is None:
        name = plt.rcParams.get('pyseas.logo.name', 'logo.png')
    if box_alignment and isinstance(loc, str):
        raise ValueError("Can't specify box alignment with string based locations")
    if isinstance(loc, str):
        is_global = isinstance(_last_projection, str) and _last_projection.startswith('global.')
        if is_global:
            if loc == 'center':
                box_alignment = (0.5, 0.5)
                loc = (0.5, 0.5)
            else:
                v, h = loc.split()
                a0, l0 = {'upper' : (1, 0.98), 'center' : (0.5, 0.5), 'lower' : (0, 0.02)}[v]
                delta = 0.02 if (v == 'center') else 0.2
                a1, l1 = {'right' : (1, 1 - delta), 'center' : (0.5, 0.5), 'left' : (0, delta)}[h]
                box_alignment = (a1, a0)
                loc = (l1, l0)

    elif box_alignment is None:
        box_alignment = (0.5, 0.5)

        loc = (0.32, 0.92) if is_global else 'lower left'
    base_scale = plt.rcParams.get('pyseas.logo.base_scale', 1)
    if alpha is None:
        alpha = plt.rcParams.get('pyseas.logo.alpha', 1)
    if ax is None:
        ax = plt.gca()

    logo = skio.imread(os.path.join(root, 'untracked/data/logos', name))
    imagebox = mplobox.OffsetImage(logo, zoom=scale * base_scale, alpha=alpha)
    if isinstance(loc, str):
        aob = mplobox.AnchoredOffsetbox(child=imagebox, loc=loc, frameon=False)
    else:
        aob = mplobox.AnnotationBbox(offsetbox=imagebox, xy=loc, frameon=False, xycoords='axes fraction',
                                     box_alignment=box_alignment)
    ax.add_artist(aob)
    return aob



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
    im = add_raster(raster, ax=ax, **kwargs)
    add_land(ax)
    return  ax, im


def plot_raster_w_colorbar(raster, label='', loc='bottom',
                projection='global.default', hspace=0.05, wspace=0.016,
                bg_color=None, hide_axes=True, cbformat=None, **kwargs):
    """Draw a GFW themed map over a raster with a colorbar

    Parameters
    ----------
    raster : 2D array
    label : str, optional
    loc : str, optional
    projection : cartopy.crs.Projection, optional
    hspace : float, optional
        space between colorbar and axis
    wspace : float, optional
        horizontal space adjustment
    bg_color : str or tuple, optional
    hide_axes : bool
        if `true`, hide x and y axes
    cbformat : formatter
    
    Other Parameters
    ----------------
    Keyword args are passed on to plot_raster.

    Returns
    -------
    (GeoAxes, AxesImage)
    """
    assert loc in ('top', 'bottom')
    is_global = isinstance(projection, str) and projection.startswith('global.')
    if is_global:
        wratios = [1, 1, 1, 0.85]
    else:
        wratios = [1, 1, 1, 0.01]
    if loc == 'top':
        hratios = [.015, 1]
        cb_ind, pl_ind = 0, 1
        anchor = 'NE'
    else:
        hratios = [1, 0.015]
        cb_ind, pl_ind = 1, 0
        anchor = 'SE'

    gs = plt.GridSpec(2, 4, height_ratios=hratios, width_ratios=wratios, hspace=hspace, wspace=wspace)
    ax, im = plot_raster(raster, gs[pl_ind, :], projection=projection, **kwargs)
    ax.set_anchor(anchor)
    cb_ax = plt.subplot(gs[cb_ind, 2])
    cb = plt.colorbar(im, cb_ax, orientation='horizontal', shrink=0.8, format=cbformat)
    leg_ax = plt.subplot(gs[cb_ind, 1], frame_on=False)
    leg_ax.axes.get_xaxis().set_visible(False)
    leg_ax.axes.get_yaxis().set_visible(False)
    leg_ax.text(1, 0.5, label, 
        fontdict=plt.rcParams.get('pyseas.map.colorbarlabelfont', styles._colorbarlabelfont),
                    horizontalalignment='right', verticalalignment='center')
    if loc == 'top':
        cb_ax.xaxis.tick_top()
    plt.sca(ax)
    return ax, im, cb
