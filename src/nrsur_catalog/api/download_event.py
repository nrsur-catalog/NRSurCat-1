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
from .zenodo_interface import check_if_event_in_zenodo, get_zenodo_urls, get_analysed_event_names


PROGNAME = "get_nrsur_event"

def create_parser():
    parser = argparse.ArgumentParser(
        prog="PROGNAME",
        description="Download NRSur Catlog analysis results from Zenodo.",
    )
    parser.add_argument(
        "--event-name",
        type=str,
        default="",
        help="The name of the event to be downloaded (e.g. GW150914)",
    )
    parser.add_argument(
        "--cache-dir",
        type=str,
        default=DEFAULT_CACHE_DIR,
        help="The directory to save the NRSur Catlog event result files.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        default=False,
        help="If all catalog results should be downloaded. Cannot be used with --event-name.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        default=False,
        help="If the result files need to be re-downloaded (if they already exist).",
    )
    return parser

def get_cli_args(args=None) -> Tuple[str, bool, str]:
    """Get the NRSur Catlog event name from the CLI and return it"""

    if args is None:
        args = sys.argv[1:]  # Get all args except the script name

    parser = create_parser()
    args = parser.parse_args(args=args)

    if (
            (args.all is False and args.event_name == "") or (args.all is True and args.event_name != "")
    ):
        raise ValueError("Either --all or --event-name must be specified.")

    return args.event_name, args.all, args.cache_dir, args.clean


def download_event(
        event_name: str,
        cache_dir: Optional[str] = DEFAULT_CACHE_DIR,
        download_lvk: bool = False,
        clean: bool = False,
) -> None:
    """Download the NRSur Catlog events from Zenodo given the event name"""

    CACHE = CatalogCache(cache_dir)

    try:
        present, event_name = check_if_event_in_zenodo(
            event_name, lvk_posteriors=download_lvk
        )
    except Exception as e:
        logger.debug(e)
        present = False

    if not present:
        valid_events = "\n".join([f"{i:2d}) {n}" for i, n in enumerate(get_analysed_event_names())])
        logger.error(
            f"Event {event_name} not found on Zenodo. "
            f"Please choose an event from:\n{valid_events}"
        )
        return

    if not clean and event_name in CACHE.find(
            event_name, lvk_posteriors=download_lvk
    ):  # Check if the event is already cached
        logger.warning(f"File for {event_name} already downloaded: {CACHE.find(event_name)}")

        return

    url_dict = get_zenodo_urls(lvk_posteriors=download_lvk)
    if event_name not in url_dict:
        raise ValueError(
            f"{event_name} has not been analysed -- Please choose from {list(url_dict.keys())}"
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


def download_missing_events(cache_dir: str, clean=False) -> None:
    """Download all NRSur Catlog events from Zenodo that are not already present"""
    cache = CatalogCache(cache_dir)
    events_to_download = cache.missing_events
    if clean:
        events_to_download = get_analysed_event_names()
    logger.info(f"Downloading all {len(events_to_download)} events...")
    for event_name in events_to_download:
        download_event(event_name, cache_dir=cache_dir, clean=clean)


def main(args=None):
    """Download the NRSur Catlog events from Zenodo given the event name [get_nrsur_event]"""
    event_name, download_all, cache_dir, clean = get_cli_args(args)
    if download_all:
        download_missing_events(cache_dir, clean)
    else:
        download_event(event_name, cache_dir, clean)
