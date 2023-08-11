# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # NRSurrogate Events
# Table of all the events analyses in the NRSurrogate Catalog.

# + tags=["remove-cell"]
from nrsur_catalog_webbuilder.utils import get_catalog_summary

summary_df = get_catalog_summary("{{EVENTS_DIR}}", "{{CACHE_DIR}}")

import itables.options as opt

# + tags=["remove-input", "full-width"]
from itables import JavascriptFunction, init_notebook_mode, show

opt.drawCallback = JavascriptFunction(
    "function(settings) " '{MathJax.Hub.Queue(["Typeset",MathJax.Hub]);}'
)
init_notebook_mode(all_interactive=True)
summary_df.rename(columns={"Waveform": "   "})
summary_df = summary_df.reset_index(drop=True)
show(
    summary_df,
    style="width:3500px",
    scrollX=True,
    autoWidth=True,
    lengthMenu=[5, 10, 20, 50],
    classes="cell-border nowrap display compact",
    caption='<caption style="caption-side: bottom-start">Made with <a href="https://mwouts.github.io/itables/">itables</a> and <a href="https://datatables.net/">datatables</a>.</caption>',
)

# -
