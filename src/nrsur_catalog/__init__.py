import logging
import os

import matplotlib.pyplot as plt

from .catalog import Catalog
from .nrsur_result import NRsurResult

__version__ = "0.0.1"
__website__ = "https://cjhaster.github.io/NRSurrogateCatalog/"

HERE = os.path.dirname(__file__)

logging.getLogger("bilby").setLevel(logging.ERROR)

plt.style.use(f"{HERE}/style.mplstyle")
