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

# <a href="https://colab.research.google.com/github/nrsur-catalog/NRSurCat-1/blob/gh-pages/_sources/catalog_plots.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab"/></a>

# + tags=["remove-cell"]
# %matplotlib inline
# -

#
# # Catalog plots
#
# Here we have some catalog plots showing the ensemble results of the catalog.
# (it may take a few minutes to download the data the first time you run this notebook.)
#

# + tags=["hide-cell"]
# ! pip install nrsur_catalog

# + tags=["remove-output"]
from nrsur_catalog import Catalog

catalog = Catalog.load(cache_dir=".nrsur_catalog_cache")

# -

# ## Violin Plots

# + tags=["remove-output"]
catalog.violin_plot("mass_1_source")
catalog.violin_plot("mass_2_source")
catalog.violin_plot("mass_ratio")
catalog.violin_plot("chi_eff")
catalog.violin_plot("final_mass")
catalog.violin_plot("final_spin")
catalog.violin_plot("final_kick")

# -

#
# ````{tab} $m_1^{\rm src}$
# ![mass_1_source_violin.png](mass_1_source_violin.png)
# ````
# ````{tab} $m_2^{\rm src}$
# ![mass_2_source_violin.png](mass_2_source_violin.png)
# ````
# ````{tab} $q$
# ![mass_ratio_violin.png](mass_ratio_violin.png)
# ````
# ````{tab} $\chi_{\rm eff}$
# ![chi_eff_violin.png](chi_eff_violin.png)
# ````
# ````{tab} $M_f$
# ![final_mass_violin.png](final_mass_violin.png)
# ````
# ````{tab} $\chi_f$
# ![final_spin_violin.png](final_spin_violin.png)
# ````
# ````{tab} $v_f$
# ![final_kick_violin.png](final_kick_violin.png)
# ````
#
# ## 2D Scatter Plots

# + tags=["remove-output"]
fig = catalog.plot_2d_posterior("mass_1_source", "mass_2_source")
fig.savefig("catalog_mass_1_mass_2.png")
fig = catalog.plot_2d_posterior(
    "chi_eff", "mass_ratio", event_posteriors=False, event_quantiles=False
)
fig.savefig("catalog_chi_eff_mass_ratio.png")
fig = catalog.plot_2d_posterior(
    "chi_p", "final_kick", event_posteriors=True, event_quantiles=False
)
fig.savefig("catalog_chi_p_final_kick.png")


# -

#
# ````{tab} $m_1^{\rm src}$ vs $m_2^{\rm src}$
# ![catalog_mass_1_mass_2.png](catalog_mass_1_mass_2.png)
# ````
# ````{tab} $\chi_{\rm eff}$ vs $q$
# ![catalog_chi_eff_mass_ratio.png](catalog_chi_eff_mass_ratio.png)
# ````
# ````{tab} $\chi_{\rm P}$ vs $v_{f}$
# ![catalog_chi_p_final_kick.png](catalog_chi_p_final_kick.png)
# ````
#

# ## Comments
#
# This has been made with `nrsur_catalog` version {{NRSUR_CATALOG_VERSION}}.
# If you used this data, please [cite this work](citation_section).
#
# Leave a comment in this [issue](https://github.com/nrsur-catalog/NRSurCat-1/issues/new?title=catalog%20plots).
