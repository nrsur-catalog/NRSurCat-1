import unittest
from nrsur_catalog.api import zenodo_interface
from generate_mock_data import get_mock_cache_dir, cleanup_mock_data


class TestZenodoInterface(unittest.TestCase):

    def test_update_cache(self):
        zenodo_interface.cache_zenodo_urls_file(sandbox=True)

    def test_names_of_events(self):
        events = zenodo_interface.get_zenodo_urls()
        event0 = events.keys()[0]
        self.assertTrue(zenodo_interface.check_if_event_in_zenodo(event0))


if __name__ == '__main__':
    unittest.main()
