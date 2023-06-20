import unittest
from nrsur_catalog.web_builder import build_website
from nrsur_catalog.web_builder.make_pages import make_gw_page, make_events_menu_page
from nrsur_catalog.web_builder.utils import get_catalog_summary
from nrsur_catalog.cache import CatalogCache

import os
import glob


DIR = os.path.dirname(os.path.abspath(__file__))

def test_web(mock_cache_dir):
    cache = CatalogCache(mock_cache_dir)
    # generate
    outdir = "out_test_website"
    build_website(
        event_dir=mock_cache_dir,
        outdir=outdir,
        clean=True,
    )
    assert os.path.exists(outdir)
    html_dir = os.path.join(outdir, "_build/html")
    assert os.path.exists(f"{html_dir}/index.html")
    event_nbs = glob.glob(f"{html_dir}/_sources/events/GW*.ipynb")
    images = glob.glob(f"{html_dir}/_images/*waveform.png")
    assert len(event_nbs) == cache.num_events
    assert len(images) == cache.num_events


def test_gw_page(mock_cache_dir,tmpdir):
    cache = CatalogCache(mock_cache_dir)
    name = cache.event_names[0]
    event_ipynb_dir = tmpdir
    make_gw_page(name, event_ipynb_dir, cache=cache)
    assert os.path.exists(f"{event_ipynb_dir}/{name}.ipynb")


# def test_menu_page(mock_cache_dir,tmpdir):
#     cache = CatalogCache(mock_cache_dir)
#
#     summary = get_catalog_summary(cache.dir)
#
#     event_ipynb_dir = tmpdir
#     make_events_menu_page(outdir=event_ipynb_dir, cache=cache)
#     assert os.path.exists(f"{event_ipynb_dir}/events/gw_menu_page.ipynb")

if __name__ == "__main__":
    unittest.main()
