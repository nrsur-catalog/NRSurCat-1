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

# <a href="https://colab.research.google.com/github/nrsur-catalog/NRSurCat-1/blob/gh-pages/_sources/events/{{GW EVENT NAME}}.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab"/></a>

# + tags=["remove-input"]
# %load_ext autoreload
# %autoreload 2
# %matplotlib inline

import pandas as pd

pd.set_option("display.max_rows", None, "display.max_columns", None)

# + tags=["hide-cell"]
# ! pip install nrsur_catalog
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
#
# _Note: For most events the kick inference is dominated by the prior itself, see Figs. 10 and 11 of [Islam et al, 2023](https://arxiv.org/abs/2309.14473)._

# Lets make some plots!

# + tags=["hide-input", "remove-output"]
# NRSurrogate corner plots

import os

param_sets = dict(
    mass=["mass_1_source", "mass_2_source", "mass_ratio"],
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
#
# Corner plots of the NRSurCat-1 posteriors. The plots along the diagonal display the 1D marginalized posteriors, with the median values and the central $1\sigma$ credible regions indicated as text. The contour plots display the joint 2D posteriors at the $1,2,3\sigma$ regions. The LVK posteriors are plotted using the IMRPhenomXPHM samples obtained from the the [GWTC-2.1](https://zenodo.org/record/6513631) and [GWTC-3](https://zenodo.org/record/5546663) zenodo releases. 
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
# Posterior corner plots for the component masses, and mass-ratio ($m_1^{\rm src}, m_2^{\rm src}, q$). Component masses are shown in the source frame.
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
# Posterior corner plots for the component spin magnitudes ($\chi_1, \chi_2$) and tilt angles ($\theta_1, \theta_2$).
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
# Posterior corner plots for the mass-ratio $q$, effective spin $\chi_{\rm eff}$ and the transverse spin precession parameters $\chi_p$.
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
# Posterior corner plots for the luminosity distance, ra and dec ($d_L, \alpha, \delta$).
#
#
#
# ### Remnant
#
# !["{{GW EVENT NAME}}_remnant_corner.png"]({{GW EVENT NAME}}_remnant_corner.png)
#
#
# Posterior corner plots for the remnant mass, remnant spin magnitude and kick ($M_f^{\rm src}, \chi_f, v_f$).

# + [markdown] tags=["remove-cell"]
# ## Waveform posterior-predictive plot
#
# This is a plot of waveforms generated using 1000 random posterior samples from the event's posterior.

# + tags=["hide-input", "remove-output", "remove-cell"]
fname = f"{{GW EVENT NAME}}_waveform.png"
if not os.path.isfile(fname):
    fig = nrsur_result.plot_signal(outdir=".")


# + [markdown] tags=["remove-cell"]
# ![waveform]({{GW EVENT NAME}}_waveform.png)
# -

{{ANIMATION_CELL}}

# ## Analysis configs
# Below are the configs used for the analysis of this job.
#

# + tags=["output_scroll"]
nrsur_result.print_configs()

# -

# ## Comments
#
# This has been made with `nrsur_catalog` version {{NRSUR_CATALOG_VERSION}}.
# If you used this data, please [cite this work](citation_section).
#
# Leave a comment in this [issue](https://github.com/nrsur-catalog/NRSurCat-1/issues/new?title={{GW EVENT NAME}}).
