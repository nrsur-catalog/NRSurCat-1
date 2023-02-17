import logging

__version__ = "0.0.1"

from .nrsur_result import NRsurResult

logging.getLogger("bilby").setLevel(logging.ERROR)
