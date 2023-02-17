import unittest
from nrsur_catalog.web_builder import build_website
from testing_datapaths import get_test_cache_dir
import os
import glob

class TestWebbuilder(unittest.TestCase):
    def test_web(self):
        webout = "out_test_website"
        build_website(
            fit_dir=get_test_cache_dir(),
            outdir=webout,
        )
        self.assertTrue(os.path.exists(webout))
        self.assertTrue(os.path.exists(os.path.join(webout, "_build/html/index.html")))
        self.assertTrue(os.path.exists(os.path.join(webout, "fits/GW150914.ipynb")))
        self.assertTrue(os.path.exists(os.path.join(webout, "fits/GW150914_waveform.png")))
        self.assertTrue(os.path.exists(os.path.join(webout, "fits/out_nrsur_catalog/GW150914/GW150914_corner.png")))


if __name__ == '__main__':
    unittest.main()
