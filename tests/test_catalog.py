import os.path
import unittest
import shutil

from generate_mock_data import get_mock_cache_dir, cleanup_mock_data
from nrsur_catalog.cache import CACHE
from nrsur_catalog import Catalog

CLEANUP = False


class TestCatalog(unittest.TestCase):
    def setUp(self) -> None:
        self.num_events = 2
        self.outdir = "tmp_test"
        os.makedirs(self.outdir, exist_ok=True)
        CACHE.cache_dir = get_mock_cache_dir(num_events=self.num_events)

    def tearDown(self) -> None:
        cleanup_mock_data()
        if CLEANUP:
            shutil.rmtree(self.outdir)

    def test_catalog_plot(self):
        """Test that the Catalog class can be instantiated"""
        catalog = Catalog.load()
        fig = catalog.violin_plot("mass_1")
        fig.savefig(os.path.join(self.outdir, "violin_plot.png"))
        catalog.interactive_violin_plot("mass_1")
        catalog.interactive_violin_2("mass_1")


if __name__ == "__main__":
    unittest.main()
