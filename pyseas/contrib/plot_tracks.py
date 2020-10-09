import matplotlib.pyplot as plt
from matplotlib import gridspec
import cartopy
import cartopy.feature as cfeature
import numpy as np
import pandas as pd
import datetime as DT
from collections import Counter
from collections import namedtuple
from cycler import cycler
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgba
import matplotlib.dates as mdates

from ..maps import core as maps
from .. import styles
from .. import props
from ..util import asarray, lon_avg

from ..maps import find_projection


def add_subpanel(gs, timestamp, y, kind, label, prop_map, break_on_change, miny=None, maxy=None, 
                    show_xticks=True, tick_label_width=5):
    ax = plt.subplot(gs)

    x = mdates.date2num(timestamp)

    indices = set(kind)
    for (k1, k2) in prop_map:
            mask1 = (kind == k1)
            if k2 == k1:
                mask2 = mask1
            else:
                mask2 = (kind == k2)

            mask = np.zeros_like(mask1)
            mask[:-1] = mask1[:-1] & mask2[1:]
            mask[1:] |= mask1[:-1] & mask2[1:]

            ml_coords = maps._build_multiline_string_coords(x, y, mask, break_on_change, x_is_lon=False)  

            mls = LineCollection(ml_coords, **prop_map[k1, k2])
            ax.add_collection(mls)

    if miny is None and maxy is None:
        miny0, maxy0 = np.percentile(y, [0.1, 99]) 
        y0 = 0.5 * (maxy0 + miny0)
        dy = maxy0  - miny0
        miny = y0 - 0.75 * dy
        maxy = y0 + 0.75 * dy
    elif maxy is None:
        maxy = miny + np.percentile(y - miny, 99) * 1.5
    elif miny is None:
        miny = maxy - np.percentile(maxy - y, 99) * 1.5
    ax.autoscale_view()
    ax.set_ylim(miny, maxy)
    ax.set_ylabel(label)
    if not show_xticks:
        ax.set_xticks([]) 
    else:
        ax.xaxis_date()
    return ax


def hour_offset(lons):
    lon0 = lon_avg(lons)
    return (lon0 / 180) * 12


# TODO: Clean up and document
def add_shades(ax, timestamp, lon, color=None, alpha=None):
    if color is None:
        color = plt.rcParams.get('pyseas.nightshade.color', props.chart.nightshade.color)
    if alpha is None:
        alpha = alpha=plt.rcParams.get('pyseas.nightshade.alpha', props.chart.nightshade.alpha)
    min_dt, max_dt = [mdates.num2date(x).replace(tzinfo=None) for x in ax.get_xlim()]

    timestamp = pd.to_datetime(asarray(timestamp)).to_pydatetime()
    lon = asarray(lon)

    mask = [(timestamp[0] <= x <= 
            (timestamp[0] + DT.timedelta(hours=1))) for x in timestamp]
    
    (min_dt <= timestamp) & (timestamp <= min_dt + DT.timedelta(hours=1))
    osh = hour_offset(lon[mask])
    os_min_dt = min_dt + DT.timedelta(hours=osh)
    # TODO: check this logic
    if os_min_dt.hour < 6:
        start = (DT.datetime(os_min_dt.year, os_min_dt.month, os_min_dt.day, tzinfo=os_min_dt.tzinfo)
                     - DT.timedelta(hours=6 - osh))
    else:
        start = (DT.datetime(os_min_dt.year, os_min_dt.month, os_min_dt.day, tzinfo=os_min_dt.tzinfo) 
                     + DT.timedelta(hours=18 - osh))
    while start < max_dt:
        stop = start + DT.timedelta(hours=12)
        
        adj_start = min_dt if (start < min_dt) else start
        if stop > max_dt:
            stop = max_dt
        ax.axvspan(mdates.date2num(adj_start), mdates.date2num(stop), 
                        alpha=alpha, facecolor=color, edgecolor='none')
        start += DT.timedelta(hours=24)
        mask = (start <= timestamp) & (timestamp <= start + DT.timedelta(hours=1))
        if mask.sum():
            new_osh = hour_offset(lon[mask])
            delta = new_osh - osh
            # Chose shorter delta if possible
            delta = (delta + 12) % 24 - 12
            start -= DT.timedelta(hours=delta)
            osh = new_osh

        ax.set_xlim(min_dt, max_dt)



