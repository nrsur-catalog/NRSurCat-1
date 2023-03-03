# ---
# jupyter:
#   jupytext:
#     formats: ipynb,md:myst,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: venv
#     language: python
#     name: venv
# ---

# # Catalog plots 
#
# Here we have some catalog plots showing the ensemble results of the catalog (working on making these plotly-plots).

# +
from nrsur_catalog import Catalog

catalog = Catalog.load()

# +
from myst_nb import glue

fig = catalog.violin_plot('mass_1')
glue("mass_1", fig, display=False)

fig = catalog.violin_plot('mass_ratio')
glue("mass_ratio", fig, display=False)

fig = catalog.violin_plot('chi_eff')
glue("chi_eff", fig, display=False)

# -

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
