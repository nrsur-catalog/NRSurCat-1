import contextlib
import os
from typing import Optional, List, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bilby.gw.result import CompactBinaryCoalescenceResult
from .utils import plot_overlaid_corner

from bilby.gw.waveform_generator import WaveformGenerator

from .api import download_event
from .cache import CatalogCache, DEFAULT_CACHE_DIR
from .logger import logger
from .utils import get_1d_summary_str, get_dir_tree, pesummary_to_bilby_result
from .utils import CATALOG_MAIN_COLOR, INTERESTING_PARAMETERS, LATEX_LABELS, prior_to_str
from .lvk_posterior import load_lvk_result

pd.set_option("display.max_rows", None, "display.max_columns", None)


class NRsurResult(CompactBinaryCoalescenceResult):
    """Class to interface with a result of a NRSur Catalog analysis."""

    def __init__(self, *args, **kwargs):
        super(NRsurResult, self).__init__(*args, **kwargs)
        self._lvk_result = None

    @classmethod
    def load(
            cls,
            event_name: str,
            cache_dir: Optional[str] = DEFAULT_CACHE_DIR,
            event_path: Optional[str] = None,
    ) -> "NRsurResult":
        """Load a result (either by downloading or from a local dir).

        Parameters
        ----------
        event_name: str
            The name of the event to load
            (list all available events with `nrsur_catalog.catalog.Catalog.
        cache_dir: Optional[str]
            The credible level to use in the plot (default 0.9)
        event_path: Optional[str] = None
            The path to the NRSur result file to load.

        Returns
        -------
        NRsurResult: loaded result object.

        """

        CACHE = CatalogCache(cache_dir)
        if not CACHE.find(event_name) and event_path is None:
            logger.debug(f"{event_name} not in {CACHE.dir}. Downloading...")
            download_event(event_name, cache_dir)

        if event_path is None:
            event_path = CACHE.find(event_name)

        if event_path is None:
            raise ValueError(f"Event {event_name} not found.")

        r = pesummary_to_bilby_result(event_path)
        r.path_to_result = event_path
        r.outdir = os.path.join(CACHE.dir, event_name)
        r.label = event_name
        os.makedirs(r.outdir, exist_ok=True)
        r.__class__ = NRsurResult
        logger.debug(f"Loaded NRresult {event_name} from {event_path}")
        return r

    def summary(self, markdown: bool = False) -> Union[str, pd.DataFrame]:
        """Generate a table of the event parameter summary statistics.

        Parameters
        ----------
        markdown: bool
            True, return a string-markdown table of the summary
            False, return a pd.DataFrame of the summary.
        """

        selected_parameters = []
        summary_str = []
        priors = []

        for _, parameters in INTERESTING_PARAMETERS.items():
            for parameter in parameters:
                if parameter in self.posterior:
                    selected_parameters.append(LATEX_LABELS[parameter])
                    summary_str.append(get_1d_summary_str(self.posterior[parameter]))
                    pri = self.priors.get(parameter, "$-$")
                    if pri != "$-$":
                        pri = prior_to_str(pri)
                    priors.append(pri)

        df = pd.DataFrame(
            {
                "Parameter": selected_parameters,
                "Posterior 90% CI": summary_str,
                "Prior": priors,
            }
        )
        df.index = df["Parameter"]
        df = df.drop(columns=["Parameter"])
        if markdown:
            md_txt = df.to_markdown()
            md_txt = "\n".join([f"# {line}" for line in md_txt.splitlines()])
            return "\n" + md_txt
        else:
            return df

    def plot_skymap(self, *args, **kwargs):
        """Generate a skymap of the event"""
        with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
            # call the super class sky map method
            super(NRsurResult, self).plot_skymap()

    def __get_waveform_generator(self) -> WaveformGenerator:
        return self.waveform_generator_class(
            duration=self.duration,
            sampling_frequency=self.sampling_frequency,
            start_time=self.start_time,
            frequency_domain_source_model=self.frequency_domain_source_model,
            parameter_conversion=self.parameter_conversion,
            waveform_arguments=self.waveform_arguments,
        )
    def plot_signal(
            self,
            n_samples: Optional[int] = 1000,
            level: Optional[float] = 0.9,
            color: Optional[str] = CATALOG_MAIN_COLOR,
            polarisation: Optional[str] = "plus",
            outdir: Optional[str] = "",
    )->Union[plt.Figure, None]:
        """Generate a signal plot of the event

        Parameters
        ----------
        n_samples: int
            The number of samples to use in the plot
        level: float
            The credible level to use in the plot (default 0.9)
        color: str
            The color of the waveform.
        polarisation: str
            The polarisation to plot
        outdir:str
            The outdir to save the plot. If '' not saved.

        """

        if n_samples > len(self.posterior):
            n_samples = len(self.posterior)
            logger.warning(
                "n_samples > len(posterior), using n_samples = len(posterior)"
            )

        samples = self.posterior.sample(n_samples, replace=False)
        samples = samples.reset_index(drop=True)
        base_params = dict(samples.iloc[0])

        delta = (1 + level) / 2
        upper_percentile = delta * 100
        lower_percentile = (1 - delta) * 100
        ci = int(upper_percentile - lower_percentile)

        # Generate the plotting data
        waveform_generator = self.__get_waveform_generator()

        try:
            # suppress stdout
            with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
                base_wf = waveform_generator.time_domain_strain(base_params)[
                    polarisation
                ]
        except RuntimeError:
            logger.warning(
                "Unable to create a waveform: do you have NrSur7dq4 installed? Defaulting to IMRPhenomPv2"
            )
            self.waveform_arguments["waveform_approximant"] = "IMRPhenomPv2"
            self.waveform_arguments['minimum_frequency'] = 20
            waveform_generator = self.__get_waveform_generator()
            base_wf = waveform_generator.time_domain_strain(base_params)[polarisation]

        time_idx = np.arange(len(base_wf))
        waveforms = np.zeros((n_samples, len(base_wf)))

        for i, params in samples.iterrows():
            params = dict(params)
            waveforms[i] = waveform_generator.time_domain_strain(params)[polarisation]
        waveforms = np.roll(waveforms, 4 * len(base_wf) // 5, axis=1)

        median = np.median(waveforms, axis=0)
        lower, upper = np.quantile(
            waveforms, [lower_percentile / 100, upper_percentile / 100], axis=0
        )

        # Plot the data
        fig, ax = plt.subplots(1, 1, figsize=(6, 5))
        ax.plot(time_idx, median, color=color)
        ax.fill_between(
            time_idx,
            lower,
            upper,
            alpha=0.3,
            label=f"{ci}% credible region",
            color=color,
            linewidth=0,
        )
        ax.axis("off")
        outdir = self.outdir if outdir == "" else outdir
        filename = os.path.join(outdir, self.label + "_waveform.png")
        fig.tight_layout()
        fig.savefig(filename, dpi=300, bbox_inches="tight", transparent=True)
        return fig

    def plot_corner(
            self,
            parameters: Optional[List[str]] = None,
            priors: Optional[bool] = None,
            titles: Optional[List[str]] = True,
            save: Optional[bool] = False,
            filename: Optional[str] = None,
            dpi: Optional[int] = 300,
            **kwargs,
    )->Union[plt.Figure, None]:
        labels = []
        if parameters is not None:
            labels = [LATEX_LABELS[p] for p in parameters]
        if not "labels" in kwargs:
            kwargs["labels"] = labels
        if not "color" in kwargs:
            kwargs["color"] = CATALOG_MAIN_COLOR

        return super(NRsurResult, self).plot_corner(
            parameters, priors, titles, save, filename, dpi, **kwargs
        )

    def plot_lvk_comparison_corner(self, parameters: List[str], **kwargs):
        """Plot a corner plot comparing the posterior to the LVK catalog."""
        return plot_overlaid_corner(
            r1=self, r2=self.lvk_result, parameters=parameters,
            labels=["NRSur7dq4", "LVK [XPHM]"],
            colors=[CATALOG_MAIN_COLOR, "tab:blue"],
            **kwargs,
        )

    def print_configs(self)->str:
        configs = self.meta_data["config_file"]
        for key, config in configs.items():
            k = f"{key}:"
            print(f"{k:<35} {config}")

    def download_analysis_datafiles(self, outdir:str):
        """Downloads all the analysis datafiles -- CURRENTLY NOT IMPLEMENTED.
        Please raise a git-issue if this is something you would like us to add.
        """
        if outdir is None:
            outdir = f"outdir_{self.label}"
        raise NotImplementedError(
            "Please raise a git-issue if this is something that you would "
            "really like us to include.")
        logger.info(f"Saving files to {outdir}")
        logger.info("To be implemented...")
        logger.info("Downloading analysis strain")
        logger.info("Downloading PSDs")
        logger.info("Downloading calibration files")
        logger.info("writing analysis config file")
        logger.info(f"Files:\n{get_dir_tree(outdir)}")

    @property
    def lvk_result(self)->CompactBinaryCoalescenceResult:
        """The event's corresponding LVK result (from the GWTC)."""
        if not hasattr(self, "_lvk_result"):
            self._lvk_result = load_lvk_result(self.label, cache_dir=os.path.dirname(self.outdir))
            logger.debug(f"Loaded LVKresult{self.label}")
        return self._lvk_result
