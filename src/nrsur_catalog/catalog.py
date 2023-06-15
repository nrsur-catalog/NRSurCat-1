"""Module to load all the catalog events and make plots with them"""
import os.path

from tqdm.auto import tqdm
from .nrsur_result import NRsurResult

from typing import Dict, Optional
import matplotlib.pyplot as plt
from glob import glob
from .utils import get_event_name

from .cache import CatalogCache, DEFAULT_CACHE_DIR, NR_FILE_EXTENSION
from .logger import logger
from .api.download_event import download_all_events
from .utils import LATEX_LABELS, CATALOG_MAIN_COLOR, INTERESTING_PARAMETERS
import plotly.graph_objs as go

import h5py
import pandas as pd
from itertools import chain
import numpy as np

POSTERIORS_TO_KEEP = list(chain.from_iterable(v for v in INTERESTING_PARAMETERS.values()))
# POSTERIORS_TO_KEEP += ["log_likelihood", "log_prior"]
MAX_SAMPLES = 10000
CATALOG_FN = "downsampled_posteriors.h5"


class Catalog:
    def __init__(self, posteriors: pd.DataFrame):
        """Class to store the catalog events

        posteriors: pd.DataFrame
            A dataframe with the catalog posteriors
            The dataframe must have an `event` column with the event name
        """
        self._df = posteriors
        # sort by event name (GW150914, GW151012, ...)
        self._df = self._df.sort_values("event")
        self.event_names = self._df.event.unique()
        self.n = len(self.event_names)

    @classmethod
    def load(cls, cache_dir: Optional[str] = DEFAULT_CACHE_DIR, max_samples=MAX_SAMPLES, clean=True) -> "Catalog":
        """Load the catalog from the cache"""
        CACHE = CatalogCache(cache_dir)
        fname = f"{cache_dir}/{CATALOG_FN}"

        if not clean and os.path.isfile(fname):
            logger.info(f"Loading catalog from {fname}")
            catalog = cls(Catalog.from_hdf5(fname))
        else:
            if CACHE.is_empty:
                logger.warning("Cache is empty, downloading all events...")
                download_all_events(CACHE.dir)
            df = Catalog.load_events(cache_dir, max_samples=max_samples)
            catalog = cls(df)
            catalog.save(f"{cache_dir}/{CATALOG_FN}")
        return catalog

    @staticmethod
    def load_events(events_dir: str, max_samples=MAX_SAMPLES) -> pd.DataFrame:
        event_paths = glob(f"{events_dir}/*{NR_FILE_EXTENSION}")
        dfs = []
        assert len(event_paths) > 0, f"No events found in {events_dir}"
        for path in tqdm(event_paths, desc="Loading events"):
            event_name = get_event_name(path)

            r = NRsurResult.load(event_name, event_path=path)
            posterior = r.posterior[POSTERIORS_TO_KEEP]
            if len(r.posterior) > max_samples:
                logger.debug(
                    f"Event {event_name} has {len(r.posterior)}>{max_samples} samples, "
                    f"downsampling to {max_samples} samples"
                )
                posterior = posterior.sample(max_samples, weights=r.posterior.log_likelihood)
            posterior['event'] = event_name
            dfs.append(posterior)
        return pd.concat(dfs)

    def to_dict_of_posteriors(self, parameters=None) -> Dict[str, pd.DataFrame]:
        """Return a dictionary of posteriors"""
        if parameters is None:
            parameters = POSTERIORS_TO_KEEP
        return {
            e: self._df[self._df['event'] == e][parameters]
            for e in self.event_names
        }

    def save(self, path: str):
        """Save the catalog to a hdf5 file"""
        assert path.endswith(".h5"), "Path must end with .h5"
        data = self.to_dict_of_posteriors()
        with h5py.File(path, "w") as f:
            for event_name, posterior in data.items():
                # write each posterior to a different key in the hdf5 file
                f.create_dataset(event_name, data=posterior.to_records(index=False))

    @staticmethod
    def from_hdf5(path: str) -> pd.DataFrame:
        """Load the catalog from a hdf5 file"""
        assert path.endswith(".h5"), "Path must end with .h5"
        with h5py.File(path, "r") as f:
            posteriors = []
            for key in f:
                df = pd.DataFrame(f[key][:])
                df['event'] = key
                posteriors.append(df)
            return pd.concat(posteriors)

    def violin_plot(self, parameter: str):
        """Generate a violin plot of a parameter"""
        # posterior subsets for each event
        data = [post.values.ravel() for post in self.to_dict_of_posteriors([parameter]).values()]
        means = [np.mean(d) for d in data]

        # sort by mean
        ylabels = [e for _, e in sorted(zip(means, self.event_names))]
        data = [d for _, d in sorted(zip(means, data), key=lambda x: x[0])]

        fig, ax = plt.subplots(figsize=(7, self.n * 0.8))
        ax.tick_params(axis="x", bottom=True, top=True, labelbottom=True, labeltop=True)
        for pos in ["right", "top", "bottom", "left"]:
            ax.spines[pos].set_visible(False)
        ax.set_xticks([])
        ax.set_title(LATEX_LABELS[parameter], fontsize=22)
        ax.set_xlabel(LATEX_LABELS[parameter], fontsize=22)
        ax.grid(True, axis="x", alpha=0.25)
        ax.xaxis.set_tick_params(width=0)
        ax.yaxis.set_tick_params(width=0)
        ax.set_yticks(range(1, self.n + 1))
        ax.set_yticklabels(ylabels)
        violin_parts = ax.violinplot(data, vert=False)
        for pc in violin_parts["bodies"]:
            pc.set_color(CATALOG_MAIN_COLOR)
        for partname in ("cbars", "cmins", "cmaxes"):
            vp = violin_parts[partname]
            vp.set_edgecolor(CATALOG_MAIN_COLOR)
        min_x = min([min(d) for d in data])
        max_x = max([max(d) for d in data])
        axes_ticks = np.linspace(min_x, max_x, 5)
        ax.set_ylim(0.5, self.n + 0.5)
        ax.set_xticks(axes_ticks)

        # annotate a group number every 7 y ticks
        ntics = 7
        for i in range(6, self.n, ntics):
            for xval in axes_ticks:
                ax.text(
                    xval,
                    i + 1.5,
                    f"{xval:.1f}",
                    fontsize=12,
                    ha="center",
                    va="center",
                    color="black",
                    alpha=0.25,
                )

        plt.tight_layout()
        fig.savefig(f"{parameter}_violin.png", dpi=300, bbox_inches="tight")
        return fig
