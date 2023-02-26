from nrsur_catalog.web_builder import build_website
from generate_mock_data import get_mock_cache_dir
from nrsur_catalog.api.zenodo_interface import upload_to_zenodo
import os

test_dir = os.path.abspath("test_events_dir")
# get_mock_cache_dir(test_dir=test_dir, num_events=10, pts=1000, symlinks=False)
# upload_to_zenodo(path_regex=f"{test_dir}/*.json", test=True)
build_website(event_dir=test_dir, outdir="test_website")
os.system("ghp-import -npf test_website/_build/html")
