"""Module to build individual pages for the website"""

from ploomber_engine import execute_notebook
from nbconvert.preprocessors import CellExecutionError, ExecutePreprocessor
import jupytext
import os
import nbformat
import shutil

from ..cache import CatalogCache, DEFAULT_CACHE_DIR
from ..nrsur_result import NRsurResult

HERE = os.path.dirname(__file__)
GW_PAGE_TEMPLATE = os.path.join(HERE, "page_templates/gw_notebook_template.py")
CATALOG_TEMPLATE = os.path.join(HERE, "page_templates/catalog_plots.py")
TABLE_PAGE_TEMPLATE = os.path.join(HERE, "page_templates/gw_menu_page.py")


def make_events_menu_page(outdir: str) -> None:
    """Writes the events menu page"""
    py_fname = f"{outdir}/events/gw_menu_page.py"
    events_dir = os.path.abspath(os.path.join(outdir, "events"))
    _replace_strings_from_file(TABLE_PAGE_TEMPLATE, {"{{IPYNB_DIR}}": events_dir}, py_fname)
    ipynb_fn = convert_py_to_ipynb(py_fname)
    return execute_notebook(ipynb_fn, ipynb_fn, cwd=outdir, progress_bar=False, verbose=False,
                            save_profiling_data=False)


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
    nrsurr_res = NRsurResult.load(event_name, cache_dir=cache.dir)
    summary_md = nrsurr_res.summary(markdown=True)
    _replace_strings_from_file(
        GW_PAGE_TEMPLATE,
        {"{{GW EVENT NAME}}": event_name, "{{SUMMARY_TABLE}}": summary_md},
        md_fn
    )
    ipynb_fn = convert_py_to_ipynb(md_fn)
    return execute_notebook(
        ipynb_fn, ipynb_fn, cwd=outdir, save_profiling_data=True, profile_memory=True,
        progress_bar=False, verbose=False
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
        if not os.path.exists(dst):
            os.symlink(src, dst)

    execute_notebook(
        ipynb_fn,
        f"{outdir}/catalog_plots.ipynb",
        cwd=outdir,
        save_profiling_data=True, profile_memory=True
    )
