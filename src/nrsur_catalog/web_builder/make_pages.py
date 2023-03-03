"""Module to build individual pages for the website"""

from papermill import execute_notebook
import jupytext
import os
import nbformat
import shutil

from ..cache import CACHE

HERE = os.path.dirname(__file__)
GW_PAGE_TEMPLATE = os.path.join(HERE, "page_templates/gw_notebook_template.py")
CATALOG_TEMPLATE = os.path.join(HERE, "page_templates/catalog_plots.py")
TABLE_PAGE_TEMPLATE = "events/nrsur_events_menu.md"


def make_events_menu_page(outdir: str) -> None:
    """Writes the events menu page"""
    fname = f"{outdir}/{TABLE_PAGE_TEMPLATE}"
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    top_text = (
        "# NRSur Events\nTable of all the events analyses in the NRSur Catalog.\n"
    )
    table = "|NRSurrogate Fits| |\n"
    table += "|:---------------:|:---------------:|\n"
    for event_name in CACHE.event_names:
        ipynb = f"[{event_name}]({event_name}.ipynb)"
        image = f"![{event_name}]({event_name}_waveform.png)"
        table += f"|{ipynb}|{image}|\n"

    with open(fname, "w") as f:
        f.write(top_text + table)


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


def make_gw_page(event_name: str, outdir: str):
    """Writes the GW event notebook and executes it"""
    md_fn = f"{outdir}/{event_name}.py"
    with open(GW_PAGE_TEMPLATE, "r") as temp_f:
        txt = temp_f.read()
        txt = txt.replace("{{GW EVENT NAME}}", event_name)
    with open(md_fn, "w") as out_f:
        out_f.write(txt)
    ipynb_fn = convert_py_to_ipynb(md_fn)
    return execute_notebook(ipynb_fn, ipynb_fn, cwd=outdir)


def make_catalog_page(outdir: str):
    """Writes the catalog notebook and executes it"""
    py_fname = f"{outdir}/catalog_plots.py"
    shutil.copyfile(CATALOG_TEMPLATE, py_fname)
    ipynb_fn = convert_py_to_ipynb(py_fname)
    execute_notebook(
        ipynb_fn,
        f"{outdir}/catalog_plots.ipynb",
        cwd=outdir,
    )
