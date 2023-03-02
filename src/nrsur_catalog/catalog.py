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
from .utils import LATEX_LABELS, CATALOG_MAIN_COLOR
from plotly.tools import mpl_to_plotly

import numpy as np

class Catalog:
    def __init__(self, events: Dict[str, NRsurResult]):
        self.events = events

    @property
    def n(self):
        return len(self.events)

    @property
    def event_names(self):
        return list(self.events.keys())

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

    def violin_plot(self, parameter: str):
        """Generate a violin plot of a parameter"""
        data = [e.posterior[parameter].values for e in self.events.values()]
        fig, ax = plt.subplots(figsize=(7, self.n))
        ax.tick_params(axis="x", bottom=True, top=True, labelbottom=True, labeltop=True)
        for pos in ['right', 'top', 'bottom', 'left']:
            ax.spines[pos].set_visible(False)
        ax.set_xticks([])
        ax.set_title(LATEX_LABELS[parameter], fontsize=22)
        ax.set_xlabel(LATEX_LABELS[parameter], fontsize=22)
        ax.grid(True, axis='x', alpha=0.25)
        ax.xaxis.set_tick_params(width=0)
        ax.yaxis.set_tick_params(width=0)
        ax.set_yticks(range(1, self.n + 1))
        ax.set_yticklabels(self.event_names)
        violin_parts = ax.violinplot(data, vert=False)
        for pc in violin_parts['bodies']:
            pc.set_color(CATALOG_MAIN_COLOR)
        for partname in ('cbars', 'cmins', 'cmaxes'):
            vp = violin_parts[partname]
            vp.set_edgecolor(CATALOG_MAIN_COLOR)
        min_x  = min([min(d) for d in data])
        max_x = max([max(d) for d in data])
        axes_ticks = np.linspace(min_x, max_x, 5)
        ax.set_xticks(axes_ticks)
        plt.tight_layout()
        return fig

    def interactive_violin_plot(self, parameter):
        return mpl_to_plotly(self.violin_plot(parameter))
