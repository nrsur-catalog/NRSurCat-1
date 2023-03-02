"""Module to build the website for the catalog
Most of the code has been grabbed from dfm/tess-atlas
"""

import argparse
import shutil
from itertools import repeat

from papermill import execute_notebook

import jupytext
import os

from tqdm.contrib.concurrent import process_map
from tqdm.auto import tqdm
from multiprocessing import cpu_count

import nbformat
from nbconvert.preprocessors import CellExecutionError, ExecutePreprocessor

from ..cache import CACHE
from ..logger import logger
from ..api.zenodo_interface import cache_zenodo_urls_file

from .make_pages import make_events_menu_page, make_catalog_page, make_gw_page

HERE = os.path.dirname(__file__)
WEB_TEMPLATE = os.path.join(HERE, "website_template")


def build_website(event_dir: str, outdir: str, clean: bool = True, parallel_build=True) -> None:
    """Build the website for the catalog"""
    CACHE.cache_dir = os.path.abspath(event_dir)
    CACHE.check_if_events_cached_in_zenodo()
    cache_zenodo_urls_file()
    event_names = CACHE.event_names
    num_events = len(event_names)
    if num_events == 0:
        raise ValueError(f"No events found in the cache directory: {event_dir}")

    if clean:
        shutil.rmtree(outdir, ignore_errors=True)

    logger.info(f"Building website with {num_events} events: {event_names}")
    shutil.copytree(WEB_TEMPLATE, outdir, dirs_exist_ok=True)
    make_events_menu_page(outdir)

    event_ipynb_dir = os.path.join(outdir, "events")

    if parallel_build:
        num_threads = cpu_count() // 2
        if num_events < num_threads:
            num_threads = num_events
        logger.info(f"Executing GW event notebooks with {num_threads} threads")
        process_map(
            make_gw_page,
            event_names,
            repeat(event_ipynb_dir),
            desc="Executing GW Notebooks",
            max_workers=num_threads,
            total=len(CACHE.event_names),
        )
    else:
        for name in tqdm(event_names, desc="Executing GW notebooks"):
            make_gw_page(name, event_ipynb_dir)

    logger.info("Executing catalog notebook")
    make_catalog_page(outdir)

    command = f"jupyter-book build {outdir}"
    os.system(command)


def main():
    """Executes and builds the website [build_nrsur_website]"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--event-dir",
        type=str,
        default=".",
        help="Directory to load the events from",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default=".",
        help="Directory to write the website to",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean the output directory",
    )
    args = parser.parse_args()
    build_website(args.event_dir, args.outdir, args.clean)
