import matplotlib.pyplot as plt
from matplotlib import gridspec
import cartopy
import cartopy.feature as cfeature
import numpy as np
from collections import Counter
from collections import namedtuple
from cycler import cycler
from shapely.geometry import MultiLineString
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgba
import matplotlib.dates as mdates

from ..maps import core as maps
from .. import styles
from ..util import asarray

DEFAULT_PADDING_DEG = 0.1


def find_projection(lons, lats, delta_scale=0.2, abs_delta=0.1, percentile=99.9):
    assert len(lons) == len(lats), (len(lons), len(lats))
    coslon = np.mean(np.cos(np.radians(lons)))
    sinlon = np.mean(np.sin(np.radians(lons)))
    lonm0 = np.degrees(np.arctan2(sinlon, coslon))
    lons = (lons - lonm0 + 180) % 360 + lonm0 - 180
    lon0, lonm, lon1 = np.percentile(lons, (100 - percentile, 50, percentile))
    (lon0, lon1) = [(x - lonm + 180) % 360 + lonm - 180 for x in (lon0, lon1)]
    if lon0 > lon1: 
        lon0, lon1 = lon1, lon0
    lat0, latm, lat1 = np.percentile(lats, (100 - percentile, 50, percentile))
    lon_delta = abs(lon1 - lon0) * delta_scale + abs_delta
    lat_delta = abs(lat1 - lat0) * delta_scale + abs_delta

    projection = cartopy.crs.LambertAzimuthalEqualArea(central_longitude=lonm, 
                                                        central_latitude=latm)
    extent = (lon0 - lon_delta, lon1 + lon_delta, lat0 - lat_delta, lat1 + lat_delta)
    lonstr = ("{}°E" if (lonm >= 0) else "{}°W").format(int(round(abs(lonm))))
    latstr = ("{}°N" if (latm >= 0) else "{}°S").format(int(round(abs(latm))))
    description = "Lambert azimuthal equal area @{},{}".format(lonstr, latstr)
    return projection, extent, description


def add_subpanel(gs, timestamp, y, kind, label, prop_map, miny=None, maxy=None, 
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

            ml_coords = maps._build_multiline_string_coords(x, y, mask, True, x_is_lon=False)  

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


PlotPanelInfo = namedtuple('PlotFishingPanelInfo',
    ['map_ax', 'plot_axes', 'extent'])


def plot_panel(timestamp, lon, lat, kind, plots, 
                prop_map, break_on_change,
                padding_degrees=None, extent=None, map_ratio=5,
                annotations=3, annotation_y_shift=0.3):
    """

    """
    timestamp, lon, lat, kind = [asarray(x) for x in 
                                    (timestamp, lon, lat, kind)]
    assert padding_degrees is None or extent is None
    if padding_degrees is None:
        padding_degrees = DEFAULT_PADDING_DEG
        
    proj, extent, descr = find_projection(lon, lat)
    gs = gridspec.GridSpec(1 + len(plots), 1, height_ratios=[map_ratio] + [1] * len(plots))

    ax1 = maps.create_map(gs[0], projection=proj, proj_descr=descr)

    maps.add_land(ax1)
    maps.add_countries(ax1)
    
    maps.add_plot(lon, lat, kind, ax=ax1, 
                  props=prop_map, break_on_change=True)
    
    ax1.set_extent(extent, crs=maps.identity)

    axes = []
    for i, d in enumerate(plots):
        ax = add_subpanel(gs[i + 1], timestamp, asarray(d['values']), kind, d['label'], 
                          prop_map=prop_map,
                          show_xticks=(i == len(plots) - 1),
                          miny = d.get('min_y'),
                          maxy = d.get('max_y')
                          )
        if d.get('invert_yaxis'):
            ax.invert_yaxis()
        axes.append(ax)

    if annotations:
        assert annotations > 1
        time_range = (timestamp[-1] - timestamp[0])
        # assert time_range > 0
        dts = [(x - timestamp[0]) / time_range for x in timestamp]
        indices = np.searchsorted(dts, np.linspace(0, 1, annotations))
        axn = axes[-1]
        ylim = (axn.get_ylim()[0] - annotation_y_shift if plots[-1].get('invert_yaxis') 
           else axn.get_ylim()[1] + annotation_y_shift)
        axn.tick_params(axis='x', direction='inout')
        mapprops = plt.rcParams.get('gfw.map.annotationmapprops', styles._annotationmapprops)
        plotprops = plt.rcParams.get('gfw.map.annotationplotprops', styles._annotationmapprops)
        for i, ndx in enumerate(indices):
            ax1.text(lon[ndx], lat[ndx], str(i + 1), transform=maps.identity,
                     **mapprops)
            axes[-1].text(timestamp[ndx], ylim, str(i + 1), horizontalalignment='center',
                          **plotprops)

    for ax in axes:
        ax.set_facecolor(plt.rcParams['gfw.ocean.color'])
    maps.add_figure_background(color=plt.rcParams['gfw.ocean.color'])
    plt.sca(ax1)
    return PlotPanelInfo(ax1, axes, extent)





def plot_fishing_panel(timestamp, lon, lat, is_fishing, plots,
                        padding_degrees=None, extent=None, map_ratio=5,
                        annotations=3, annotation_y_shift=0.3):
    """

    """
    return plot_panel(timestamp, lon, lat, is_fishing, plots,
                      plt.rcParams['gfw.map.fishingprops'], break_on_change=True,
                      padding_degrees=padding_degrees, extent=extent, 
                      map_ratio=map_ratio, annotations=annotations, 
                      annotation_y_shift=annotation_y_shift)


def plot_tracks_panel(timestamp, lon, lat, track_id=None, plots=None, 
                        padding_degrees=None, extent=None, map_ratio=5):

    if track_id is None:
        track_id = np.ones_like(lon)

    if plots is None:
        plots = [{'label' : 'longitude', 'values' : lon},
                 {'label' : 'latitude', 'values' : lat}]

    prop_cycle = iter(plt.rcParams['gfw.map.trackprops'])
    prop_map = {(k, k) : next(prop_cycle) for k in set(track_id)}

    return plot_panel(timestamp, lon, lat, track_id, plots,
                      prop_map, break_on_change=False,
                      padding_degrees=padding_degrees, extent=extent, 
                      map_ratio=map_ratio, annotations=0)
