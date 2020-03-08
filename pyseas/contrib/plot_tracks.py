import matplotlib.pyplot as plt
from matplotlib import gridspec
import cartopy
import cartopy.feature as cfeature
import numpy as np
from collections import Counter
from cycler import cycler
from .. import maps

DEFAULT_PADDING_DEG = 0.1


# First color in default cycler is too close to land, so replace for plotting
# tracks. TODO: replace with style sheets?
track_cycler = cycler(color=plt.rcParams['axes.prop_cycle'].by_key()['color'][1:])

def plot_tracks_panel(timestamps, lons, lats, track_ids=None ,
                 alpha_valid_pts=0.5, alpha_invalid_pts=0.5,
                 min_track_pts=5, padding_degrees=None, 
                 extent=None):
    
    assert padding_degrees is None or extent is None
    if padding_degrees is None:
        padding_degrees = DEFAULT_PADDING_DEG
    
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
    
    if extent is None:
        lon0 = max(valid_lons.min() - padding_degrees, -180)
        lat0 = max(valid_lats.min() - padding_degrees, -90)
        lon1 = min(valid_lons.max() + padding_degrees, 180)
        lat1 = min(valid_lats.max() + padding_degrees, 90)
        extent = (lon0, lon1, lat0, lat1)
    else:
        (lon0, lon1, lat0, lat1) = extent
    
    gs = gridspec.GridSpec(3, 1, height_ratios=[3, 1, 1])
    ax1 = maps.create_map(subplot=gs[0], hide_axes=False, projection=maps.identity)
    ax1.set_extent(extent, crs=maps.identity)
    maps.add_land(ax1)
    ax2 = plt.subplot(gs[1])
    ax3 = plt.subplot(gs[2])

    maps.add_plot(ax1, valid_lons, valid_lats, '.', markersize=2, 
             alpha=alpha_valid_pts, color='grey')

    valid_times = timestamps[valid_mask]
    ax2.plot(valid_times, valid_lons, '.', markersize=2, 
             alpha=alpha_valid_pts, color='grey')
    ax3.plot(valid_times, valid_lats, '.', markersize=3, 
             alpha=alpha_valid_pts, color='grey')
    
    if (~valid_mask).sum():
        ax1.plot(valid_lons, valid_lats, '+', markersize=2, 
                 alpha=alpha_invalid_pts, color='red', transform=maps.identity)
        invalid_times = timestamps[~valid_mask]
        ax2.plot(invalid_times, lons[~valid_mask], '+', markersize=2, 
                 alpha=alpha_invalid_pts, color='red')
        ax3.plot(invalid_times, lats[~valid_mask], '+', markersize=2, 
             alpha=alpha_invalid_pts, color='red')
        
    for i, (m, props) in enumerate(zip(masks, track_cycler)):
        x = lons[m]
        y = lats[m]
        maps.add_plot(ax1, x, y, '-', label=id_list[i], linewidth=0.5, **props)
        ts = timestamps[m]
        ax2.plot(ts, lons[m], '-', linewidth=0.5, **props)
        ax3.plot(ts, lats[m], '-', linewidth=0.5, **props)
    ax1.set_ylabel('lat')
    ax1.set_xlabel('lon')
    ax2.set_ylabel('lon')
    ax3.set_ylabel('lat')
    
    ax2.set_ylim(lon0, lon1)
    ax3.set_ylim(lat0, lat1)
    return ax1, ax2, ax3