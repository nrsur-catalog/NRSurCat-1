"""Module to download, cache, and read the LVK posteriors"""
import pandas as pd

from nrsur_catalog.api import download_event
from nrsur_catalog.cache import CACHE
import h5py


def get_lvk_posterior(event_name: str) -> pd.DataFrame:
    """Load the LVK posterior for an event"""
    if not CACHE.find(event_name, lvk_posteriors=True):
        download_event(event_name, cache_dir=CACHE.cache_dir, download_lvk=True)
    event_path = CACHE.find(event_name, lvk_posteriors=True)

    res = h5py.File(event_path, "r")['C01:IMRPhenomXPHM']
    df = pd.DataFrame(res['posterior_samples'][:])
    return df
