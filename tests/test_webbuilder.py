import unittest
from nrsur_catalog.web_builder import build_website
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

if __name__ == "__main__":
    unittest.main()
