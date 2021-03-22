# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import matplotlib.pyplot as plt
import matplotlib as mpl
import pyseas
import pyseas.maps as psm

# +
# Set the global style for the notebook to the GFW chart style
psm.styles.set_chart_style()

# Plot a figure
plt.figure(figsize=(10, 6))
plt.bar([1,2,3], [1,2,3])
plt.xlabel("X Label")
plt.ylabel("Y Label")
plt.title("Title")
plt.suptitle("Sup Title")
plt.show()

# Using this option, all charts will keep that style,
# so all charts will keep this style.

# Plot another figure
plt.figure(figsize=(10, 6))
plt.bar([1,2,3], [3,2,1])
plt.xlabel("X Label")
plt.ylabel("Y Label")
plt.title("Title")
plt.suptitle("Sup Title")
plt.show()

# +
# Or, you can set the style for just a single figure to not mess
# with the rest of your visualization code.
plt.style.use(['default'])
with mpl.rc_context(rc=psm.styles.chart_style):
    plt.figure(figsize=(10, 6))
    plt.bar([1,2,3], [1,2,3])
    plt.xlabel("X Label")
    plt.ylabel("Y Label")
    plt.title("Title")
    plt.suptitle("Sup Title")
    plt.show()

# Now if we plot outside of the context, it will use the
# default matplotlib style or whatever styles are set
# in the global context.
plt.figure(figsize=(10, 6))
plt.bar([1,2,3], [3,2,1])
plt.show()
# -


