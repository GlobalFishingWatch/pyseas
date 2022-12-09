# flake8: noqa
from .. import cm, context, styles, use
from . import overlays, rasters
from .bivariate import add_bivariate_colorbox, add_bivariate_raster
from .colorbar import add_left_labeled_colorbar, add_top_labeled_colorbar
from .core import (add_countries, add_eezs, add_figure_background,
                   add_gridlabels, add_gridlines, add_h3_data, add_land,
                   add_logo, add_miniglobe, add_plot, add_raster, create_map,
                   create_maps, identity, plot, plot_h3_data, plot_raster,
                   plot_raster_w_colorbar)
from .extent import set_lat_extent, set_lon_extent
from .projection import find_projection
from .scalebar import add_scalebar

add_colorbar = add_left_labeled_colorbar
