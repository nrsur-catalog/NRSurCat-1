from nrsur_catalog.web_builder import build_website
from generate_mock_data import get_mock_cache_dir
import os

test_dir = os.path.abspath("test_events_dir")
# get_mock_cache_dir(test_dir=test_dir, num_events=10, pts=1000, symlinks=False)
build_website(event_dir=test_dir, outdir="test_website")
os.system("ghp-import -npf test_website/_build/html")
