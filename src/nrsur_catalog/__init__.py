import logging
import os

import matplotlib.pyplot as plt

from .catalog import Catalog
from .nrsur_result import NRsurResult

__version__ = "0.0.1"
__website__ = "https://sxs-collaboration.github.io/"
__uri__ = "https://github.com/sxs-collaboration/nrsur_catalog"
__author__ = "NRSurrogate Catalog Team"
__email__ = "tousifislam24@gmail.com"
__license__ = "MIT"
__description__ = "GW event posteriors obtained using numerical relativity surrogate models"
__copyright__ = "Copyright 2023 NRSurrogate Catalog Team"
__contributors__ = "https://github.com/sxs-collaboration/nrsur_catalog/graphs/contributors"



HERE = os.path.dirname(__file__)

logging.getLogger("bilby").setLevel(logging.ERROR)

plt.style.use(f"{HERE}/style.mplstyle")
