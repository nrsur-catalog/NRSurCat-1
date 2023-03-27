import os.path
import unittest
import shutil

from generate_mock_data import get_mock_cache_dir, cleanup_mock_data
from nrsur_catalog.cache import CatalogCache
from nrsur_catalog import Catalog

CLEANUP = False


class TestCatalog(unittest.TestCase):
    def setUp(self) -> None:
        self.num_events = 2
        self.outdir = "tmp_test"
        os.makedirs(self.outdir, exist_ok=True)
        self.CACHE = CatalogCache(get_mock_cache_dir(num_events=self.num_events))


    def tearDown(self) -> None:
        cleanup_mock_data()
        if CLEANUP:
            shutil.rmtree(self.outdir)

    def test_catalog_plot(self):
        """Test that the Catalog class can be instantiated"""
        df = Catalog.load_events(self.CACHE.dir)
        catalog = Catalog(df)
        catalog.save(self.CACHE.dir + "/downsampled_catalog.hdf5")
        catalog = Catalog.load(clean=False)
        fig = catalog.violin_plot("mass_1")
        fig.savefig(os.path.join(self.outdir, "violin_plot.png"))
        catalog.interactive_violin_plot("mass_1")
        catalog.interactive_violin_2("mass_1")

def test_new():
    # Catalog.load("/home/avaj040/Documents/projects/data/nrsur_results/", clean=True)
    c = Catalog.load("/home/avaj040/Documents/projects/data/nrsur_results/", clean=False)
    c.violin_plot("mass_1")


if __name__ == "__main__":
    unittest.main()
