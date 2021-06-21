import matplotlib.pyplot as plt
from matplotlib import gridspec
import cartopy
import cartopy.feature as cfeature
import numpy as np
import pandas as pd
import datetime as DT
from collections import Counter
from collections import namedtuple
from cycler import cycler, Cycler
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgba
import matplotlib.dates as mdates

from ..maps import core as maps
from .. import styles
from .. import props
from ..util import asarray, lon_avg

from ..maps import find_projection
from ..maps.overlays import add_shades
from ..maps.core import _build_mask


# Matplotlib uses days rather than seconds for its timestamps
S_PER_DAY = 24 * 60 * 60

def _find_y_range(y, min_y, max_y):
    if min_y is None and max_y is None:
        miny0, maxy0 = np.percentile(y, [0.1, 99]) 
        y0 = 0.5 * (maxy0 + miny0)
        dy = maxy0  - miny0
        min_y = y0 - 0.75 * dy
        max_y = y0 + 0.75 * dy
    elif max_y is None:
        max_y = min_y + np.percentile(y - min_y, 99) * 1.5
    elif min_y is None:
        min_y = max_y - np.percentile(max_y - y, 99) * 1.5
    return min_y, max_y


def _add_subpanel(gs, timestamp, values, kind, label, prop_map, break_on_change, 
                    min_y=None, max_y=None, show_xticks=True, offset=None, label_angle=45):
    ax = plt.subplot(gs)

    x = mdates.date2num(timestamp)
    y = asarray(values)
    if offset is not None:
        y = (y + offset) % 360 - offset

    indices = set(kind)

    for (k1, k2) in prop_map:
        mask = _build_mask(kind, k1, k2, break_on_change)
        ml_coords = maps._build_multiline_string_coords(x, y, mask, break_on_change, x_is_lon=False)  
        p = prop_map[k1, k2].copy()
        p.pop('legend', None)
        mls = LineCollection(ml_coords, **p)
        ax.add_collection(mls)

    min_y, max_y = _find_y_range(y, min_y, max_y)
    ax.autoscale_view()
    ax.set_ylim(min_y, max_y)
    ax.set_ylabel(label)
    if not show_xticks:
        ax.set_xticks([]) 
    else:
        ax.xaxis_date()
        ticks = ax.get_xticks()
        stamps = [mdates.num2date(x) for x in ticks]
        lbls = ['{x:%Y-%m-%d:%H:%M}'.format(x=x.replace(tzinfo=None)) for x in stamps]
        ax.set_xticks(ticks)
        label_angle = label_angle % 360
        if label_angle == 0:
            alignment = 'center'
        elif label_angle > 180:
            alignment = 'left'
        else:
            alignment = 'right'
        ax.set_xticklabels(lbls, rotation=label_angle, ha=alignment)

    ax.set_facecolor(plt.rcParams.get('pyseas.ocean.color', props.dark.ocean.color))
    return ax


def _add_annotations(map_axes, time_axes, timestamp, lon, lat, n_annotations, y_loc, y_align):
    assert n_annotations > 1
    time_range = (timestamp[-1] - timestamp[0])
    dts = [(x - timestamp[0]) / time_range for x in timestamp]
    indices = np.searchsorted(dts, np.linspace(0, 1, n_annotations))
    time_as_num = mdates.date2num(timestamp[indices[0]])
    display_coords = time_axes.transAxes.transform([time_as_num, y_loc])
    _, y_coord = time_axes.transData.inverted().transform(display_coords)
    mapprops = plt.rcParams.get('pyseas.map.annotationmapprops', styles._annotationmapprops)
    plotprops = plt.rcParams.get('pyseas.map.annotationplotprops', styles._annotationmapprops)
    for i, ndx in enumerate(indices):
        map_axes.text(lon[ndx], lat[ndx], str(i + 1), transform=maps.identity, **mapprops)
        time_axes.text(timestamp[ndx], y_coord, str(i + 1), horizontalalignment='center',
                        verticalalignment=y_align, **plotprops)



PlotPanelInfo = namedtuple('PlotFishingPanelInfo',
    ['map_ax', 'plot_axes', 'projection_info', 'legend_handles'])


