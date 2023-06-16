import os

import pandas as pd
from bilby.gw.result import CBCResult
from typing import List
from matplotlib.lines import Line2D


def plot_overlaid_corner(r1: CBCResult, r2: CBCResult, parameters: List[str], labels:List[str], colors: List[str]):
    # ensure parameters are in both results posteriors
    _check_list_is_subset(parameters, list(r1.posterior.columns))
    _check_list_is_subset(parameters, list(r2.posterior.columns))

    # plot corner
    fig = r1.plot_corner(parameters=parameters, color=colors[0], save=False, titles=True)
    fig = r2.plot_corner(parameters=parameters, color=colors[1], fig=fig, save=False, quantiles=[], titles=False)

    # add legend to figure to right using the following colors
    legend_elements = [Line2D([0], [0], color=c, lw=4, label=l) for c, l in zip(colors, labels)]
    fig.legend(
        handles=legend_elements, loc="upper right", bbox_to_anchor=(0.95, 0.95),
        bbox_transform=fig.transFigure,
        frameon=False, fontsize=16)

    return fig


def _check_list_is_subset(l1, l2):
    s1 = set(l1)
    s2 = set(l2)
    if not s1.issubset(s2):
        raise ValueError(f"Missing parameters: {s1.difference(s2)}")



def posterior_to_result(posterior:pd.DataFrame, label=""):
    """Convert a pandas DataFrame to a bilby.gw.result.CBCResult"""
    return CBCResult(
        label=label,
        search_parameter_keys=list(posterior.columns),
        posterior=posterior,
    )
