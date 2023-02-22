import unittest
from nrsur_catalog.api.zenodo_interface import ZenodoInterface
from generate_mock_data import get_mock_cache_dir, cleanup_mock_data


class TestZenodoInterface(unittest.TestCase):

    def setUp(self) -> None:
        self.cache_dir = get_mock_cache_dir(num_events=1)

    def tearDown(self) -> None:
        cleanup_mock_data()

    def test_upload_files_to_zenodo(self):
        ZenodoInterface(test=True).upload_files(f"{self.cache_dir}/*.json")

    def test_names_of_events(self):
        events = ZenodoInterface(test=True).get_event_urls()
        self.assertTrue("GW170729" in events.keys())


if __name__ == '__main__':
    unittest.main()
