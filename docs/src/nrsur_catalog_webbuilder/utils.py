import os

import pandas as pd

from nrsur_catalog import Catalog
from nrsur_catalog.utils import LATEX_LABELS
from nrsur_catalog import __website__

from .video_links import get_video_html

LINK = "<a href='{l}'> {txt}</a>"

ANIM_CELL = """
# + [markdown] tags=["full-width"]
# ## Animations  
# Here are some animations of the posterior.
# 
# |Spin       | 
# |-----------|
# | {spin}    |   
#
# |Remnant       | 
# |-----------|
# | {remnant}    | 
#
# -
"""


def get_animation_cell(event_name: str) -> str:
    """Returns the animation cell for the given event"""
    remnant_html = get_video_html(event_name, "remnant")
    spin_html = get_video_html(event_name, "spin")
    if remnant_html is None or spin_html is None:
        return ""
    return ANIM_CELL.format(spin=spin_html, remnant=remnant_html)


def get_catalog_summary(events_dir: str, cache_dir: str) -> pd.DataFrame:
    """
    Get a summary dataframe of the catalog
        events_dir: Dir with the notebooks
        cache_dir: Dir with the NRSurResults
    """
    catalog = Catalog.load(cache_dir)
    df = __load_processed_links_dataframe(catalog, events_dir)
    posterior_summary = __load_posterior_summary(catalog)

    # merge the posterior summary ('event') with the catalog summary ('event_name') columns
    df = df.merge(posterior_summary, on="event_id")
    df = df.sort_values(by="event_id")
    df = df.drop(columns=["event_id"])
    return df


def __check_fn(fname):
    if not os.path.isfile(fname):
        return ""
    return fname


def __thubnail(fname, event_link):
    if not os.path.isfile(fname):
        return "NA"
    thumbnail = f"{__website__}/_images/{os.path.basename(fname)}"
    thumbnail = f"<img src='{thumbnail}' width='100' height='50'>"
    thumbnail = LINK.format(l=event_link, txt=thumbnail)
    return thumbnail


def __load_processed_links_dataframe(catalog: Catalog, events_dir: str) -> pd.DataFrame:
    event_data = []
    for event in catalog.event_names:
        event_link = f"{__website__}/events/{event}.html"
        event_url = LINK.format(l=event_link, txt=event)
        event_data.append(
            {
                "event_id": event,
                "Event": event_url,
                "Waveform": __thubnail(
                    f"{events_dir}/{event}_waveform.png", event_link
                ),
            }
        )
    return pd.DataFrame(event_data)


def __load_posterior_summary(catalog):
    posterior_summary = catalog.get_latex_summary()
    posterior_summary["event_id"] = posterior_summary.index
    posterior_summary.index = range(len(posterior_summary))
    posterior_summary = posterior_summary.rename(
        columns={p: LATEX_LABELS.get(p, p) for p in posterior_summary.columns.values}
    )
    return posterior_summary


def is_file(f):
    return os.path.exists(f) or os.path.islink(f)
