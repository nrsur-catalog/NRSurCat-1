# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: nrsur
#     language: python
#     name: nrsur
# ---

# + tags=["hide-input"]
# %load_ext autoreload
# %autoreload 2
# %matplotlib inline
# -


import pandas as pd

pd.set_option("display.max_rows", None, "display.max_columns", None)

# ! python -m pip install --upgrade pip -q
# ! pip install "nrsur_catalog @ git+https://github.com/cjhaster/NRSurrogateCatalog@main#egg" -q

# # {{GW EVENT NAME}}
#
# Below are some plots for {{GW EVENT NAME}} from the NRSurrogate Catalog.

from nrsur_catalog import NRsurResult

nrsur_result = NRsurResult.load("{{GW EVENT NAME}}")
# cache_dir is where the events will be downloaded to (defaults to "~/.nrsur_catalog_cache")
nrsur_result.posterior_summary()

# + tags=["hide-input"]
fig = nrsur_result.plot_corner(["mass_1", "mass_2", "chirp_mass", "mass_ratio"])

# + tags=["hide-input"]
fig = nrsur_result.plot_corner(["a_1", "a_2", "tilt_1", "tilt_2"])

# + tags=["hide-input"]
fig = nrsur_result.plot_corner(["mass_ratio", "chi_eff", "chi_p"])

# + tags=["hide-input"]
fig = nrsur_result.plot_corner(["luminosity_distance", "ra", "dec"])

# + tags=["hide-input"]
fig = nrsur_result.plot_signal(outdir=".")
