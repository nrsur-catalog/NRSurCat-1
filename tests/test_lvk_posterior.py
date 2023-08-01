from nrsur_catalog.lvk_posterior import load_lvk_result
import pandas as pd
from nrsur_catalog import utils
from nrsur_catalog.logger import logger

def test_lvk_posterior_loader(mock_download, tmpdir):
    """Test that the LVK posterior can be loaded"""
    result = load_lvk_result("GW150914_095045", cache_dir=tmpdir)
    assert result is not None
    assert isinstance(result.posterior, pd.DataFrame)
    posterior = load_lvk_result("GW150914_095045", cache_dir=tmpdir) # get from cache
    assert posterior is not None