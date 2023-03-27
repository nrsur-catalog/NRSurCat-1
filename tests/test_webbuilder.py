import unittest
from nrsur_catalog.web_builder import build_website
from nrsur_catalog.web_builder.make_pages import make_gw_page
from generate_mock_data import get_mock_cache_dir, cleanup_mock_data

import os
import glob


class TestWebbuilder(unittest.TestCase):
    def setUp(self) -> None:
        self.num_events = 2
        self.cache_dir = get_mock_cache_dir(num_events=self.num_events)
        self.outdir =  "out_test_website"
        os.makedirs(self.outdir, exist_ok=True)

    # def tearDown(self) -> None:
    #     cleanup_mock_data()

    def test_web(self):
        build_website(
            event_dir=self.cache_dir,
            outdir=self.outdir,
            clean=True,
        )
        self.assertTrue(os.path.exists(self.outdir))
        html_dir = os.path.join(self.outdir, "_build/html")
        self.assertTrue(os.path.exists(f"{html_dir}/index.html"))
        event_nbs = glob.glob(f"{html_dir}/_sources/events/*.ipynb")
        images = glob.glob(f"{html_dir}/_images/*waveform.png")
        self.assertEqual(len(event_nbs), self.num_events)
        self.assertEqual(len(images), self.num_events)

    def test_make_gwpage(self):
        make_gw_page("GW150914", self.outdir)
        self.assertTrue(os.path.exists(self.outdir + "/GW150914_waveform.png"))


def test_web():
    outdir = "out_test_website"
    build_website(
        event_dir="/home/avaj040/Documents/projects/data/nrsur_results/",
        outdir="out_test_website",
        clean=False,
    )


if __name__ == "__main__":
    unittest.main()
