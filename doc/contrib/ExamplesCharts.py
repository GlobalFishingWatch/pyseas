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
pyseas._reload()

# # Use case #1: change global styling
#
# Using this option, all charts will keep that style, so all charts will keep this style.

# +
# Set the global style for the notebook to the GFW chart style
psm.use(psm.styles.chart_style)

# Plot a figure
plt.figure(figsize=(10, 6))
plt.bar([1,2,3], [1,2,3], label="label")
plt.xlabel("X Label")
plt.ylabel("Y Label")
plt.title("Title")
plt.suptitle("Sup Title")
plt.legend()
plt.show()

# Plot another figure to see that it keeps the same styling.
plt.figure(figsize=(10, 6))
plt.bar([1,2,3], [3,2,1], label="label")
plt.xlabel("X Label")
plt.ylabel("Y Label")
plt.title("Title")
plt.suptitle("Sup Title")
plt.legend()
plt.show()
# -

# # Use case #2: change local styling only
#
# This option allows styling to only applying within a `with` statement. Outside of the `with` statement, global styling will apply.

# +
# You can set the style for just a single figure to not mess
# with the rest of your visualization code.

psm.use('default')

with psm.context(psm.styles.chart_style):
    plt.figure(figsize=(10, 6))
    plt.bar([1,2,3], [1,2,3], label="label")
    plt.xlabel("X Label")
    plt.ylabel("Y Label")
    plt.title("Title")
    plt.suptitle("Sup Title")
    plt.legend()
    plt.show()

# Now if we plot outside of the context, it will use the
# default matplotlib style or whatever styles are set
# in the global context.
plt.figure(figsize=(10, 6))
plt.bar([1,2,3], [3,2,1], label="label")
plt.legend()
plt.show()
# -


