"""Module to build individual pages for the website"""

import os
import shutil

import jupytext
import nbformat
from ploomber_engine import execute_notebook

from nrsur_catalog.cache import DEFAULT_CACHE_DIR, CatalogCache
from nrsur_catalog.logger import logger
from nrsur_catalog.nrsur_result import NRsurResult
from nrsur_catalog_webbuilder.utils import get_catalog_summary

POSTERIORS = [
    "chirp_mass",
    "mass_ratio",
    "chi_eff",
    "final_mass",
    "final_spin",
    "final_kick",
]

from .utils import is_file, get_animation_cell

HERE = os.path.dirname(__file__)
GW_PAGE_TEMPLATE = os.path.join(HERE, "page_templates/gw_notebook_template.py")
CATALOG_TEMPLATE = os.path.join(HERE, "page_templates/catalog_plots.py")
TABLE_PAGE_TEMPLATE = os.path.join(HERE, "page_templates/gw_menu_page.py")


def make_events_menu_page(outdir: str, cache: CatalogCache) -> None:
    """Writes the events menu page"""
    py_fname = f"{outdir}/events/gw_menu_page.py"
    os.makedirs(os.path.dirname(py_fname), exist_ok=True)
    events_dir = os.path.abspath(os.path.join(outdir, "events"))
    summary_table = get_catalog_summary(events_dir, cache.dir, columns=POSTERIORS)
    _replace_strings_from_file(
        TABLE_PAGE_TEMPLATE,
        {
            "{{EVENTS_DIR}}": events_dir,
            "{{CACHE_DIR}}": cache.dir,
            "{{SUMMARY_TABLE}}": summary_table.to_markdown(index=False)
        },
        py_fname,
    )
    ipynb_fn = convert_py_to_ipynb(py_fname)
    return execute_notebook(
        ipynb_fn,
        ipynb_fn,
        cwd=outdir,
        progress_bar=False,
        verbose=False,
        save_profiling_data=False,
    )




def convert_py_to_ipynb(py_fn) -> str:
    """Converts a python file to a jupyter notebook"""
    ipynb_fn = py_fn.replace(".py", ".ipynb")
    template_py_pointer = jupytext.read(py_fn, fmt="py:light")
    jupytext.write(template_py_pointer, ipynb_fn)

    # ensure notebook is valid
    notebook = nbformat.read(ipynb_fn, as_version=4)
    nbformat.validate(notebook)
    os.remove(py_fn)
    return ipynb_fn


def make_gw_page(event_name: str, outdir: str, cache: CatalogCache):
    """Writes the GW event notebook and executes it"""
    md_fn = f"{outdir}/{event_name}.py"
    logger.debug(f"Making {event_name} page")
    nrsurr_res = NRsurResult.load(event_name, cache_dir=cache.dir)
    summary_md = nrsurr_res.summary(markdown=True)
    animation_md = get_animation_cell(event_name)
    _replace_strings_from_file(
        GW_PAGE_TEMPLATE,
        {
            "{{GW EVENT NAME}}": event_name,
            "{{SUMMARY_TABLE}}": summary_md,
            "{{ANIMATION_CELL}}": animation_md
        },
        md_fn,
    )
    ipynb_fn = convert_py_to_ipynb(md_fn)
    logger.debug(
        f"Executing GW{event_name}:\n"
        f"    - cwd: {outdir}\n"
        f"    - ipynb_fn: {ipynb_fn}\n"
        f"    - cache: {cache.dir}\n"
    )
    return execute_notebook(
        ipynb_fn,
        ipynb_fn,
        cwd=outdir,
        save_profiling_data=True,
        profile_memory=True,
        progress_bar=False,
        verbose=False,
    )


def _replace_strings_from_file(fname: str, replacements: dict, outfname: str) -> None:
    """Replaces strings in a file"""
    with open(fname, "r") as f:
        txt = f.read()
        for key, value in replacements.items():
            txt = txt.replace(key, value)
    with open(outfname, "w") as f:
        f.write(txt)


def make_catalog_page(outdir: str, cache: CatalogCache):
    """Writes the catalog notebook and executes it"""
    py_fname = f"{outdir}/catalog_plots.py"
    shutil.copyfile(CATALOG_TEMPLATE, py_fname)
    ipynb_fn = convert_py_to_ipynb(py_fname)

    tmp_cache = f"{outdir}/{DEFAULT_CACHE_DIR}"
    os.makedirs(tmp_cache, exist_ok=True)
    for fname in os.listdir(cache.dir):
        src = os.path.join(cache.dir, fname)
        dst = os.path.join(tmp_cache, fname)
        if not is_file(dst):
            os.symlink(src, dst)

    execute_notebook(
        ipynb_fn,
        f"{outdir}/catalog_plots.ipynb",
        cwd=outdir,
        save_profiling_data=True,
        profile_memory=True,
    )
