"""Module containing API to let users download NRSur Catlog events from Zenodo

NOTE:
    GWTC3: https://zenodo.org/record/5546663
    GWTC2.1: https://zenodo.org/record/6513631

"""
import argparse
import os.path
import sys
from typing import Optional, Tuple

from .. import utils
from ..cache import DEFAULT_CACHE_DIR, CatalogCache
from ..logger import logger
from .zenodo_interface import check_if_event_in_zenodo, get_zenodo_urls


def get_cli_args(args=None) -> Tuple[str, bool, str]:
    """Get the NRSur Catlog event name from the CLI and return it"""

    if args is None:
        args = sys.argv[1:]  # Get all args except the script name

    parser = argparse.ArgumentParser(prog="download_event")
    parser.add_argument(
        "event_name",
        type=str,
        default="",
        help="The name of the event to be downloaded (e.g. GW190521)",
    )
    parser.add_argument(
        "--cache-dir",
        type=str,
        default=DEFAULT_CACHE_DIR,
        help="The dir to cache the NRSur Catlog events",
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


def download_event(
    event_name: str,
    cache_dir: Optional[str] = DEFAULT_CACHE_DIR,
    download_lvk: bool = False,
) -> None:
    """Download the NRSur Catlog events from Zenodo given the event name"""

    CACHE = CatalogCache(cache_dir)

    present, event_name = check_if_event_in_zenodo(
        event_name, lvk_posteriors=download_lvk
    )

    if not present:
        logger.debug("Event not found in Zenodo")
        return

    if event_name in CACHE.find(
        event_name, lvk_posteriors=download_lvk
    ):  # Check if the event is already cached
        logger.debug(f"Fit {event_name} already downloaded")
        return

    url_dict = get_zenodo_urls(lvk_posteriors=download_lvk)
    if event_name not in url_dict:
        raise ValueError(
            f"{event_name} has not been analysed yet -- please choose from {list(url_dict.keys())}"
        )

    url = url_dict[event_name]
    fname = url.split("/")[-1]
    savepath = os.path.abspath(os.path.join(cache_dir, fname))
    catalog_name = "LVK" if download_lvk else "NRSur"
    logger.info(
        f"Downloading {event_name} from the {catalog_name} Catalog -> {savepath}..."
    )
    utils.download(url_dict[event_name], savepath)
    logger.info("Download completed!")


def download_missing_events(cache_dir: str) -> None:
    """Download all NRSur Catlog events from Zenodo that are not already present"""
    cache = CatalogCache(cache_dir)
    events_to_download = cache.missing_events
    logger.info(f"Downloading all {len(events_to_download)} events...")
    for event_name in events_to_download:
        download_event(event_name, cache_dir=cache_dir)
