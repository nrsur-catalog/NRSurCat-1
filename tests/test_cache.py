import unittest
from nrsur_catalog.cache import CACHE
from generate_mock_data import get_mock_cache_dir, cleanup_mock_data


class TestCacheCase(unittest.TestCase):
    def test_cache_list_ordered(self):
        CACHE.cache_dir = get_mock_cache_dir()
        self.assertEqual("GW150914", CACHE.event_names[0])
        cleanup_mock_data()


if __name__ == "__main__":
    unittest.main()
