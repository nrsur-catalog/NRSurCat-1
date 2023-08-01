"""Module to download, cache, and read the LVK posteriors"""
import h5py
import pandas as pd
from bilby.gw.result import CBCResult

from nrsur_catalog.api import download_event
from nrsur_catalog.cache import DEFAULT_CACHE_DIR, LVK_LABEL, CatalogCache

from .logger import logger


def load_lvk_result(event_name: str, cache_dir=DEFAULT_CACHE_DIR) -> CBCResult:
    """Load the LVK posterior for an event"""
    CACHE = CatalogCache(cache_dir)
    if not CACHE.find(event_name, lvk_posteriors=True):
        logger.debug(f"LVK {event_name} not in {CACHE.dir}. Downloading...")
        download_event(event_name, cache_dir=CACHE.dir, download_lvk=True)
    event_path = CACHE.find(event_name, lvk_posteriors=True, hard_fail=True)

    with h5py.File(event_path, "r") as f:
        res = f[LVK_LABEL]
        df = pd.DataFrame(res["posterior_samples"][:])

    return CBCResult(
        label="LVK [XPHM]",
        posterior=df,
        search_parameter_keys=list(df.columns),
    )