def _get_gs(gs, n_plots, map_ratio):
    """Get an appropriate gridspec for a PlotPanel

    If `gs` is specified, return an appropriate nested
    GridSpec within `gs`. Otherwise create a new GridSpec
    from scratch.

    Parameters
    ----------
    gs : GridSpec or None
    n_plots : int
      Length of the `plots` argument passed to `plot_panel`
    map_ratio : float
      See docs for `plot_panel`
      
    Returns
    -------
    GridSpec
    """
    dr = 1 + n_plots
    hr = [map_ratio] + [1] * n_plots
    if gs is None:
        return gridspec.GridSpec(dr, 1, height_ratios=hr)
    else:
        return gs.subgridspec(dr, 1, height_ratios=hr)


def plot_panel(timestamp, lon, lat, kind, plots, 
                prop_map, break_on_change,
                map_ratio=5.0,
                annotations=0, annotation_y_loc=1.0, annotation_y_align='bottom',
                annotation_axes_ndx=0, add_night_shades=False, projection_info=None,
                shift_by_cent_lon={'longitude'},
                label_angle=30, gs=None):
    """Plot a panel with a map and associated time-value plots

    Parameters
    ----------
    timestamp : sequence of timestamps
    lon : array of float
    lat : array of float
    kind : array
        Typically int, but should be OK as long as equality works.
    plots : list of dict containing
        values : sequence of float
            y-values for plot
        label : str
            y-label for plot
        min_y : float, optional
        max_y : float, optional
            Optional fixed range for y-axis
    prop_map : dict of (kind, kind) to matplotlib props
        Defines the props of the line segments drawn between points
        with the given kind values on either end. See `styles.create_props`.
    break_on_change : bool
        Controls how plots are segmented. `True` is suitable for fishing
        and other state change plots, while `False` is suitable for tracks.
    map_ratio : float, optional
        Ratio of map height to individual time-value plots.
    annotations : int, optional
        Number of annotations linking map to time-value plots to use.
    annotation_y_loc : float, optional
    annotation_y_align : str, optional
        Vertical alignment of annotation text. 
    annotation_axes_ndx : int, optional
        Which time-value to add annotations to. `0` is the topmost plot.
    add_night_shades : bool, optional
        Add shaded regions to time/value plots indicating night.
    projection_info : ProjectionInfo, optional
    shift_by_cent_lon : set of str
        Values in time-value plots to treat as longitude and recenter to prevent
        unnecessary dateline issues.
    label_angle : float, optional
        Angle to use for date values. Helps avoid dates crashing into each other.
    gs : GridSpec, optional

    Note
    ----
    Length of `timestamp`, `lat`, `lon` and `values` items in `plots` must
    all match.

    Returns
    -------
    PlotPanelInfo namedtuple containing
        map_ax : matplotlib axes
        plot_axes : list of matplotlib axes
        projection_info : ProjectionInfo describing projection and extent
        legend_handles : Dict of key, handle pairs suitable for building a legend
    """
    timestamp, lon, lat, kind = [asarray(x) for x in (timestamp, lon, lat, kind)]
        
    if projection_info is None:
        projection_info = find_projection(lon, lat)

    if prop_map is None or isinstance(prop_map, Cycler):
        prop_map = styles.create_props(np.unique(kind), prop_map)

    gs = _get_gs(gs, len(plots), map_ratio)

    ax1 = maps.create_map(gs[0], projection=projection_info.projection, 
                                 extent=projection_info.extent)
    ax1.set_anchor("S")

    maps.add_land(ax1)
    maps.add_countries(ax1)
    
    handles = maps.add_plot(lon, lat, kind, ax=ax1, 
                    props=prop_map, break_on_change=break_on_change)
    
    axes = []
    for i, plot_descr in enumerate(plots):
        offset = None if (plot_descr['label'] not in shift_by_cent_lon) else (
                                180 - projection_info.central_longitude)
        show_xticks = (i == len(plots) - 1)
        ax = _add_subpanel(gs[i + 1], timestamp,  kind=kind, 
                                 prop_map=prop_map, break_on_change=break_on_change,
                                 show_xticks=show_xticks, offset = offset, 
                                 label_angle=label_angle, **plot_descr)
        axes.append(ax)

  
    if annotations and axes:
        _add_annotations(ax1, axes[annotation_axes_ndx], timestamp, lon, lat, 
                         annotations, annotation_y_loc, annotation_y_align)

    maps.add_figure_background(color=plt.rcParams['pyseas.ocean.color'])
    plt.sca(ax1)
    return PlotPanelInfo(ax1, axes, projection_info, handles)




