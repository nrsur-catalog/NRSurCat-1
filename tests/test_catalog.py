import pandas as pd

from nrsur_catalog.cache import CatalogCache
from nrsur_catalog import Catalog
import shutil, os

CLEANUP = False


def test_catalog_plot(mock_cache_dir, tmpdir):
    """Test that the Catalog class can be instantiated"""
    CACHE = CatalogCache(mock_cache_dir)

    # Test that the Catalog class can be instantiated from dir with results
    catalog = Catalog.load(CACHE.dir, clean=True)
    assert isinstance(catalog, Catalog)
    assert isinstance(catalog._df, pd.DataFrame)
    catalog.save(f"{tmpdir}/downsampled_catalog.h5")
    catalog = Catalog(posteriors=catalog._df)
    latex_summary = catalog.get_latex_summary()
    assert isinstance(latex_summary, pd.DataFrame)
    fig = catalog.violin_plot("mass_1")
    violin_fn = os.path.join(tmpdir, "violin_plot.png")
    fig.savefig(violin_fn)
    assert os.path.isfile(violin_fn)

