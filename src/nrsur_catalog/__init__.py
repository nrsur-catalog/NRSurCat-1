import logging
import os

import matplotlib.pyplot as plt

from .nrsur_result import NRsurResult
from .catalog import Catalog

__version__ = "0.0.1"

HERE = os.path.dirname(__file__)

logging.getLogger("bilby").setLevel(logging.ERROR)

plt.style.use(f"{HERE}/style.mplstyle")
