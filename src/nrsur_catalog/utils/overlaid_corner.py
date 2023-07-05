from typing import List

from bilby.gw.result import CBCResult
from matplotlib.lines import Line2D

from .constants import LATEX_LABELS


def plot_overlaid_corner(
    r1: CBCResult,
    r2: CBCResult,
    parameters: List[str],
    labels: List[str],
    colors: List[str],
    **kwargs,
):
    # ensure parameters are in both results posteriors
    _check_list_is_subset(parameters, list(r1.posterior.columns))
    _check_list_is_subset(parameters, list(r2.posterior.columns))

    # plot corner
    latex = [LATEX_LABELS[p] for p in parameters]
    kwgs = dict(parameters=parameters, labels=latex, save=False, **kwargs)
    fig = r1.plot_corner(color=colors[0], titles=True, **kwgs)
    fig = r2.plot_corner(fig=fig, color=colors[1], quantiles=[], titles=False, **kwgs)

    # add legend to figure to right using the following colors
    legend_elements = [
        Line2D([0], [0], color=c, lw=4, label=l) for c, l in zip(colors, labels)
    ]
    fig.legend(
        handles=legend_elements,
        loc="upper right",
        bbox_to_anchor=(0.95, 0.95),
        bbox_transform=fig.transFigure,
        frameon=False,
        fontsize=16,
    )

    return fig


def _check_list_is_subset(l1, l2):
    s1 = set(l1)
    s2 = set(l2)
    if not s1.issubset(s2):
        raise ValueError(f"Missing parameters: {s1.difference(s2)}")
