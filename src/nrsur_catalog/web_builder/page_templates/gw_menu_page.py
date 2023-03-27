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

# + tags=["remove-input"]
import glob
import pandas as pd
from nrsur_catalog.utils import get_event_name
import os
from itables import init_notebook_mode, show

init_notebook_mode(all_interactive=True)

webroot = 'https://cjhaster.com/NRSurrogateCatalog/'
LINK = "<a href='{l}'> {txt}</a>"

events_dir = '{{IPYNB_DIR}}'
event_ipynb = glob.glob(f"{events_dir}/GW*.ipynb")
event_waveform = glob.glob(f"{events_dir}/*waveform.png")
event_name = [get_event_name(os.path.basename(f)) for f in event_ipynb]
event_link = [f"{webroot}/events/{n}.html" for n in event_name]

thumbnails = [f"{webroot}/_images/{os.path.basename(f)}" for f in event_waveform]
thumbnails = [f"<img src='{f}' height='100'>" for f in thumbnails]
thumbnails = [LINK.format(l=l, txt=t) for l, t in zip(event_link, thumbnails)]
event = [LINK.format(l=l, txt=t) for l, t in zip(event_link, event_name)]

df = pd.DataFrame({
    "Event": event,
    " ": thumbnails
})

df = df.sort_values(by="Event")
df.set_index('Event', inplace=True)
show(df, dom='ltpr', columnDefs=[{"className": "dt-left", "targets": "_all"}])
# -