PlotPanelInfo = namedtuple('PlotFishingPanelInfo',
    ['map_ax', 'plot_axes', 'projection_info', 'legend_handles'])

def plot_panel(timestamp, lon, lat, kind, plots, 
                prop_map, break_on_change,
                map_ratio=5,
                annotations=3, annotation_y_loc=1.0, annotation_y_align='bottom',
                annotation_axes_ndx=0, add_night_shades=False, projection_info=None,
                shift_by_cent_lon={'longitude'}):
    """

    """
    timestamp, lon, lat, kind = [asarray(x) for x in 
                                    (timestamp, lon, lat, kind)]
        
    if projection_info is None:
        projection_info = find_projection(lon, lat)
    gs = gridspec.GridSpec(1 + len(plots), 1, height_ratios=[map_ratio] + [1] * len(plots))

    ax1 = maps.create_map(gs[0], projection=projection_info.projection, 
                                 extent=projection_info.extent)
    ax1.set_anchor("S")

    maps.add_land(ax1)
    maps.add_countries(ax1)
    
    handles = maps.add_plot(lon, lat, kind, ax=ax1, 
                    props=prop_map, break_on_change=break_on_change)
    
    axes = []
    for i, d in enumerate(plots):
        values = np.array(d['values'])
        if d['label'] in shift_by_cent_lon:
            offset = 180 - projection_info.central_longitude
            values = (values + offset) % 360 - offset
        ax = add_subpanel(gs[i + 1], timestamp, values, kind, d['label'],
                          prop_map=prop_map, break_on_change=break_on_change,
                          show_xticks=(i == len(plots) - 1),
                          miny = d.get('min_y'),
                          maxy = d.get('max_y')
                          )
        if d.get('invert_yaxis'):
            ax.invert_yaxis()
        axes.append(ax)

    if annotations and len(axes):
        assert annotations > 1
        time_range = (timestamp[-1] - timestamp[0])
        # assert time_range > 0
        dts = [(x - timestamp[0]) / time_range for x in timestamp]
        indices = np.searchsorted(dts, np.linspace(0, 1, annotations))
        axn = axes[-1]
        time_as_num = mdates.date2num(timestamp[indices[0]])
        display_coords = axes[annotation_axes_ndx].transAxes.transform([time_as_num, annotation_y_loc])
        _, y_coord = axes[annotation_axes_ndx].transData.inverted().transform(display_coords)
        mapprops = plt.rcParams.get('pyseas.map.annotationmapprops', styles._annotationmapprops)
        plotprops = plt.rcParams.get('pyseas.map.annotationplotprops', styles._annotationmapprops)
        for i, ndx in enumerate(indices):
            ax1.text(lon[ndx], lat[ndx], str(i + 1), transform=maps.identity,
                     **mapprops)
            axes[annotation_axes_ndx].text(timestamp[ndx], y_coord, str(i + 1), horizontalalignment='center',
                            verticalalignment=annotation_y_align,
                          **plotprops)

    for ax in axes:
        ax.set_facecolor(plt.rcParams['pyseas.ocean.color'])
        if add_night_shades:
            add_shades(ax, timestamp, lon)

    maps.add_figure_background(color=plt.rcParams['pyseas.ocean.color'])
    plt.sca(ax1)
    return PlotPanelInfo(ax1, axes, projection_info, handles)




