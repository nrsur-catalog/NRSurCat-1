import os
import re

import numpy as np
import requests
from bilby.core.prior import Prior
from tqdm.auto import tqdm

from ..logger import logger
from .constants import (
    CATALOG_MAIN_COLOR,
    INTERESTING_PARAMETERS,
    LATEX_LABELS,
    LOG_PARAMS,
)
from .overlaid_corner import plot_overlaid_corner
from .pesummary_result_to_bilby_result import pesummary_to_bilby_result


def get_size_of_file(filename: str) -> str:
    """Get the size of a file in human-readable format"""
    size = os.path.getsize(filename)
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0


def format_qts_to_latex(q_lo: float, q_mid: float, q_hi: float) -> str:
    """Format quantiles to a LaTeX string"""
    q_m, q_p = q_mid - q_lo, q_hi - q_mid
    fmt = "{{0:{0}}}".format(".2f").format
    summary = r"${{{0}}}_{{-{1}}}^{{+{2}}}$"
    return summary.format(fmt(q_mid), fmt(q_m), fmt(q_p))


def get_1d_summary_str(x: np.ndarray, quantiles=[0.16, 0.5, 0.84]) -> str:
    q_lo, q_mid, q_hi = np.quantile(x, quantiles)
    return format_qts_to_latex(q_lo, q_mid, q_hi)


def get_event_name(s: str):
    """Get the event name from a string using a regex
    e.g.
    'GW170817' from 'GW170817_4.5_0.1.hdf5'
    'GW150914' from "https://sandbox.zenodo.org/record/1164558/files/GW150914_result.json"
    'GW200224_222234'  from  "GW200224_222234_NRSur7dq4_merged_result.json"
    """
    try:
        return re.findall(r"(GW\d{6}\_\d{6}|GW\d{6})", s)[0]
    except IndexError:
        logger.debug(f"Could not parse event name from {s}")
        return None


def get_dir_tree(path):
    """Get a directory tree (in a string)"""
    tree = ""
    for root, dirs, files in os.walk(path):
        level = root.replace(path, "").count(os.sep)
        indent = " " * 4 * (level)
        tree += f"{indent}{os.path.basename(root)}/\n"
        subindent = " " * 4 * (level + 1)
        for f in files:
            tree += f"{subindent}{f}\n"
    return tree


def download(url: str, fname: str) -> None:
    """Download a file from a URL and save it to a file"""
    resp = requests.get(url, timeout=5)
    if resp.status_code != 200:
        raise ValueError(f"Failed to download {url}: {resp.json()}")
    total = int(resp.headers.get("content-length", 0))
    with open(fname, "wb") as file, tqdm(
        desc=f"Downloading file",
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


def prior_to_str(prior: Prior):
    """Convert a prior to a string"""
    # get class name
    name = prior.__class__.__name__
    min_val, max_val = None, None
    if hasattr(prior, "minimum"):
        min_val = round(prior.minimum, 2)
    if hasattr(prior, "maximum"):
        max_val = round(prior.maximum, 2)
    repr = r"$\text{" + name + "}"
    if min_val is not None and max_val is not None:
        repr += f" [{min_val}, {max_val}]"
    return repr + "$"


def safe_plot(func):
    """Decorator to catch errors when plotting"""

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Failed to plot {func.__name__}: {e}")

    return wrapper
