import os.path
import pytest

from nrsur_catalog import NRsurResult
from nrsur_catalog.cache import CatalogCache


def test_load_result_from_cache(mock_cache_dir, mock_download):
    """Test that the GWResult class can be instantiated"""
    CACHE = CatalogCache(mock_cache_dir)
    event = CACHE.event_names[0]
    nrsur_result = NRsurResult.load(event, cache_dir=mock_cache_dir)
    nrsur_result.plot_corner(parameters=["mass_1", "mass_2"])
    nrsur_result.plot_lvk_comparison_corner(["luminosity_distance", "ra", "dec"])
    nrsur_result.plot_signal()

    # test that ValueError is raised if event is not in cache
    with pytest.raises(ValueError):
        event_name = "GW100000"
        nrsur_result.load(event_name)

    fpath = CACHE.find(CACHE.event_names[0])
    assert os.path.isfile(fpath)
