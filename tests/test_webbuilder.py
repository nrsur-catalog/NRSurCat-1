import unittest
from nrsur_catalog.web_builder import build_website
from nrsur_catalog.web_builder.make_pages import make_gw_page, make_events_menu_page
from nrsur_catalog.web_builder.utils import get_catalog_summary
import nrsur_catalog

nrsur_catalog.catalog.DEFAULT_CLEAN_CATALOG = False
from nrsur_catalog.cache import CatalogCache

import os
import glob
from unittest.mock import patch, PropertyMock

DIR = os.path.dirname(os.path.abspath(__file__))

CLEAN = True

def test_web(mock_cache_dir):
    cache = CatalogCache(mock_cache_dir)
    # generate
    outdir = "out_test_website"
    with patch("nrsur_catalog.cache.CatalogCache.is_incomplete", new_callable=PropertyMock) as mock_cache:
        mock_cache.return_value = False
        build_website(
            event_dir=mock_cache_dir,
            outdir=outdir,
            clean=CLEAN,
        )
    assert os.path.exists(outdir)
    html_dir = os.path.join(outdir, "_build/html")
    assert os.path.exists(f"{html_dir}/index.html")
    event_nbs = glob.glob(f"{html_dir}/_sources/events/GW*.ipynb")
    images = glob.glob(f"{html_dir}/_images/*waveform.png")
    assert len(event_nbs) == cache.num_events
    assert len(images) == cache.num_events
    print(f"ACCESS WEB HERE:\n{html_dir}/index.html")


def test_gw_page(mock_cache_dir, tmpdir):
    cache = CatalogCache(mock_cache_dir)
    name = cache.event_names[0]
    event_ipynb_dir = tmpdir
    make_gw_page(name, event_ipynb_dir, cache=cache)
    fpath = f"{event_ipynb_dir}/{name}.ipynb"
    assert os.path.exists(fpath)
    print(f"ACCESS GWPAGE HERE:\n {fpath}")


def test_menu_page(mock_cache_dir, tmpdir):
    cache = CatalogCache(mock_cache_dir)

    summary = get_catalog_summary(events_dir=tmpdir, cache_dir=cache.dir)
    assert len(summary) > 0

    event_ipynb_dir = tmpdir
    make_events_menu_page(outdir=event_ipynb_dir, cache=cache)
    assert os.path.exists(f"{event_ipynb_dir}/events/gw_menu_page.ipynb")


if __name__ == "__main__":
    unittest.main()
