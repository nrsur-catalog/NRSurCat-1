import unittest
from nrsur_catalog.api.download_event import download_event
from nrsur_catalog.api.zenodo_interface import upload_files_to_zenodo
from generate_mock_data import get_mock_cache_dir, cleanup_mock_data


class TestZenodoInterface(unittest.TestCase):

    def setUp(self) -> None:
        self.cache_dir = get_mock_cache_dir()

    def test_upload_files_to_zenodo(self):
        upload_files_to_zenodo(f"{self.cache_dir}/*.json")



if __name__ == '__main__':
    unittest.main()
