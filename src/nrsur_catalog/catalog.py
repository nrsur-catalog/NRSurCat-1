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
import plotly.graph_objs as go

import pandas as pd

import numpy as np


class Catalog:
    def __init__(self, events: Dict[str, NRsurResult]):
        self.events = events
        self.df = self.to_posterior_dataframe()

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
        for pos in ["right", "top", "bottom", "left"]:
            ax.spines[pos].set_visible(False)
        ax.set_xticks([])
        ax.set_title(LATEX_LABELS[parameter], fontsize=22)
        ax.set_xlabel(LATEX_LABELS[parameter], fontsize=22)
        ax.grid(True, axis="x", alpha=0.25)
        ax.xaxis.set_tick_params(width=0)
        ax.yaxis.set_tick_params(width=0)
        ax.set_yticks(range(1, self.n + 1))
        ax.set_yticklabels(self.event_names)
        violin_parts = ax.violinplot(data, vert=False)
        for pc in violin_parts["bodies"]:
            pc.set_color(CATALOG_MAIN_COLOR)
        for partname in ("cbars", "cmins", "cmaxes"):
            vp = violin_parts[partname]
            vp.set_edgecolor(CATALOG_MAIN_COLOR)
        min_x = min([min(d) for d in data])
        max_x = max([max(d) for d in data])
        axes_ticks = np.linspace(min_x, max_x, 5)
        ax.set_xticks(axes_ticks)
        plt.tight_layout()
        fig.savefig(f"{parameter}_violin.png", dpi=300, bbox_inches="tight")
        return fig

    def to_posterior_dataframe(self, max_pts=5000):
        """
        Convert the catalog to a pandas dataframe

        Each column is a parameter, each row is a sample.
        The "event" column is the event name.
        """
        dfs = []
        for event_name in self.event_names:
            posterior = self.events[event_name].posterior
            if len(posterior) > max_pts:
                posterior = posterior.sample(max_pts)
            df = posterior
            df["event"] = event_name
            dfs.append(df)
        data = pd.concat(dfs)
        return data

    def interactive_violin_plot(self, parameter):
        df = self.df

        fig = go.Figure()
        fig.add_trace(
            go.Violin(
                x=df[parameter],
                y=df["event"],
                orientation="h",
                line_color="black",
                fillcolor="orange",
                opacity=0.6,
                meanline_visible=True,
                box_visible=True,
            )
        )
        fig.update_layout(
            title=LATEX_LABELS[parameter],
            xaxis_title=LATEX_LABELS[parameter],
            yaxis_title="Event",
            yaxis_zeroline=False,
            xaxis_zeroline=False,
            template="plotly_white",
            width=600,
            height=1200,
        )
        # fig.show()
        fig.write_html("violin2.html")
        fig_widget = go.FigureWidget(fig)
        return fig_widget

    def interactive_violin_2(self, parameter):
        event_names = self.event_names
        df = self.df

        fig = go.Figure()
        for event in event_names:
            fig.add_trace(
                go.Violin(
                    x=df[parameter][df["event"] == event],
                    y=df["event"][df["event"] == event],
                    name=event,
                    orientation="h",
                    box_visible=True,
                    meanline_visible=True,
                )
            )
        fig.update_layout(
            title=LATEX_LABELS[parameter],
            xaxis_title=LATEX_LABELS[parameter],
            yaxis_title="Event",
            yaxis_zeroline=False,
            xaxis_zeroline=False,
            template="plotly_white",
            width=600,
            height=1200,
        )

        # fig.show()
        fig.write_html("violin1.html")
        fig_widget = go.FigureWidget(fig)
        return fig_widget
