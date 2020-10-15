import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from ..util import asarray, lon_avg, is_sorted
from .. import props


def hour_offset(lons):
    """How many hours to offset UTC based on lon to get naive time
    """
    lon0 = lon_avg(lons)
    return (lon0 / 180) * 12


def add_shades(timestamp, lon, ax=None, color=None, alpha=None):
    """Overlay colored rectangles, corresponding to night, on the current plot

    Overlays gray regions, corresponding to night, to the current plot,

    Parameters
    ----------
    timestamp : array of np.datetime
    lon : array of float
    ax : matplotlib axes, optional
    color : matplotlib color specifier, optional
        Taken from 'pyseas.nightshade.color' if not specified.
    alpha : float, optional
        Taken from 'pyseas.nightshade.alpha' if not specified.
    """
    timestamp, lon = (asarray(x) for x in (timestamp, lon))
    if not is_sorted(timestamp):
        raise ValueError('inputs must be sorted by time')
    if ax is None:
        ax = plt.gca()
    if color is None:
        color = plt.rcParams.get('pyseas.nightshade.color', props.chart.nightshade.color)
    if alpha is None:
        alpha = alpha=plt.rcParams.get('pyseas.nightshade.alpha', props.chart.nightshade.alpha)
    min_dt, max_dt = [mdates.num2date(x).replace(tzinfo=None) for x in ax.get_xlim()]

    timestamp = pd.to_datetime(asarray(timestamp)).to_pydatetime()
    lon = asarray(lon)

    mask = [(timestamp[0] <= x <= 
            (timestamp[0] + timedelta(hours=1))) for x in timestamp]
    
    # (min_dt <= timestamp) & (timestamp <= min_dt + timedelta(hours=1))
    osh = hour_offset(lon[mask])
    os_min_dt = min_dt + timedelta(hours=osh)
    # TODO: check this logic
    if os_min_dt.hour < 6:
        start = (datetime(os_min_dt.year, os_min_dt.month, os_min_dt.day, tzinfo=None)
                     - timedelta(hours=6 + osh))
    else:
        start = (datetime(os_min_dt.year, os_min_dt.month, os_min_dt.day, tzinfo=None) 
                     + timedelta(hours=18 - osh))
    while start < max_dt:
        stop = start + timedelta(hours=12)
        
        adj_start = min_dt if (start < min_dt) else start
        if stop > max_dt:
            stop = max_dt
        ax.axvspan(mdates.date2num(adj_start), mdates.date2num(stop), 
                        alpha=alpha, facecolor=color, edgecolor='none')
        start += timedelta(hours=24)
        mask = (start <= timestamp) & (timestamp <= start + timedelta(hours=1))
        if mask.sum():
            new_osh = hour_offset(lon[mask])
            delta = new_osh - osh
            # Chose shorter delta if possible
            delta = (delta + 12) % 24 - 12
            start -= timedelta(hours=delta)
            osh = new_osh

        ax.set_xlim(min_dt, max_dt)