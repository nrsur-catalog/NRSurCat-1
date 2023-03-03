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

# # Catalog plots 
#
# Here we have some catalog plots showing the ensemble results of the catalog (working on making these plotly-plots).

# +
from nrsur_catalog import Catalog

catalog = Catalog.load()
# -

# ## Mass 1

catalog.violin_plot('mass_1')

# ## Mass Ratio

catalog.violin_plot('mass_ratio')

# ## Chi Eff

catalog.violin_plot('chi_eff')

# ````{tab} Mass 1
# ```{glue:} mass_1
# ```
# ````
# ````{tab} Mass Ratio
# ```{glue:} mass_ratio
# ```
# ````
# ````{tab} Chi Eff
# ```{glue:} chi_eff
# ```
# ````
