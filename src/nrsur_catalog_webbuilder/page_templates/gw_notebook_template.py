# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: nrsur
#     language: python
#     name: nrsur
# ---

# <a href="https://colab.research.google.com/github/cjhaster/NRSurrogateCatalog/blob/gh-pages/_sources/events/{{GW EVENT NAME}}.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab"/></a>

# + tags=["remove-input"]
# %load_ext autoreload
# %autoreload 2
# %matplotlib inline

import pandas as pd

pd.set_option("display.max_rows", None, "display.max_columns", None)

# + tags=["hide-cell"]
import pip

try:
    __import__("nrsur_catalog")
except ImportError:
    pip.main(["install", "nrsur_catalog", "-q", ])

# -

# # {{GW EVENT NAME}}
#
# Below are some plots for {{GW EVENT NAME}} from the NRSurrogate Catalog.

# + tags=["remove-output"]
from nrsur_catalog import NRsurResult

nrsur_result = NRsurResult.load("{{GW EVENT NAME}}", cache_dir=".nrsur_catalog_cache")
# you can specify a `cache_dir`: folder where data will be downloaded
# -

# ## Summary

# + tags=["remove-output"]
nrsur_result.summary()
# -

#
# {{SUMMARY_TABLE}}
#

# Lets make some plots!

# + tags=["hide-input", "remove-output"]
# NRSurrogate corner plots

import os

param_sets = dict(
    mass=["mass_1", "mass_2", "chirp_mass", "mass_ratio"],
    spin=["a_1", "a_2", "tilt_1", "tilt_2"],
    effective_spin=["mass_ratio", "chi_eff", "chi_p"],
    sky_localisation=["luminosity_distance", "ra", "dec"],
    remnant=["final_mass", "final_spin", "final_kick"],
)
for name, params in param_sets.items():
    fname = f"{{GW EVENT NAME}}_{name}_corner.png"
    if not os.path.isfile(fname):
        fig = nrsur_result.plot_corner(params)
        fig.savefig(fname)

    if name == "remnant":
        continue

    # LVK-Comparison plots
    fname = f"{{GW EVENT NAME}}_compare_{name}_corner.png"
    if not os.path.isfile(fname):
        fig = nrsur_result.plot_lvk_comparison_corner(params)
        fig.savefig(fname)

# -

# ## Corner Plots
#
# ### Mass
#
#
# ::::{tab-set}
#
# :::{tab-item} NRSurrogate
# :sync: key1
#
# !["{{GW EVENT NAME}}_mass_corner.png"]({{GW EVENT NAME}}_mass_corner.png)
# :::
#
# :::{tab-item} LVK-Comparison
# :sync: key2
#
# !["{{GW EVENT NAME}}_compare_mass_corner.png"]({{GW EVENT NAME}}_compare_mass_corner.png)
# :::
#
# ::::
#
#
#
# ### Spin
#
#
# ::::{tab-set}
#
# :::{tab-item} NRSurrogate
# :sync: key1
#
# !["{{GW EVENT NAME}}_spin_corner.png"]({{GW EVENT NAME}}_spin_corner.png)
# :::
#
# :::{tab-item} LVK-Comparison
# :sync: key2
#
# !["{{GW EVENT NAME}}_compare_spin_corner.png"]({{GW EVENT NAME}}_compare_spin_corner.png)
# :::
#
# ::::
#
#
# ### Effective Spin
#
#
# ::::{tab-set}
#
# :::{tab-item} NRSurrogate
# :sync: key1
#
# !["{{GW EVENT NAME}}_effective_spin_corner.png"]({{GW EVENT NAME}}_effective_spin_corner.png)
# :::
#
# :::{tab-item} LVK-Comparison
# :sync: key2
#
# !["{{GW EVENT NAME}}_compare_effective_spin_corner.png"]({{GW EVENT NAME}}_compare_effective_spin_corner.png)
# :::
#
# ::::
#
#
#
# ### Sky-localisation
#
#
# ::::{tab-set}
#
# :::{tab-item} NRSurrogate
# :sync: key1
#
# !["{{GW EVENT NAME}}_sky_localisation_corner.png"]({{GW EVENT NAME}}_sky_localisation_corner.png)
# :::
#
# :::{tab-item} LVK-Comparison
# :sync: key2
#
# !["{{GW EVENT NAME}}_compare_sky_localisation_corner.png"]({{GW EVENT NAME}}_compare_sky_localisation_corner.png)
# :::
#
# ::::
#
#
#
# ### Remnant
#
# !["{{GW EVENT NAME}}_remnant_corner.png"]({{GW EVENT NAME}}_remnant_corner.png)
#

# ## Waveform posterior-predictive plot

# + tags=["hide-input", "remove-output"]
fname = f"{{GW EVENT NAME}}_waveform.png"
if not os.path.isfile(fname):
    fig = nrsur_result.plot_signal(outdir=".")

# -

# ![waveform]({{GW EVENT NAME}}_waveform.png)

{{ANIMATION_CELL}}

# ## Analysis configs
# Below are the configs used for the analysis of this job.

# + tags=["output_scroll"]
nrsur_result.print_configs()
# -

# If you used this data, please [cite this work](../citation.md).
#
# ## Comments
# Leave a comment in this [issue](https://github.com/nrsur-catalog/NRSurCat-1/issues/new?title={{GW EVENT NAME}}).


