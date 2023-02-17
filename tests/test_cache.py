import unittest
from nrsur_catalog.cache import CACHE
from testing_datapaths import get_test_cache_dir


class TestCacheCase(unittest.TestCase):
    def test_cache_list_ordered(self):
        CACHE.cache_dir = get_test_cache_dir()
        self.assertEqual("GW150914", CACHE.event_names[0])

if __name__ == '__main__':
    unittest.main()
