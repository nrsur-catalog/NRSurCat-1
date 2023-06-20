import pandas as pd
from nrsur_catalog import Catalog
from nrsur_catalog.utils import get_event_name, LATEX_LABELS

import os, glob


def get_catalog_summary(events_dir:str, cache_dir:str)->pd.DataFrame:
    """
    Get a summary dataframe of the catalog
    """
    catalog = Catalog.load(cache_dir)

    webroot = 'https://cjhaster.com/NRSurrogateCatalog'
    LINK = "<a href='{l}'> {txt}</a>"


    event_ipynb = glob.glob(f"{events_dir}/GW*.ipynb")
    event_waveform = glob.glob(f"{events_dir}/*waveform.png")
    event_name = [get_event_name(os.path.basename(f)) for f in event_ipynb]
    event_link = [f"{webroot}/events/{n}.html" for n in event_name]

    thumbnails = [f"{webroot}/_images/{os.path.basename(f)}" for f in event_waveform]
    thumbnails = [f"<img src='{f}' height='100'>" for f in thumbnails]
    thumbnails = [LINK.format(l=l, txt=t) for l, t in zip(event_link, thumbnails)]
    event = [LINK.format(l=l, txt=t) for l, t in zip(event_link, event_name)]

    df = pd.DataFrame({
        'event_id': event_name,
        "Event": event,
        " ": thumbnails,
    })
    posterior_summary = catalog.get_latex_summary()
    posterior_summary['event_id'] = posterior_summary.index
    posterior_summary.index = range(len(posterior_summary))
    posterior_summary = posterior_summary.rename(columns={
        p: LATEX_LABELS.get(p, p) for p in  posterior_summary.columns.values}
    )

    # merge the posterior summary ('event') with the catalog summary ('event_name') columns
    df = df.merge(posterior_summary, on='event_id')
    df = df.sort_values(by="event_id")
    # drop 'event' column
    df = df.drop(columns=['event_id'])
    df.set_index('Event', inplace=True)
    return df

