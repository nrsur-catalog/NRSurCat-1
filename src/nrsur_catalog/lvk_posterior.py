"""Module to download, cache, and read the LVK posteriors"""
import pandas as pd

from nrsur_catalog.api import download_event
from nrsur_catalog.cache import CatalogCache, LVK_LABEL
import h5py


def get_lvk_posterior(event_name: str, cache_dir='.') -> pd.DataFrame:
    """Load the LVK posterior for an event"""
    CACHE = CatalogCache(cache_dir)
    if not CACHE.find(event_name, lvk_posteriors=True):
        download_event(event_name, cache_dir=CACHE.dir, download_lvk=True)
    event_path = CACHE.find(event_name, lvk_posteriors=True, hard_fail=True)

    with h5py.File(event_path, "r") as f:
        res = f[LVK_LABEL]
        df = pd.DataFrame(res['posterior_samples'][:])

    return df
