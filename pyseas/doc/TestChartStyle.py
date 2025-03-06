# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pyseas.maps as psm
import numpy as np
import matplotlib.pyplot as plt
import pyseas

# This magic function attempts to reload all of PySeas, which is
# good for testing
pyseas._reload()

# Currently the style is called `chart_style`.
# But perhaps it should be styles.charts.light instead.

# I've incorporated most of David and Fernando's suggestions
# except for turning off clipping, which I haven't found a style
# for.

with psm.context(psm.styles.chart_style):
    plt.plot(np.arange(10), np.arange(10), '--.', label='line')
    plt.xlim(0, 8)
    plt.legend()

# %%
# Note that styles is currently located in pyseas and aliased in pyseas.maps.
# It might make sense to have pyseas incorporate styles.maps and styles.charts
# So pyseas.styles.maps is basically the same (minus the chart style which now one uses)
# and pyseas.styles.charts gives the charts styles (so we could have multiple ones)

import pyseas
pyseas.styles.dark

# %%
