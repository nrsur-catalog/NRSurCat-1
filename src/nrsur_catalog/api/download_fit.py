"""Module containing API to let users download NRSur Catlog fits from Zenodo"""
import argparse
import os.path
import sys
import requests
from tqdm.auto import tqdm
from typing import Optional

from ..cache import CACHE, DEFAULT_CACHE_DIR
from ..logger import logger
from .zenodo_interface import get_zenodo_urls


def get_cli_args(args=None) -> argparse.Namespace:
    """Get the NRSur Catlog fit name from the CLI and return it"""

    if args is None:
        args = sys.argv[1:]  # Get all args except the script name

    parser = argparse.ArgumentParser(prog="download_fit")
    parser.add_argument(
        "event_name",
        type=str,
        default="",
        help="The name of the NRSur Catlog fit to be downloaded (e.g. GW190521)",
    )
    parser.add_argument(
        "--cache-dir",
        type=str,
        default=DEFAULT_CACHE_DIR,
        help="The dir to cache the NRSur Catlog fits",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        default=False,
    )
    args = parser.parse_args(args=args)

    if args.all is False and args.event_name == "":
        raise ValueError("Either --all or --event-name must be specified")

    return args.event_name, args.all, args.cache_dir


def download_fit(fit_name: str, cache_dir: Optional[str] = DEFAULT_CACHE_DIR) -> None:
    """Download the NRSur Catlog fits from Zenodo given the fit name"""

    CACHE.cache_dir = cache_dir
    if fit_name in CACHE.list:  # Check if the fit is already cached
        logger.debug(f"Fit {fit_name} already downloaded")
        return

    analysed_fits = get_zenodo_urls()
    if fit_name not in analysed_fits:
        raise ValueError(
            f"{fit_name} has not been analysed yet -- please choose from {list(analysed_fits.keys())}"
        )

    url = analysed_fits[fit_name]
    fname = url.split("/")[-1]
    savepath = os.path.join(cache_dir, fname)
    logger.info(f"Downloading {fit_name} from the NRSur Catalog -> {savepath}...")
    download(analysed_fits[fit_name], savepath)
    logger.info("Completed! Enjoy your fit!")


def download_all_fits() -> None:
    """Download all NRSur Catlog fits from Zenodo"""
    analysed_fits = get_zenodo_urls()
    logger.info(f"Downloading all {len(analysed_fits)} fits...")
    for fit_name in analysed_fits:
        download_fit(fit_name)


def download(url: str, fname: str) -> None:
    """Download a file from a URL and save it to a file"""
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
            desc=f"Downloading file",
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


def main():
    """Download the NRSur Catlog fits from Zenodo given the fit name"""
    fit_name, download_all, cache_dir = get_cli_args()
    if download_all:
        download_all_fits()
    else:
        download_fit(fit_name, cache_dir)
