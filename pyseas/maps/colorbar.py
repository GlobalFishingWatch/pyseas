import matplotlib.pyplot as plt
from matplotlib import gridspec
from . import core
from .. import styles


def fig_to_axes(crds, fig, ax):
    """Convert figure coordinates to axies coordinates"""
    display = fig.transFigure.transform(crds)
    return ax.transAxes.inverted().transform(display)

def get_fig_width(fig, ax):
    crds = fig_to_axes([(0, 0), (1, 1)], fig, ax)
    return crds[1, 0] - crds[0, 0]


def add_colorbar(img, *, ax=None, fig=None, label='', loc='bottom', width=0.33, height=0.015, format=None, 
                 hspace=0.05, wspace=0.016, min_text_width=0.33):
    """Add colorbar to a PySeas raster

    Parameters
    ----------
    img : matplotlib Image
    ax : matplotlib Axes, optional
    fig : matplotlib Figure, optional
    label : str, optional
    loc : str, optional
        'top' or 'bottom'
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
    if fig is None:
        fig = plt.gcf()
    figwidth = get_fig_width(fig, ax)
    width = min(width, figwidth)
    text_width = max(min_text_width, 1 - width - wspace)
    text_width = min(text_width, figwidth - width - wspace)
    text_width = max(text_width, 0)
    figwidth = width + text_width + wspace

    is_global = isinstance(core._last_projection, str) and core._last_projection.startswith('global.')
    right_edge = 0.78 if is_global else 1.0
    height = 0.015
    padded_height = height + hspace
    cbloc = right_edge - width
    hloc = 1 + padded_height if (loc == 'top') else -padded_height

    cb_ax = ax.inset_axes([cbloc, hloc, width, height], transform=ax.transAxes)

    cb = plt.colorbar(img, ax=ax, cax=cb_ax, orientation='horizontal', ticklocation=loc, format=format)

    offset = figwidth - 1
    leg_ax = ax.inset_axes([-offset, hloc, max(offset + cbloc - wspace, 0), 0.015], transform=ax.transAxes, frameon=False)
    leg_ax.text(1, 0.5, label, 
        fontdict=plt.rcParams.get('pyseas.map.colorbarlabelfont', styles._colorbarlabelfont),
                    horizontalalignment='right', verticalalignment='center')
    leg_ax.xaxis.set_visible(False)
    leg_ax.yaxis.set_visible(False)

    plt.sca(ax)     

    return cb_ax, leg_ax