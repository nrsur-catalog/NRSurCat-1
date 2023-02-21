import os.path
import unittest

from nrsur_catalog import NRsurResult
from generate_mock_data import get_mock_cache_dir, cleanup_mock_data


class TestGWResult(unittest.TestCase):
    def setUp(self) -> None:
        self.cache_dir = get_mock_cache_dir()
        self.nrsur_result = NRsurResult.load("GW150914", cache_dir=self.cache_dir)

    def tearDown(self) -> None:
        cleanup_mock_data()

    def test_gw_plot(self):
        """Test that the GWResult class can be instantiated"""
        self.nrsur_result.plot_corner(parameters=["mass_1", "mass_2"])
        self.nrsur_result.plot_signal()