def track_state_panel(timestamp, lon, lat, state, plots=(), prop_map=None,
                      map_ratio=5, annotations=0, 
                      annotation_y_loc=1.0, annotation_y_align='bottom',
                      annotation_axes_ndx=0, add_night_shades=False,
                      projection_info=None, shift_by_cent_lon={'longitude'},
                      label_angle=30, gs=None):
    if isinstance(prop_map, str):
        prop_map = plt.rcParams.get(prop_map)
    return plot_panel(timestamp, lon, lat, state, plots, prop_map,
                      break_on_change=True, map_ratio=map_ratio, annotations=annotations, 
                      annotation_y_loc=annotation_y_loc, annotation_y_align=annotation_y_align,
                      annotation_axes_ndx=annotation_axes_ndx, add_night_shades=add_night_shades,
                      projection_info=projection_info, shift_by_cent_lon=shift_by_cent_lon,
                      label_angle=label_angle, gs=gs)


# Backward compatibility
def plot_fishing_panel(timestamp, lon, lat, is_fishing, plots=(), prop_map=None,
                      map_ratio=5, annotations=0, 
                      annotation_y_loc=1.0, annotation_y_align='bottom',
                      annotation_axes_ndx=0, add_night_shades=False,
                      projection_info=None, shift_by_cent_lon={'longitude'},
                      label_angle=30, gs=None):    
    if prop_map is None:
        prop_map = plt.rcParams.get('pyseas.map.fishingprops', styles._fishing_props)
    return plot_panel(timestamp, lon, lat, is_fishing, plots, prop_map,
                      break_on_change=True, map_ratio=map_ratio, annotations=annotations, 
                      annotation_y_loc=annotation_y_loc, annotation_y_align=annotation_y_align,
                      annotation_axes_ndx=annotation_axes_ndx, add_night_shades=add_night_shades,
                      projection_info=projection_info, shift_by_cent_lon=shift_by_cent_lon,
                      label_angle=label_angle, gs=gs)


def multi_track_panel(timestamp, lon, lat, track_id=None, plots=(), prop_map=None,
                      map_ratio=5, annotations=0, 
                      annotation_y_loc=1.0, annotation_y_align='bottom',
                      annotation_axes_ndx=0, add_night_shades=False,
                      projection_info=None, shift_by_cent_lon={'longitude'},
                      label_angle=30, gs=None): 
    if track_id is None:
        track_id = np.ones(len(lon))
    if prop_map is None:
        if isinstance(prop_map, str):
            prop_map = plt.rcParams.get(prop_map)
            if isinstance(prop_map, Cycler):
                prop_map = styles.get_props(prop_map, interstitial_color=None)
    return plot_panel(timestamp, lon, lat, track_id, plots, prop_map,
                      break_on_change=False, map_ratio=map_ratio, annotations=annotations, 
                      annotation_y_loc=annotation_y_loc, annotation_y_align=annotation_y_align,
                      annotation_axes_ndx=annotation_axes_ndx, add_night_shades=add_night_shades,
                      projection_info=projection_info, shift_by_cent_lon=shift_by_cent_lon,
                      label_angle=label_angle, gs=gs)

# Backward compatibility
def plot_tracks_panel(timestamp, lon, lat, track_id=None, plots=None, prop_map=None,
                      map_ratio=5, annotations=0, 
                      annotation_y_loc=1.0, annotation_y_align='bottom',
                      annotation_axes_ndx=0, add_night_shades=False,
                      projection_info=None, shift_by_cent_lon={'longitude'}, 
                      label_angle=30, gs=None): 
    if track_id is None:
        track_id = np.ones(len(lon))
    if prop_map is None:
        prop_cycle = plt.rcParams.get('pyseas.map.trackprops', styles._dark_artist_cycler)()
        prop_map = {(k, k) : next(prop_cycle) for k in set(track_id)}
    if plots is None:
        plots = [{'label' : 'longitude', 'values' : lon},
                 {'label' : 'latitude',  'values' : lat}]
    return plot_panel(timestamp, lon, lat, track_id, plots, prop_map,
                      break_on_change=False, map_ratio=map_ratio, annotations=annotations, 
                      annotation_y_loc=annotation_y_loc, annotation_y_align=annotation_y_align,
                      annotation_axes_ndx=annotation_axes_ndx, add_night_shades=add_night_shades,
                      projection_info=projection_info, shift_by_cent_lon=shift_by_cent_lon,
                      label_angle=label_angle, gs=gs)