import contextlib
import os
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bilby.gw.result import CompactBinaryCoalescenceResult

from .api import download_event
from .cache import CACHE
from .logger import logger
from .utils import get_1d_summary_str, get_dir_tree
from .utils import CATALOG_MAIN_COLOR, INTERESTING_PARAMETERS, LATEX_LABELS

pd.set_option("display.max_rows", None, "display.max_columns", None)


class NRsurResult(CompactBinaryCoalescenceResult):
    """Class to store the results of a NRsur event"""

    @classmethod
    def load(
        cls, event_name: str, cache_dir: Optional[str] = CACHE.cache_dir
    ) -> "NRsurResult":
        """Load a CBCResult from the NRSur Catalog"""
        CACHE.cache_dir = cache_dir
        if CACHE.find(event_name) is None:
            logger.debug(f"{event_name} not in {CACHE.event_names}, downloading...")
            download_event(event_name, cache_dir)
        event_path = CACHE.find(event_name)
        r = cls.from_json(event_path)
        r.path_to_result = event_path
        r.outdir = os.path.join("out_nrsur_catalog", event_name)
        r.label = event_name
        os.makedirs(r.outdir, exist_ok=True)
        return r

    def posterior_summary(self):
        """Generate a table of the event parameters"""

        selected_parameters = []
        summary_str = []
        priors = []

        for _, parameters in INTERESTING_PARAMETERS.items():
            for parameter in parameters:
                if parameter in self.posterior:
                    selected_parameters.append(parameter)
                    summary_str.append(get_1d_summary_str(self.posterior[parameter]))
                    priors.append(str(self.priors.get(parameter, "NA")))

        df = pd.DataFrame(
            {
                "Parameter": selected_parameters,
                "Posterior 90% CI": summary_str,
                "Prior": priors,
            }
        )
        df.index = df["Parameter"]
        df = df.drop(columns=["Parameter"])
        return df

    def plot_skymap(self, *args, **kwargs):
        """Generate a skymap of the event"""
        with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
            # call the super class sky map method
            super(NRsurResult, self).plot_skymap()

    def _get_waveform_generator(self):
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
        n_samples=1000,
        level=0.9,
        color=CATALOG_MAIN_COLOR,
        polarisation="plus",
        outdir="",
    ):
        """Generate a signal plot of the event

        Parameters
        ----------
        n_samples: int
            The number of samples to use in the plot
        level: float
            The credible level to use in the plot (default 0.9)

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
        waveform_generator = self._get_waveform_generator()

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
            waveform_generator = self._get_waveform_generator()
            base_wf = waveform_generator.time_domain_strain(base_params)[polarisation]

        time_idx = np.arange(len(base_wf))
        waveforms = np.zeros((n_samples, len(base_wf)))

        for i, params in samples.iterrows():
            params = dict(params)
            waveforms[i] = waveform_generator.time_domain_strain(params)[polarisation]
        # roll all waveforms halfway
        waveforms = np.roll(waveforms, len(base_wf) // 2, axis=1)

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
        parameters=None,
        priors=None,
        titles=True,
        save=False,
        filename=None,
        dpi=300,
        **kwargs,
    ):
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

    def print_configs(self):
        logger.info("To be implemented...")

    def download_analysis_datafiles(self, outdir=None):
        if outdir is None:
            outdir = f"outdir_{self.label}"
        logger.info(f"Saving files to {outdir}")
        logger.info("To be implemented...")
        logger.info("Downloading analysis strain")
        logger.info("Downloading PSDs")
        logger.info("Downloading calibration files")
        logger.info("writing analysis config file")
        logger.info(f"Files:\n{get_dir_tree(outdir)}")
