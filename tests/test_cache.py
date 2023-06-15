import pytest
from nrsur_catalog.cache import CatalogCache


def test_cache(mock_cache_dir):
    CACHE = CatalogCache(mock_cache_dir)
    assert (len(CACHE.event_names) > 0)
    assert (mock_cache_dir == CACHE.dir)

    assert isinstance(CACHE.find(CACHE.event_names[0]), str)
    with pytest.raises(FileNotFoundError):
        CACHE.find(name="fake event", hard_fail=True)

