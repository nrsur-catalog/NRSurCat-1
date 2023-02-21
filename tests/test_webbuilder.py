import unittest
from nrsur_catalog.web_builder import build_website
from generate_mock_data import get_mock_cache_dir, cleanup_mock_data

import os
import glob


class TestWebbuilder(unittest.TestCase):
    def test_web(self):
        webout = "out_test_website"
        build_website(
            event_dir=get_mock_cache_dir(),
            outdir=webout,
        )
        self.assertTrue(os.path.exists(webout))
        html_dir = os.path.join(webout, "html")
        self.assertTrue(os.path.exists(f"{html_dir}/index.html"))
        self.assertTrue(os.path.exists(f"{html_dir}/_sources/events/GW150914.ipynb"))
        self.assertTrue(os.path.exists(f"{html_dir}/_images/GW150914_waveform.png"))

    def tearDown(self) -> None:
        cleanup_mock_data()


if __name__ == "__main__":
    unittest.main()
