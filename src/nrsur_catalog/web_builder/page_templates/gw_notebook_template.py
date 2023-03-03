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

# + tags=["hide-cell"]
# %load_ext autoreload
# %autoreload 2
# %matplotlib inline

import pandas as pd

pd.set_option("display.max_rows", None, "display.max_columns", None)

# ! python -m pip install --upgrade pip -q
# ! pip install "nrsur_catalog @ git+https://github.com/cjhaster/NRSurrogateCatalog@main#egg" -q
# -

# # {{GW EVENT NAME}}
#
# Below are some plots for {{GW EVENT NAME}} from the NRSurrogate Catalog.

# + tags=["remove-output"]
from nrsur_catalog import NRsurResult

nrsur_result = NRsurResult.load("{{GW EVENT NAME}}")
# you can specify a `cache_dir`: folder where data will be downloaded (defaults to "~/.nrsur_catalog_cache")
# -

nrsur_result.posterior_summary()

# ## Corner Plots
# ### Mass

# + tags=["hide-input"]
fig = nrsur_result.plot_corner(["mass_1", "mass_2", "chirp_mass", "mass_ratio"])
# -

# ### Spin

# + tags=["hide-input"]
fig = nrsur_result.plot_corner(["a_1", "a_2", "tilt_1", "tilt_2"])

# + tags=["hide-input"]
fig = nrsur_result.plot_corner(["mass_ratio", "chi_eff", "chi_p"])
# -

# ### Sky-localisation

# + tags=["hide-input"]
fig = nrsur_result.plot_corner(["luminosity_distance", "ra", "dec"])
# -

# ## Waveform posterior-predictive plot

# + tags=["hide-input"]
fig = nrsur_result.plot_signal(outdir=".")
# -

# ## Analysis configs
# Below are the configs used for the analysis of this job.

# + tags=["output_scroll"]
nrsur_result.print_configs()
# -

# Download the analysis datafiles with the following (you can specify an outdir)

nrsur_result.download_analysis_datafiles()
