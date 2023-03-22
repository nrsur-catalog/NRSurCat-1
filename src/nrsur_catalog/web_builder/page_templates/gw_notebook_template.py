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
import os
print(os.getcwd())

# +
import pip


try:
    __import__("nrsur_catalog")
except ImportError:
    pip.main(['install', "nrsur_catalog @ git+https://github.com/cjhaster/NRSurrogateCatalog@main#egg", "-q"])   

# -

# # {{GW EVENT NAME}}
#
# Below are some plots for {{GW EVENT NAME}} from the NRSurrogate Catalog.

# + tags=["remove-output"]
from nrsur_catalog import NRsurResult

nrsur_result = NRsurResult.load("{{GW EVENT NAME}}")
# you can specify a `cache_dir`: folder where data will be downloaded (defaults to "~/.nrsur_catalog_cache")
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
fig = nrsur_result.plot_corner(["mass_1", "mass_2", "chirp_mass", "mass_ratio"])
fig.savefig("{{GW EVENT NAME}}_mass_corner.png")
fig = nrsur_result.plot_corner(["a_1", "a_2", "tilt_1", "tilt_2"])
fig.savefig("{{GW EVENT NAME}}_spin_corner.png")
fig = nrsur_result.plot_corner(["mass_ratio", "chi_eff", "chi_p"])
fig.savefig("{{GW EVENT NAME}}_effective_spin.png")
fig = nrsur_result.plot_corner(["luminosity_distance", "ra", "dec"])
fig.savefig("{{GW EVENT NAME}}_sky_localisation.png")

# LVK-Comparison plots
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
# !["{{GW EVENT NAME}}_mass_corner.png"]({{GW EVENT NAME}}_mass_corner.png)
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
# !["{{GW EVENT NAME}}_spin_corner.png"]({{GW EVENT NAME}}_spin_corner.png)
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
# !["{{GW EVENT NAME}}_effective_spin.png"]({{GW EVENT NAME}}_effective_spin.png)
# :::
#
# :::{tab-item} LVK-Comparison
# :sync: key2
#
# !["{{GW EVENT NAME}}_effective_spin.png"]({{GW EVENT NAME}}_effective_spin.png)
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
# !["{{GW EVENT NAME}}_sky_localisation.png"]({{GW EVENT NAME}}_sky_localisation.png)
# :::
#
# :::{tab-item} LVK-Comparison
# :sync: key2
#
# !["{{GW EVENT NAME}}_sky_localisation.png"]({{GW EVENT NAME}}_sky_localisation.png)
# :::
#
# ::::
#
#
#

# ## Waveform posterior-predictive plot

# + tags=["hide-input", "remove-output"]
fig = nrsur_result.plot_signal(outdir=".")
# -

# ![waveform]({{GW EVENT NAME}}_waveform.png)

# ## Analysis configs
# Below are the configs used for the analysis of this job.

# + tags=["output_scroll"]
nrsur_result.print_configs()
# -

# Download the analysis datafiles with the following (you can specify an outdir)

nrsur_result.download_analysis_datafiles()
