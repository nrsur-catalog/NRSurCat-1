"""Module to build the website for the catalog
Most of the code has been grabbed from dfm/tess-atlas
"""

import argparse
import glob
import os
import shutil
import sys
from multiprocessing import cpu_count

from tqdm.auto import tqdm
from tqdm.contrib.concurrent import process_map

from nrsur_catalog.cache import DEFAULT_CACHE_DIR, CatalogCache
from nrsur_catalog.logger import logger
from nrsur_catalog.utils import get_event_name
from .make_pages import make_catalog_page, make_events_menu_page, make_gw_page
from .utils import is_file

HERE = os.path.dirname(__file__)
WEB_TEMPLATE = os.path.join(HERE, "website_template")


def build_website(
    event_dir: str, outdir: str, clean: bool = False, parallel_build=False
) -> None:
    """Build the website for the catalog"""
    logger.info(
        f"Building website [args: event_dir:{event_dir}, outdir:{outdir}, clean:{clean}]"
    )

    if clean:
        shutil.rmtree(outdir, ignore_errors=True)

    CACHE = CatalogCache(os.path.abspath(event_dir))

    # make symlink to the web cache directory
    web_cache = os.path.join(outdir, f"events/{DEFAULT_CACHE_DIR}/")

    # make each file in the cache directory a symlink to the web cache directory
    for file in os.listdir(CACHE.dir):
        src = os.path.join(CACHE.dir, file)
        dst = os.path.join(web_cache, file)
        dst_dir = os.path.dirname(dst)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir, exist_ok=True)
        if not is_file(dst):
            assert os.path.exists(src), f"File {src} (src) does not exist"
            os.symlink(src, dst)

    event_names = CACHE.event_names
    num_events = len(event_names)
    if num_events == 0:
        raise ValueError(f"No events found in the cache directory: {event_dir}")

    logger.info(f"Building website with {num_events} events: {event_names}")
    shutil.copytree(WEB_TEMPLATE, outdir, dirs_exist_ok=True)
    event_ipynb_dir = os.path.join(outdir, "events")
    regex = os.path.join(os.path.abspath(event_ipynb_dir), "GW*.ipynb")

    logger.debug(f"Checking {regex} for processed notebooks")
    events_processed = [get_event_name(f.split("/")[-1]) for f in glob.glob(regex)]
    events_not_processed = list(set(event_names) - set(events_processed))

    logger.debug(
        f"Events to make webpages for: {len(events_not_processed)}/{num_events}"
    )

    build_commands = [
        f"build_gwpage {name} {event_ipynb_dir} {CACHE.dir}"
        for name in events_not_processed
    ]
    if parallel_build:
        num_threads = cpu_count() // 2
        if num_events < num_threads:
            num_threads = num_events
        logger.info(f"Executing GW event notebooks with {num_threads} threads")
        process_map(
            os.system,
            build_commands,
            desc="Executing GW Notebooks",
            max_workers=num_threads,
            total=len(events_not_processed),
        )
    else:
        for cmd in tqdm(build_commands, desc="Executing GW notebooks"):
            os.system(cmd)

    logger.info("Executing events menu notebook")
    make_events_menu_page(outdir, CACHE)

    logger.info("Executing catalog notebook")
    make_catalog_page(outdir, CACHE)

    command = f"jupyter-book build {outdir}"
    os.system(command)


def gwpage_main():
    """Runs one GW notebook"""
    args = sys.argv[1:]
    name = args[0]
    event_ipynb_dir = args[1]
    data_dir = args[2]
    CACHE = CatalogCache(data_dir)
    logger.debug(
        f"Running GW notebook for {name} in {event_ipynb_dir} with data in {data_dir}"
    )
    make_gw_page(name, event_ipynb_dir, cache=CACHE)


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
