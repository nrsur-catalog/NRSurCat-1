import unittest
from nrsur_catalog.cache import CACHE
from generate_mock_data import get_mock_cache_dir, cleanup_mock_data


class TestCacheCase(unittest.TestCase):
    def test_cache_list_ordered(self):
        path = get_mock_cache_dir()
        CACHE.cache_dir = path
        self.assertTrue(len(CACHE.event_names) > 0)
        cleanup_mock_data()
        self.assertTrue(path, CACHE.cache_dir)


if __name__ == "__main__":
    unittest.main()
