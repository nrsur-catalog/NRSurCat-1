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

# <a href="https://colab.research.google.com/github/cjhaster/NRSurrogateCatalog/blob/gh-pages/_sources/catalog_plots.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab"/></a>

# + tags=["remove-cell"]
# %matplotlib inline
# -

# # Catalog plots
#
# Here we have some catalog plots showing the ensemble results of the catalog.
# (Note: it may take a few minutes to download the data the first time you run this notebook.)

# + tags=["hide-cell"]
import pip


try:
    __import__("nrsur_catalog")
except ImportError:
    pip.main(['install', "nrsur_catalog @ git+https://github.com/cjhaster/NRSurrogateCatalog@main#egg", "-q"])

# + tags=["remove-output"]
from nrsur_catalog import Catalog

catalog = Catalog.load(cache_dir=".nrsur_catalog_cache")

# -

# ## Violin Plots

# + tags=["remove-output"]
catalog.violin_plot("mass_1")
catalog.violin_plot("mass_2")
catalog.violin_plot("final_mass")
catalog.violin_plot("mass_ratio")
catalog.violin_plot("chi_eff")
catalog.violin_plot("final_spin")
catalog.violin_plot("final_kick")

# -

#
# ````{tab} $m_1$
# ![mass_1_violin.png](mass_1_violin.png)
# ````
# ````{tab} $m_2$
# ![mass_2_violin.png](mass_2_violin.png)
# ````
# ````{tab} $m_f$
# ![final_mass_violin.png](final_mass_violin.png)
# ````
# ````{tab} $q$
# ![mass_ratio_violin.png](mass_ratio_violin.png)
# ````
# ````{tab} $\chi_{\text{EFF}}$
# ![chi_eff_violin.png](chi_eff_violin.png)
# ````
# ````{tab} $\chi_{\text{f}}$
# ![final_spin_violin.png](final_spin_violin.png)
# ````
# ````{tab} $v_{\text{kick}}$
# ![final_kick_violin.png](final_kick_violin.png)
# ````
#
# ## 2D Scatter Plots

# + tags=["remove-output"]
fig = catalog.plot_2d_posterior("mass_1", "mass_2")
fig.savefig("catalog_mass_1_mass_2.png")
fig = catalog.plot_2d_posterior("chi_eff", "mass_ratio", event_posteriors=False, event_quantiles=False)
fig.savefig("catalog_chi_eff_mass_ratio.png")
fig = catalog.plot_2d_posterior("chi_p", "final_kick", event_posteriors=True, event_quantiles=False)
fig.savefig("catalog_chi_p_final_kick.png")


# -

#
# ````{tab} $m_1$ vs $m_2$
# ![catalog_mass_1_mass_2.png](catalog_mass_1_mass_2.png)
# ````
# ````{tab} $\chi_{\text{EFF}}$ vs $q$
# ![catalog_chi_eff_mass_ratio.png](catalog_chi_eff_mass_ratio.png)
# ````
# ````{tab} $\chi_{\text{P}}$ vs $v_{\text{kick}}$
# ![catalog_chi_p_final_kick.png](catalog_chi_p_final_kick.png)
# ````
#
