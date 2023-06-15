import os

import numpy as np
import re
import requests
from tqdm.auto import tqdm
from bilby.core.prior import Prior
from .pesummary_result_to_bilby_result import pesummary_to_bilby_result

from ..logger import logger


INTERESTING_PARAMETERS = {
    "Mass Parameters": ["mass_1", "mass_2", "chirp_mass", "mass_ratio"],
    "Spin Parameters": ["a_1", "a_2", "tilt_1", "tilt_2", "chi_eff", "chi_p"],
    "Localisation Parameters": [
        "ra",
        "dec",
        "geocent_time",
        "luminosity_distance",
    ],
    "Other Parameters": [
        "phase",
        "azimuth",
        "zenith",
        "psi",
        "phi_jl",
        "phi_12",
        "theta_jn",
    ],
}


CATALOG_MAIN_COLOR = "tab:orange"

LATEX_LABELS = dict(
    mass_1=r"$m_1\ [M_{\odot}]$",
    mass_2=r"$m_2\ [M_{\odot}]$",
    chirp_mass=r"$\mathcal{M}\ [M_{\odot}]$",
    mass_ratio=r"$q$",
    a_1=r"$a_1$",
    a_2=r"$a_2$",
    tilt_1=r"$\theta_1$",
    tilt_2=r"$\theta_2$",
    chi_eff=r"$\chi_{\mathrm{eff}}$",
    chi_p=r"$\chi_{\mathrm{p}}$",
    ra=r"$\alpha$",
    dec=r"$\delta$",
    geocent_time=r"$t_c\ [s]$",
    luminosity_distance=r"$d_L\ [Mpc]$",
    phase=r"$\phi$",
    azimuth=r"$\phi$",
    zenith=r"$\theta$",
    psi=r"$\psi$",
    phi_jl=r"$\phi_{\mathrm{JL}}$",
    phi_12=r"$\phi_{12}$",
    theta_jn=r"$\theta_{\mathrm{JN}}$",
)


def get_size_of_file(filename: str) -> str:
    """Get the size of a file in human-readable format"""
    size = os.path.getsize(filename)
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0


def get_1d_summary_str(x: np.ndarray):
    q_lo, q_mid, q_hi = np.quantile(x, [0.16, 0.5, 0.84])
    q_m, q_p = q_mid - q_lo, q_hi - q_mid
    fmt = "{{0:{0}}}".format(".2f").format
    summary = r"${{{0}}}_{{-{1}}}^{{+{2}}}$"
    return summary.format(fmt(q_mid), fmt(q_m), fmt(q_p))


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


def prior_to_str(prior:Prior):
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