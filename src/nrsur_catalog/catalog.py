"""Module to load all the catalog events and make plots with them"""
from tqdm.auto import tqdm
from .nrsur_result import NRsurResult
from typing import Dict, Optional
import matplotlib.pyplot as plt
from glob import glob
from .utils import get_event_name

from .cache import CACHE
from .logger import logger
from .api.download_event import download_all_events


class Catalog:
    def __init__(self, events: Dict[str, NRsurResult]):
        self.events = events

    @classmethod
    def load(cls, cache_dir: Optional[str] = CACHE.cache_dir) -> "Catalog":
        """Load the catalog from the cache"""
        CACHE.cache_dir = cache_dir
        if CACHE.is_empty:
            logger.warning("Cache is empty, downloading all events...")
            download_all_events(CACHE.cache_dir)
        events = Catalog.load_events(cache_dir)
        return cls(events)

    @staticmethod
    def load_events(events_dir: str) -> Dict[str, NRsurResult]:
        events = {}
        event_paths = glob(f"{events_dir}/*.json")
        for path in tqdm(event_paths, desc="Loading events"):
            event_name = get_event_name(path)
            events[event_name] = NRsurResult.load(event_name)
        return events

    def violin_plot(self, parameter: str, **kwargs):
        """Generate a violin plot of a parameter"""
        fig, ax = plt.subplots()
        data = [event.posterior[parameter] for event in self.events.values()]
        ax.violinplot(data, **kwargs)
        return fig

    def plot_bayes_factors(self,  **kwargs):
        """Generate a plot of the Bayes Factors"""
        fig, ax = plt.subplots()
        data = [event.bayes_factor for event in self.events.values()]
        ax.hist(data, **kwargs)
        return fig
