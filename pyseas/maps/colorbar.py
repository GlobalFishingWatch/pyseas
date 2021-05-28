import matplotlib.pyplot as plt
from matplotlib import gridspec
from . import core
from .. import styles


def add_colorbar(img, *, ax=None, label='', loc='bottom', hspace=0.05, wspace=0.016, format=None):
    """Add colorbar to a PySeas raster

    Parameters
    ----------
    img : matplotlib Image
    ax : matplotlib Axes, optional
    label : str, optional
    loc : str, optional
    hspace : float, optional
        Space between colorbar and axis
    wspace : float, optional
        Space between colorbar and label
    format : matplotlib formatter
        Formatter for colorbar labels.


    Returns
    -------
    Colorbar
    """
    assert loc in ('top', 'bottom')
    if ax is None:
        ax = plt.gca()
    is_global = isinstance(core._last_projection, str) and core._last_projection.startswith('global.')
    cbloc =  0.52 if is_global else 0.67
    cbwidth = 0.26 if is_global else 0.33
    cbheight = 0.015
    padded_height = cbheight + hspace
    hloc = 1 + padded_height if (loc == 'top') else -padded_height

    cb_ax = ax.inset_axes([cbloc, hloc, cbwidth, cbheight], transform=ax.transAxes)

    cb = plt.colorbar(img, ax=ax, cax=cb_ax, orientation='horizontal', ticklocation=loc, format=format)

    leg_ax = ax.inset_axes([0, hloc, 1 - cbwidth - wspace, 0.015], transform=ax.transAxes, frameon=False)
    leg_ax.text(1, 0.5, label, 
        fontdict=plt.rcParams.get('pyseas.map.colorbarlabelfont', styles._colorbarlabelfont),
                    horizontalalignment='right', verticalalignment='center')
    leg_ax.xaxis.set_visible(False)
    leg_ax.yaxis.set_visible(False)

    return cb_ax, leg_ax