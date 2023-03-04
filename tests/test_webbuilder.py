import unittest
from nrsur_catalog.web_builder import build_website
from generate_mock_data import get_mock_cache_dir, cleanup_mock_data

import os
import glob


class TestWebbuilder(unittest.TestCase):
    def setUp(self) -> None:
        self.num_events = 2
        self.cache_dir = get_mock_cache_dir(num_events=self.num_events)

    # def tearDown(self) -> None:
    #     cleanup_mock_data()

    def test_web(self):
        webout = "out_test_website"
        build_website(
            event_dir=self.cache_dir,
            outdir=webout,
            clean=True,
        )
        self.assertTrue(os.path.exists(webout))
        html_dir = os.path.join(webout, "_build/html")
        self.assertTrue(os.path.exists(f"{html_dir}/index.html"))
        event_nbs = glob.glob(f"{html_dir}/_sources/events/*.ipynb")
        images = glob.glob(f"{html_dir}/_images/*waveform.png")
        self.assertEqual(len(event_nbs), self.num_events)
        self.assertEqual(len(images), self.num_events)


if __name__ == "__main__":
    unittest.main()
