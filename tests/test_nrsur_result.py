import os.path
import unittest
import shutil

from nrsur_catalog import NRsurResult
from generate_mock_data import get_mock_cache_dir, cleanup_mock_data
from nrsur_catalog.cache import CACHE

# from nrsur_catalog.api.zenodo_interface import upload_to_zenodo
from nrsur_catalog.api.zenodo_interface import check_if_event_in_zenodo


class TestGWResult(unittest.TestCase):
    def setUp(self) -> None:
        self.num_events = 1
        CACHE.cache_dir = get_mock_cache_dir(num_events=self.num_events)
        self.tmp = "tmp_test"
        os.makedirs(self.tmp, exist_ok=True)

    def tearDown(self) -> None:
        cleanup_mock_data()
        shutil.rmtree(self.tmp)

    def test_from_cache(self):
        """Test that the GWResult class can be instantiated"""
        event = CACHE.event_names[0]
        self.nrsur_result = NRsurResult.load(event)
        self.nrsur_result.plot_corner(parameters=["mass_1", "mass_2"])
        self.nrsur_result.plot_signal()

    # def test_from_web(self):
    #     event = CACHE.event_names[0]
    #     if not check_if_event_in_zenodo(event):
    #         upload_to_zenodo(path_regex=f"{CACHE.cache_dir}/*.json", test=True)
    #     # set new cache dir to test that the event is downloaded when not in local cache
    #     CACHE.cache_dir = self.tmp
    #     self.assertTrue(len(CACHE.event_names)==0)
    #     self.nrsur_result = NRsurResult.load(event, cache_dir=CACHE.cache_dir)
    #     self.assertEqual(CACHE.event_names[0], event)
