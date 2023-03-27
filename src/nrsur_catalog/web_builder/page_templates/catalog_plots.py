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

# + tags=["remove-output"]
from nrsur_catalog import Catalog

catalog = Catalog.load(cache_dir=".nrsur_catalog_cache")
catalog.violin_plot("mass_1")
catalog.violin_plot("mass_ratio")
catalog.violin_plot("chi_eff")
# -

# ## Violin Plots
#
# ````{tab} $m_1$
# ![mass_1_violin.png](mass_1_violin.png)
# ````
# ````{tab} $q$
# ![mass_ratio_violin.png](mass_ratio_violin.png)
# ````
# ````{tab} $\chi_{\text{EFF}}$
# ![chi_eff_violin.png](chi_eff_violin.png)
# ````

