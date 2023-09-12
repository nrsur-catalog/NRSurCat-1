import os

import matplotlib.pyplot
import bilby
import numpy as np
import corner as corner
import imageio
from matplotlib.lines import Line2D
from nrsur_catalog.nrsur_result import NRsurResult
import pandas as pd
import warnings
import logging

logging.getLogger('root').setLevel(logging.ERROR)

from tqdm.auto import tqdm


def make_corner_plot(result, prior_samp, params, frac_posterior, param_ranges=[]):
    total = len(result.posterior)
    np.random.seed(0)

    post = result.posterior
    # mix such that prior is 1-frac of total

    samp = pd.concat(
        [post.sample(frac=frac_posterior, replace=False),
         prior_samp.sample(frac=1 - frac_posterior)
         ])
    samp = samp[params]

    if len(param_ranges) == 0:
        param_ranges = [(result.priors[param].minimum, result.priors[param].maximum) for param in params]
    kwgs = dict(
        plot_datapoints=False, bins=30,
        smooth1d=0.02, show_titles=False, titles=False, range=param_ranges,
        plot_density=True, plot_contours=False, fill_contours=False, smooth=0.7,
    )
    color = 'tab:blue'

    # surpress WARNING:root:Pandas support in corner is deprecated; use ArviZ directly

    with warnings.catch_warnings():
        fig = corner.corner(samp.values, color=color, **kwgs, )

    #
    # # add legend to figure to right using the following colors
    # legend_elements = [
    #     Line2D([0], [0], color=color, lw=4, label=f'')
    # ]
    # fig.legend(
    #     handles=legend_elements,
    #     loc="upper right",
    #     bbox_to_anchor=(0.95, 0.95),
    #     bbox_transform=fig.transFigure,
    #     frameon=False,
    #     fontsize=16,
    # )

    return fig


def make_corner_anim(result, params, n_images, param_ranges=[], outdir='out_gif'):
    # fracs = np.linspace(0, 1, n_images)
    fracs = [0.0, 0.01, 0.013, 0.017, 0.05, 0.09, 0.13, 0.2, 0.5, 0.7, 0.9, 0.95, 0.98, 1.0]
    image_fns = []
    os.makedirs(outdir, exist_ok=True)
    total = len(result.posterior)
    prior_samp = pd.DataFrame(result.priors.sample(total))[params]

    for frac in tqdm(fracs):
        fig = make_corner_plot(result,prior_samp, params, frac, param_ranges)
        fn = os.path.join(outdir, f"corner_{frac}.png")
        fig.savefig(fn)
        image_fns.append(fn)
        matplotlib.pyplot.close(fig)
    __make_gif(image_fns)


def __make_gif(image_fns):
    """Make a gif from a list of images and loop it forever"""
    images = []
    for fn in image_fns:
        images.append(imageio.imread(fn))
    # and now in reverse
    for fn in image_fns[::-1]:
        images.append(imageio.imread(fn))
    imageio.mimsave("animation.gif", images, duration=2, loop=0)


if __name__ == '__main__':
    r = NRsurResult.load(event_name='GW150914_0954045',
                         event_path="/Users/avaj0001/Documents/projects/NR_DATA/GW150914_095045_NRSur7dq4.h5")
    params = ['chirp_mass', 'mass_ratio', 'a_1', 'a_2', 'luminosity_distance']
    r.posterior.geocent_time = r.posterior.geocent_time - r.posterior.geocent_time.min()
    g = r.posterior.geocent_time
    r.posterior = r.posterior.sample(frac=0.1)
    make_corner_anim(r, params, 5, param_ranges=[(20, 40), (0.2, 1), (0, 1), (0, 1), (100, 2000)])
