"""Module to build the website for the catalog
Most of the code has been grabbed from dfm/tess-atlas
"""

import argparse
import shutil
from itertools import repeat

import jupytext
import os

from tqdm.contrib.concurrent import process_map
from tqdm.auto import tqdm
from multiprocessing import cpu_count

import nbformat
from nbconvert.preprocessors import CellExecutionError, ExecutePreprocessor

from ..cache import CACHE
from ..logger import logger

HERE = os.path.dirname(__file__)
WEB_TEMPLATE = os.path.join(HERE, "template")
GW_PAGE_TEMPLATE = os.path.join(HERE, "gw_notebook_template.py")
TABLE_PAGE_TEMPLATE = "fits/NRSur_Fits.md"


def build_website(fit_dir: str, outdir: str, clean: bool = False) -> None:
    """Build the website for the catalog"""
    CACHE.cache_dir = fit_dir
    event_names = CACHE.event_names
    num_events = len(event_names)

    logger.info(f"Building website with {num_events} fits: {event_names}")
    shutil.copytree(WEB_TEMPLATE, outdir, dirs_exist_ok=True)
    write_fits_table_page(os.path.join(outdir, TABLE_PAGE_TEMPLATE))

    num_threads = cpu_count() // 2
    if num_events < num_threads:
        num_threads = num_events

    logger.info(f"Executing GW fit notebooks with {num_threads} threads")
    fit_dir = os.path.join(outdir, "fits")
    try:
        process_map(
            write_and_execute_gw_notebook,
            event_names,
            repeat(fit_dir),
            desc="Executing Notebooks",
            max_workers=num_threads,
            total=len(CACHE.event_names),
        )
    except Exception as e:
        logger.warning(f"Not executing in parallel: {e}")
        for name in tqdm(event_names, desc="Executing notebooks"):
            write_and_execute_gw_notebook(name, fit_dir)

    command = f"jupyter-book build {outdir}"
    os.system(command)


def write_fits_table_page(path: str) -> None:
    with open(path, "r") as f:
        template_txt = f.read()

    table = "|NRSurrogate Fits| |\n"
    table += "|:---------------:|:---------------:|\n"
    for event_name in CACHE.event_names:
        ipynb = f"[{event_name}]({event_name}.ipynb)"
        image = f"![{event_name}]({event_name}_waveform.png)"
        table += f"|{ipynb}|{image}|\n"

    with open(path, "w") as f:
        f.write(template_txt.replace("{{TABLE}}", table))


def convert_py_to_ipynb(py_fn) -> str:
    ipynb_fn = py_fn.replace(".py", ".ipynb")
    template_py_pointer = jupytext.read(py_fn, fmt="py:light")
    jupytext.write(template_py_pointer, ipynb_fn)

    # ensure notebook is valid
    notebook = nbformat.read(ipynb_fn, as_version=4)
    nbformat.validate(notebook)
    os.remove(py_fn)
    return ipynb_fn


def write_and_execute_gw_notebook(event_name: str, outdir: str):
    with open(GW_PAGE_TEMPLATE, "r") as f:
        template_txt = f.read()
    py_fn = f"{outdir}/{event_name}.py"
    with open(py_fn, "w") as f:
        f.write(template_txt.replace("{{GW EVENT NAME}}", event_name))
    ipynb_fn = convert_py_to_ipynb(py_fn)
    execute_ipynb(ipynb_fn)


def execute_ipynb(notebook_filename: str):
    """
    :param notebook_filename: path of notebook to process
    :return: bool if notebook-preprocessing successful/unsuccessful
    """
    success = True
    with open(notebook_filename) as f:
        notebook = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=-1)
    logger.debug(f"Executing {notebook_filename}")
    try:
        # Note that path specifies in which folder to execute the notebook.
        run_path = os.path.dirname(notebook_filename)
        ep.preprocess(notebook, {"metadata": {"path": run_path}})
    except CellExecutionError as e:
        logger.error(
            f"Preprocessing {notebook_filename} failed:\n\n {e.traceback}"
        )
        success = False
    finally:
        with open(notebook_filename, mode="wt") as f:
            nbformat.write(notebook, f)
    return success


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fit-dir",
        type=str,
        default=".",
        help="Directory to load the fits from",
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
    build_website(args.fit_dir, args.outdir, args.clean)
