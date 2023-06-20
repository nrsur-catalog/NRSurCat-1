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

# # NRSur Events
# Table of all the events analyses in the NRSur Catalog.

# + tags=["remove-cell"]
from nrsur_catalog.web_builder.utils import get_catalog_summary

summary_df = get_catalog_summary("{{EVENTS_DIR}}", "{{CACHE_DIR}}")

# + tags=["remove-input"]
from itables import init_notebook_mode, show, JavascriptFunction
import itables.options as opt

opt.css = opt.css + """
.itables table.dataTable tbody td {
  vertical-align: top;
}
"""

opt.drawCallback = JavascriptFunction(
    "function(settings) " '{MathJax.Hub.Queue(["Typeset",MathJax.Hub]);}'
)
init_notebook_mode(all_interactive=True)
show(
    summary_df,
    columnDefs=[{"width": "1000px", "targets": "_all"}],
    scrollX=True,
    style="width:3000px",
    autoWidth=False,
    lengthMenu=[5, 10, 20, 50]
)



# -
