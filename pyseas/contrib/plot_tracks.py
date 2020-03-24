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

from .. import maps
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
    if lon0 > lon1: # TODO: check
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


def plot_tracks_panel(timestamps, lons, lats, track_ids=None ,
                 alpha_valid_pts=0.5, alpha_invalid_pts=0.5,
                 min_track_pts=5, padding_degrees=None, 
                 extent=None):
    """

    Example Usage:

    with pyseas.context(pyseas.styles.dark):

        fig = plt.figure(figsize=(12, 8), facecolor=(0.95, 0.95, 0.95))
        ts = [pd.Timestamp(x).to_pydatetime() for x in df.timestamp]
        ax1, ax2, ax3 = plot_tracks.plot_tracks_panel(ts, df.lon, df.lat, df.track_id )
        fig.suptitle(ssvid + ' - tracks ' + new_msgs.iloc[0].which, y=0.93)    
        plt.show() 

    """
    
    assert padding_degrees is None or extent is None
    if padding_degrees is None:
        padding_degrees = DEFAULT_PADDING_DEG
    
    track_cycler = plt.rcParams['axes.prop_cycle']


    assert len(lons) == len(lats) == len(timestamps)
    timestamps = np.asarray(timestamps)
    lons = np.asarray(lons)
    lats = np.asarray(lats)
    ids = np.array(['1' for x in lons]) if (track_ids is None) else np.asarray(track_ids)

    id_mask = [x not in ('', None) for x in ids]
    id_list = sorted([k for (k, n) in 
                      Counter(ids[id_mask]).most_common() 
                          if n >= min_track_pts])
    if not(len(id_list)):
        logging.warning('tracks too short to plot.')
        return None, None, None
    # TODO: maybe we can plot and scale using all points here?
    
    masks = []
    valid_mask = np.zeros([len(lons)], dtype=bool)
    
    for id_ in id_list:
        mask = (ids == id_)
        masks.append(mask)
        valid_mask |= mask

    valid_lons = lons[valid_mask]
    valid_lats = lats[valid_mask]
    
    # Refactor ~below here
    projection, default_extent, descr = find_projection(valid_lons, valid_lats)

    if extent is None:
        extent = default_extent
    
    gs = gridspec.GridSpec(3, 1, height_ratios=[3, 1, 1])
    ax1 = maps.create_map(subplot=gs[0], hide_axes=False, 
                            projection=projection, proj_descr=descr)
    ax1.set_extent(extent, crs=maps.identity)
    maps.add_land(ax1)
    ax2 = plt.subplot(gs[1])
    ax3 = plt.subplot(gs[2])

    if alpha_valid_pts > 0:
        maps.add_plot(ax1, valid_lons, valid_lats, fmt='.', markersize=2, 
                 alpha=alpha_valid_pts, color='grey')

        valid_times = timestamps[valid_mask]
        ax2.plot(valid_times, valid_lons, marker='.', markersize=2, 
                 alpha=alpha_valid_pts, color='grey')
        ax3.plot(valid_times, valid_lats, marker='.', markersize=3, 
                 alpha=alpha_valid_pts, color='grey')
    
    if alpha_invalid_pts > 0 and (~valid_mask).sum():
        maps.add_plot(ax1, lons[~valid_mask], lats[~valid_mask], fmt='+', markersize=2,
                 alpha=alpha_invalid_pts, color='red', transform=maps.identity)
        invalid_times = timestamps[~valid_mask]
        ax2.plot(invalid_times, lons[~valid_mask], marker='+', markersize=2, 
                 alpha=alpha_invalid_pts, color='red')
        ax3.plot(invalid_times, lats[~valid_mask], marker='+', markersize=2, 
             alpha=alpha_invalid_pts, color='red')
        
    for i, (m, props) in enumerate(zip(masks, track_cycler)):
        x = lons[m]
        y = lats[m]
        maps.add_plot(ax1, x, y, fmt='-', label=id_list[i], linewidth=0.5, **props)
        ts = timestamps[m]
        ax2.plot(ts, lons[m], linewidth=0.5, **props)
        ax3.plot(ts, lats[m], linewidth=0.5, **props)
    ax1.set_ylabel('lat')
    ax1.set_xlabel('lon')
    ax2.set_ylabel('lon')
    ax3.set_ylabel('lat')
    
    (lon0, lon1, lat0, lat1) = extent
    ax2.set_ylim(lon0, lon1)
    ax3.set_ylim(lat0, lat1)
    return ax1, ax2, ax3

def add_subpanel(gs, timestamp, y, kind, label, miny=None, maxy=None, show_xticks=True):
    ax = plt.subplot(gs)

    props = styles.dark['gfw.plot.fishingprops']
    x = mdates.date2num(timestamp)

    for (k1, k2) in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            # TODO: refactor
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

            ml_coords = maps._build_multiline_string_coords(x, y, mask, True, x_is_lon=False)  

            mls = LineCollection(ml_coords, **props[k1, k2]) # Styleize
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

PlotFishingPanelInfo = namedtuple('PlotFishingPanelInfo',
    ['map_ax', 'lon_ax', 'lat_ax', 'speed_ax', 'depth_ax', 'extent'])

def plot_fishing_panel(timestamp, lon, lat, speed, elevation, is_fishing ,
                        padding_degrees=None, extent=None, map_ratio=3):
    """

    """
    timestamp, lon, lat, speed, elevation, is_fishing = [asarray(x) for x in 
                                    (timestamp, lon, lat, speed, elevation, is_fishing)]
    assert padding_degrees is None or extent is None
    if padding_degrees is None:
        padding_degrees = DEFAULT_PADDING_DEG
        
    proj, extent, descr = find_projection(lon, lat)
    gs = gridspec.GridSpec(5, 1, height_ratios=[map_ratio, 1, 1, 1, 1])

    ax1 = maps.create_map(gs[0], projection=proj, proj_descr=descr)
    
    maps.add_land(ax1)
    maps.add_countries(ax1)

    props = styles.dark['gfw.map.fishingprops']
    
    maps.add_plot(ax1, lon, lat, is_fishing, 
                  props=props, break_on_change=True)
    
    ax1.set_extent(extent, crs=maps.identity)

    # TODO: fix y label alignment by using a standard format that alway pads to 4 digits.
    # Then can leave depth alone.

    ax2 = add_subpanel(gs[1], timestamp, lon, is_fishing, 'lon', show_xticks=False)
    ax3 = add_subpanel(gs[2], timestamp, lat, is_fishing, 'lat', show_xticks=False)
    ax4 = add_subpanel(gs[3], timestamp, speed, is_fishing, 'speed (knots)', miny=0, show_xticks=False)
    if min(elevation) <= -995:
        elevation /= 1000
        label = 'depth (km)'
    else:
        label = 'depth (m)'
    ax5 = add_subpanel(gs[4], timestamp, -elevation, is_fishing, label, miny=0)
    ax5.invert_yaxis()

    for ax in [ax2, ax3, ax4, ax5]:
        ax.set_facecolor(plt.rcParams['gfw.ocean.color'])

    return PlotFishingPanelInfo(ax1, ax2, ax3, ax4, ax5, extent)


