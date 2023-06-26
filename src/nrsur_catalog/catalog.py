"""Module to load all the catalog events and make plots with them"""
import os.path

from matplotlib.ticker import AutoMinorLocator
from tqdm.auto import tqdm
from .nrsur_result import NRsurResult

from typing import Dict, Optional, List
import matplotlib.pyplot as plt
from glob import glob
from .utils import get_event_name, format_qts_to_latex

from .cache import CatalogCache, DEFAULT_CACHE_DIR, NR_FILE_EXTENSION
from .logger import logger
from .api.download_event import download_all_events
from .utils import LATEX_LABELS, CATALOG_MAIN_COLOR, INTERESTING_PARAMETERS, LOG_PARAMS
import plotly.graph_objs as go
from corner import hist2d
import seaborn as sns

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

    @classmethod
    def load(cls, cache_dir: Optional[str] = DEFAULT_CACHE_DIR, max_samples=MAX_SAMPLES, clean=False) -> "Catalog":
        """Load the catalog from the cache"""
        CACHE = CatalogCache(cache_dir)
        fname = f"{cache_dir}/{CATALOG_FN}"

        if not clean and os.path.isfile(fname):
            logger.info(f"Loading catalog from {fname}")
            catalog = cls(Catalog.from_hdf5(fname))
        else:
            if CACHE.is_empty:
                logger.warning(f"Cache {cache_dir} is empty, downloading all events...")
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
        event_paths = sorted(event_paths, key=get_event_name)
        for path in tqdm(event_paths, desc="Loading events"):
            event_name = get_event_name(path)

            r = NRsurResult.load(event_name, event_path=path)
            missing_params = set(POSTERIORS_TO_KEEP) - set(r.posterior.columns)
            if len(missing_params) > 0:
                logger.warning(
                    f"Event {event_name} does not have all the required parameters. Missing:"
                    f"{missing_params}. Adding mock data..."
                )
                for p in missing_params:
                    r.posterior[p] = np.nan
            posterior = r.posterior[POSTERIORS_TO_KEEP]
            if len(r.posterior) > max_samples:
                logger.debug(
                    f"Event {event_name} has {len(r.posterior)}>{max_samples} samples, "
                    f"downsampling to {max_samples} samples"
                )
                posterior = posterior.sample(max_samples, weights=r.posterior.log_likelihood)
            posterior.loc[:, "event"] = event_name
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

    @property
    def parameters(self) -> List[str]:
        """Return a list of parameters in the catalog"""
        p = list(self._df.columns)
        p.remove('event')
        return p

    def get_posterior_quantiles(self, quantiles=[0.16, 0.5, 0.84]) -> pd.DataFrame:
        """Compute posterior quantiles for each event's posteriors"""
        quant_df = self._df.groupby("event").quantile(quantiles)
        quant_df.index = quant_df.index.rename(["event", "quantile"])
        return quant_df

    @property
    def event_names(self) -> List[str]:
        """Return a list of events in the catalog"""
        return list(self._df.event.unique())

    @property
    def n(self) -> int:
        """Return the number of events in the catalog"""
        return len(self.event_names)

    def get_latex_summary(self) -> pd.DataFrame:
        """
        Return a dataframe with the median and 68% credible interval for each parameter
        """
        post_quantiles = self.get_posterior_quantiles()
        latex_summary = {}
        for event in self.event_names:
            event_data = {}
            for param in self.parameters:
                event_quants = post_quantiles.loc[event, param].values
                event_data[param] = format_qts_to_latex(*event_quants)
            latex_summary[event] = event_data

        latex_summary = pd.DataFrame(latex_summary).T
        latex_summary.index.name = "event"
        return latex_summary

    def get_event_posterior(self, event_name: str) -> pd.DataFrame:
        """
        Return a dataframe with the posterior for a given event
        """
        return self._df[self._df['event'] == event_name]

    def plot_2d_posterior(
            self, parm_x, parm_y,
            scatter_medians=True,
            event_posteriors=False,
            event_quantiles=True,
            all_catalog_samples=True,
            color_by_event=False,
            color=CATALOG_MAIN_COLOR
    ):
        """
        Plot a 2D posterior for all events in the catalog
        """
        fig, ax = plt.subplots(figsize=(5, 5))



        if event_posteriors or all_catalog_samples:
            if event_posteriors:
                linewidths = 0.2
            else:
                linewidths = 0

            for i, event in enumerate(self.event_names):
                data = self.get_event_posterior(event)[[parm_x, parm_y]]
                color = f'C{i}' if color_by_event else color
                hist2d(
                    ax=ax, x=data[parm_x].values, y=data[parm_y].values, color=color,
                    bins=50, zorder=-2, alpha=0.1,
                    plot_datapoints=False,
                    plot_density=False,
                    plot_contours=True,
                    no_fill_contours=False,
                    fill_contours=True,
                    levels=[0, 1.0 - np.exp(-0.5 * 2.1 ** 2)],
                    smooth=1.1,
                    contourf_kwargs=dict(linewidths=linewidths),
                    contour_kwargs=dict(linewidths=linewidths),

                )

        if scatter_medians:
            posterior_quantiles = self.get_posterior_quantiles()
            posterior_quantiles = posterior_quantiles[[parm_x, parm_y]]
            for i, event in enumerate(self.event_names):
                color = f'C{i}' if color_by_event else color
                x, y = posterior_quantiles.loc[event].values[1]
                xlow, ylow = posterior_quantiles.loc[event].values[0]
                xhigh, yhigh = posterior_quantiles.loc[event].values[2]
                ax.scatter(x, y, color=color, s=0.5)
                if event_quantiles:
                    ax.errorbar(
                        x, y,
                        xerr=[[x - xlow], [xhigh - x]], yerr=[[y - ylow], [yhigh - y]],
                        fmt='none', color=color, alpha=0.2, capsize=0,
                    )

        # add minor ticks
        ax.set_xlim(min(self._df[parm_x]), max(self._df[parm_x]))
        ax.set_ylim(min(self._df[parm_y]), max(self._df[parm_y]))
        ax.tick_params(
            axis='both', which='both', direction='in',
            top=True, right=True, labelsize=12, pad=5)
        ax.tick_params(axis='x', pad=10)
        # add minor ticks
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(axis='both', which='major', length=8)
        ax.tick_params(axis='both', which='minor', length=4)
        ax.set_xlabel(LATEX_LABELS[parm_x])
        ax.set_ylabel(LATEX_LABELS[parm_y])
        plt.tight_layout()
        return fig


    def get_data(self)->pd.DataFrame:
        return self._df.copy()