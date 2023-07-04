"""Module to load all the catalog events and make plots with them"""
import os.path

from matplotlib.ticker import AutoMinorLocator
from tqdm.auto import tqdm
from .nrsur_result import NRsurResult

from typing import Dict, Optional, List, Union
import matplotlib.pyplot as plt
from glob import glob
from .utils import get_event_name, format_qts_to_latex

from .cache import CatalogCache, DEFAULT_CACHE_DIR, NR_FILE_EXTENSION
from .logger import logger
from .api import download_missing_events, get_analysed_event_names

from .utils import LATEX_LABELS, CATALOG_MAIN_COLOR, INTERESTING_PARAMETERS
from corner import hist2d

import h5py
import pandas as pd
from itertools import chain
import numpy as np

POSTERIORS_TO_KEEP = list(chain.from_iterable(v for v in INTERESTING_PARAMETERS.values()))
# POSTERIORS_TO_KEEP += ["log_likelihood", "log_prior"]
MAX_SAMPLES = 10000
CATALOG_FN = "downsampled_posteriors.h5"

DEFAULT_CLEAN_CATALOG = True

class Catalog:
    def __init__(self, posteriors: pd.DataFrame):
        """Class to store the catalog events

        Parameters
        -----------
        posteriors: pd.DataFrame
            A dataframe with the catalog posteriors
            The dataframe must have an `event` column with the event name
        """
        self._df = posteriors
        # sort by event name (GW150914, GW151012, ...)
        self._df = self._df.sort_values("event")

    @classmethod
    def load(
            cls,
            cache_dir: Optional[str] = DEFAULT_CACHE_DIR,
            max_samples:Optional[int]=MAX_SAMPLES,
            clean:Optional[bool]=DEFAULT_CLEAN_CATALOG
    ) -> "Catalog":
        """Load all the catalog posterior samples and stores a cache of the down-sampled posteriors.

        Parameters
        ----------
        cache_dir: Optional[str]
            The cache-dir where the NRSurrogate results will be loaded from.
            If empty, downloads all the NRSurrogate results.
        max_samples: Optional[int]
            The max number of samples to include from each event's posterior.
        clean: Optional[bool]
            Recomputes the cache of the downsampled-posteriors.
        """
        CACHE = CatalogCache(cache_dir)
        fname = f"{cache_dir}/{CATALOG_FN}"

        if not clean and os.path.isfile(fname):
            logger.info(f"Loading catalog from {fname}")
            catalog = cls(Catalog.from_hdf5(fname))
        else:
            if CACHE.is_incomplete:
                logger.warning(f"Cache {cache_dir} is missing some events, downloading events...")
                download_missing_events(CACHE.dir)
            df = Catalog.__load_events(cache_dir, max_samples=max_samples)
            catalog = cls(df)
            catalog.save(f"{cache_dir}/{CATALOG_FN}")
        return catalog

    @staticmethod
    def __load_events(events_dir: str, max_samples:int=MAX_SAMPLES) -> pd.DataFrame:
        """Helped method to load the posteriors from the Cache dir."""
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

    def to_dict_of_posteriors(self, parameters:Optional[List[str]]=None) -> Dict[str, pd.DataFrame]:
        """Return a dictionary of event:posteriors.

        Parameters
        ----------
        parameters: Optional[List[str]]
            List of the parameters to include in the posterior.


        Returns
        -------
        Dict[str:pd.DataFrame]: Returns a dictionary of {events: event_posteriors}.

        """
        if parameters is None:
            parameters = POSTERIORS_TO_KEEP
        return {
            e: self._df[self._df['event'] == e][parameters]
            for e in self.event_names
        }

    def save(self, path: str)->None:
        """Cache the loaded catalog to a hdf5 file.

        Parameters
        ---------
        path: str
            Path to save the cache-catalog

        """
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

    def violin_plot(self, parameter: str)->plt.Figure:
        """Generate a violin plot of a parameter."""
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
        """Return posterior quantiles for each event's posteriors.

        Parameters
        ----------
        quantiles: List of floats marking the quantiles.

        """
        quant_df = self._df.groupby("event").quantile(quantiles)
        quant_df.index = quant_df.index.rename(["event", "quantile"])
        return quant_df

    @property
    def event_names(self) -> List[str]:
        """Return a list of loaded events in the catalog object"""
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

    def plot_2d_posterior(
            self,
            parm_x:str,
            parm_y:str,
            scatter_medians:Optional[bool]=True,
            event_posteriors:Optional[bool]=False,
            event_quantiles:Optional[bool]=True,
            contour_all_posterior_samples:Optional[bool]=True,
            colors:Optional[Union[str, List[str]]]=CATALOG_MAIN_COLOR
    )->plt.Figure:
        """
        Plot a 2D posterior for all events in the catalog

        Parameters
        ----------
        parm_x:str
            The parameter plotted along the x-axis (e.g. mass_1, chi_eff...)
        parm_y:str
            The parameter plotted along the y-axis (e.g. mass_1, chi_eff...)
        scatter_medians:Optional[bool]=True
            Scatter median values of each event.
        event_posteriors:Optional[bool]=False
            Outline the event posterior.
        event_quantiles:Optional[bool]=True
            Plot the 68% CI quantiles of each event's posterior.
        contour_all_posterior_samples:Optional[bool]=True
            Plot contours around all the posterior samples
            (regardless of which event each sample belongs to)
        colors:Optional[Union[str, List[str]]]
            The color to be used for each event.
            If a string, the same color will be used for each event.

        Returns
        -------
        plt.Figure: A matplotlib figure with the plot.
        """
        fig, ax = plt.subplots(figsize=(5, 5))
        if isinstance(colors, str):
            colors=[colors] * self.n

        if event_posteriors or contour_all_posterior_samples:
            if event_posteriors:
                linewidths = 0.2
            else:
                linewidths = 0

            for i, event in enumerate(self.event_names):
                data = self.get_event_posterior(event)[[parm_x, parm_y]]
                hist2d(
                    ax=ax, x=data[parm_x].values, y=data[parm_y].values, color=colors[i],
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
                x, y = posterior_quantiles.loc[event].values[1]
                xlow, ylow = posterior_quantiles.loc[event].values[0]
                xhigh, yhigh = posterior_quantiles.loc[event].values[2]
                ax.scatter(x, y, color=colors[i], s=0.5)
                if event_quantiles:
                    ax.errorbar(
                        x, y,
                        xerr=[[x - xlow], [xhigh - x]], yerr=[[y - ylow], [yhigh - y]],
                        fmt='none', color=colors[i], alpha=0.2, capsize=0,
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

    def get_all_posteriors(self) -> pd.DataFrame:
        """Return the dataframe of all the event posteriors concatenated together.
        The column 'event' denotes which 'event' the posterior sample belongs to.

        Returns
        -------
        pd.DataFrame: A dataframe of the all event's posterior samples.
        """
        return self._df.copy()

    def get_event_posterior(self, event_name: str) -> pd.DataFrame:
        """
        Return a dataframe with the posterior for a given event.

        Parameter
        ---------
        event_name:str
            The name of the event that will have its posterior returned.

        Returns
        -------
        pd.DataFrame: A dataframe of the event's posterior samples
        """
        return self._df[self._df['event'] == event_name]

    @staticmethod
    def get_analysed_event_names() -> List[str]:
        """Return the list of the analysed events available in the NRSurrogate Catalog.

        Returns
        -------
        List[str]: List of the analysed event names.
        """
        return get_analysed_event_names()

    @property
    def all_analysed_events_loaded(self)->bool:
        """True if all analysed events have been loaded
        (this will be False when the Catalog object is created
        before all event results have been downloaded).
        """
        analysed_events = set(self.get_analysed_event_names())
        loaded_events = set(self.event_names)
        return len(analysed_events-loaded_events)==0