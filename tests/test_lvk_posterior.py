from nrsur_catalog.lvk_posterior import get_lvk_posterior
import pandas as pd
from nrsur_catalog import utils
from nrsur_catalog.logger import logger

# Todo mock the download_event function

def test_lvk_posterior_loader(mock_download, tmpdir):
    """Test that the LVK posterior can be loaded"""
    posterior = get_lvk_posterior("GW150914_095045", cache_dir=tmpdir)
    assert posterior is not None
    assert isinstance(posterior, pd.DataFrame)
    posterior = get_lvk_posterior("GW150914_095045", cache_dir=tmpdir) # get from cache
    assert posterior is not None