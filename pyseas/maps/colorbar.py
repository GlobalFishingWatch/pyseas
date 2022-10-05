import matplotlib.pyplot as plt

from .. import styles
from . import core


def add_left_labeled_colorbar(
    img,
    *,
    ax=None,
    fig=None,
    label="",
    loc="bottom",
    width=None,
    height=0.015,
    format=None,
    hspace=0.04,
    wspace=0.016,
    valign=0.5,
    right_edge=None,
    center=False,
):
    """Add colorbar to a PySeas raster

    Parameters
    ----------
    img : matplotlib Image
    ax : matplotlib Axes, optional
    fig : matplotlib Figure, optional
    label : str, optional
    loc : str, optional
        'top' or 'bottom'
    width, height : float
        Size of colorbar in Axes coordinates
    format : matplotlib formatter
        Formatter for colorbar labels.
    hspace : float, optional
        Vertical space between colorbar and axis.
    wspace : float, optional
        Horizontal space between colorbar and label.
    valign : float, optional
        Vertical alignment of center of text relative to colorbar.
    right_edge : float, optional
        Location of right edge of colorbar in Axes coords.

    Returns
    -------
    Colorbar
    """
    not center and label
    assert loc in ("top", "bottom")
    if ax is None:
        ax = plt.gca()

    if width is None:
        if center:
            width = 0.56
        else:
            width = 0.33
    if right_edge is None:
        is_global = isinstance(
            core._last_projection, str
        ) and core._last_projection.startswith("global.")
        right_edge = 0.78 if is_global else 1.0
    hloc = 0.98 + hspace if (loc == "top") else -(height + hspace)
    if center:
        hloc += 0.02
    if center:
        wloc = 0.5 - width / 2
    else:
        wloc = right_edge - width

    cb_ax = ax.inset_axes([wloc, hloc, width, height], transform=ax.transAxes)
    cb = plt.colorbar(
        img,
        ax=ax,
        cax=cb_ax,
        orientation="horizontal",
        ticklocation=loc if (not center) else "bottom",
        format=format,
    )

    cb_ax.text(
        -wspace,
        valign,
        label,
        transform=cb_ax.transAxes,
        fontdict=plt.rcParams.get(
            "pyseas.map.colorbarlabelfont", styles._colorbarlabelfont
        ),
        horizontalalignment="right",
        verticalalignment="center",
    )

    cb_ax.minorticks_off()
    cb.outline.set_visible(False)

    plt.sca(ax)
    return cb_ax


def add_top_labeled_colorbar(
    img,
    *,
    ax=None,
    fig=None,
    left_label="",
    center_label="",
    right_label="",
    loc="bottom",
    width=None,
    height=0.015,
    format=None,
    vertical_space=0.04,
    **kwargs,
):
    """Add colorbar to a PySeas raster

    Parameters
    ----------
    img : matplotlib Image
    ax : matplotlib Axes, optional
    fig : matplotlib Figure, optional
    left_label : str, optional
    center_label : str, optional
    right_labels : str, optional
    loc : str, optional
        'top' or 'bottom'
    width, height : float
        Size of colorbar in Axes coordinates
    format : matplotlib formatter
        Formatter for colorbar labels.
    vertical_space : float, optional
        Vertical space between colorbar and label.
    center_loc : float, optional
        Location of center edge of colorbar in Axes coords.

    Returns
    -------
    Colorbar
    """
    assert loc in ("top", "bottom")
    if ax is None:
        ax = plt.gca()

    if width is None:
        width = 0.56

    hloc = 1.0 + vertical_space if (loc == "top") else -(height + vertical_space)
    wloc = 0.5 - width / 2

    cb_ax = ax.inset_axes([wloc, hloc, width, height], transform=ax.transAxes)
    cb = plt.colorbar(
        img,
        ax=ax,
        cax=cb_ax,
        orientation="horizontal",
        ticklocation="bottom",
        format=format,
        **kwargs,
    )

    if left_label:
        cb_ax.text(
            0,
            1.0,
            left_label,
            transform=cb_ax.transAxes,
            fontdict=plt.rcParams.get(
                "pyseas.map.colorbarlabelfont", styles._colorbarlabelfont
            ),
            horizontalalignment="left",
            verticalalignment="bottom",
        )

    if center_label:
        cb_ax.text(
            0.5,
            1.0,
            center_label,
            transform=cb_ax.transAxes,
            fontdict=plt.rcParams.get(
                "pyseas.map.colorbarlabelfont", styles._colorbarlabelfont
            ),
            horizontalalignment="center",
            verticalalignment="bottom",
        )

    if right_label:
        cb_ax.text(
            1.0,
            1.0,
            right_label,
            transform=cb_ax.transAxes,
            fontdict=plt.rcParams.get(
                "pyseas.map.colorbarlabelfont", styles._colorbarlabelfont
            ),
            horizontalalignment="right",
            verticalalignment="bottom",
        )

    cb_ax.minorticks_off()
    cb.outline.set_visible(False)

    plt.sca(ax)
    return cb_ax