def track_state_panel(timestamp, lon, lat, state, plots=(), prop_map=None,
                      map_ratio=5, annotations=0, 
                      annotation_y_loc=1.0, annotation_y_align='bottom',
                      annotation_axes_ndx=0, add_night_shades=False,
                      projection_info=None, shift_by_cent_lon={'longitude'}):
    if prop_map is None:
        prop_map = plt.rcParams.get('pyseas.map.fishingprops', styles._fishing_props)
    return plot_panel(timestamp, lon, lat, state, plots, prop_map,
                      break_on_change=True, map_ratio=map_ratio, annotations=annotations, 
                      annotation_y_loc=annotation_y_loc, annotation_y_align=annotation_y_align,
                      annotation_axes_ndx=annotation_axes_ndx, add_night_shades=add_night_shades,
                      projection_info=projection_info, shift_by_cent_lon=shift_by_cent_lon)


# Backward compatibility
def plot_fishing_panel(timestamp, lon, lat, is_fishing, plots=(), prop_map=None,
                      map_ratio=5, annotations=0, 
                      annotation_y_loc=1.0, annotation_y_align='bottom',
                      annotation_axes_ndx=0, add_night_shades=False,
                      projection_info=None, shift_by_cent_lon={'longitude'}):    
    if prop_map is None:
        prop_map = plt.rcParams.get('pyseas.map.fishingprops', styles._fishing_props)
    return plot_panel(timestamp, lon, lat, is_fishing, plots, prop_map,
                      break_on_change=True, map_ratio=map_ratio, annotations=annotations, 
                      annotation_y_loc=annotation_y_loc, annotation_y_align=annotation_y_align,
                      annotation_axes_ndx=annotation_axes_ndx, add_night_shades=add_night_shades,
                      projection_info=projection_info, shift_by_cent_lon=shift_by_cent_lon)


def multi_track_panel(timestamp, lon, lat, track_id=None, plots=(), prop_map=None,
                      map_ratio=5, annotations=0, 
                      annotation_y_loc=1.0, annotation_y_align='bottom',
                      annotation_axes_ndx=0, add_night_shades=False,
                      projection_info=None, shift_by_cent_lon={'longitude'}): 
    if track_id is None:
        track_id = np.ones(len(lon))
    if prop_map is None:
        prop_cycle = iter(plt.rcParams.get('pyseas.map.trackprops', styles._dark_artist_cycler))
        prop_map = {(k, k) : next(prop_cycle) for k in set(track_id)}
    return plot_panel(timestamp, lon, lat, track_id, plots, prop_map,
                      break_on_change=False, map_ratio=map_ratio, annotations=annotations, 
                      annotation_y_loc=annotation_y_loc, annotation_y_align=annotation_y_align,
                      annotation_axes_ndx=annotation_axes_ndx, add_night_shades=add_night_shades,
                      projection_info=projection_info, shift_by_cent_lon=shift_by_cent_lon)

# Backward compatibility
def plot_tracks_panel(timestamp, lon, lat, track_id=None, plots=None, prop_map=None,
                      map_ratio=5, annotations=0, 
                      annotation_y_loc=1.0, annotation_y_align='bottom',
                      annotation_axes_ndx=0, add_night_shades=False,
                      projection_info=None, shift_by_cent_lon={'longitude'}): 
    if track_id is None:
        track_id = np.ones(len(lon))
    if prop_map is None:
        prop_cycle = iter(plt.rcParams.get('pyseas.map.trackprops', styles._dark_artist_cycler))
        prop_map = {(k, k) : next(prop_cycle) for k in set(track_id)}
    if plots is None:
        plots = [{'label' : 'longitude', 'values' : lon},
                 {'label' : 'latitude',  'values' : lat}]
    return plot_panel(timestamp, lon, lat, track_id, plots, prop_map,
                      break_on_change=False, map_ratio=map_ratio, annotations=annotations, 
                      annotation_y_loc=annotation_y_loc, annotation_y_align=annotation_y_align,
                      annotation_axes_ndx=annotation_axes_ndx, add_night_shades=add_night_shades,
                      projection_info=projection_info, shift_by_cent_lon=shift_by_cent_lon)