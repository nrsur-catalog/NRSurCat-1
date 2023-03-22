from nrsur_catalog.lvk_posterior import get_lvk_posterior
import pandas as pd

def test_lvk_posterior_loader():
    posterior = get_lvk_posterior("GW150914")
    assert posterior is not None
    assert isinstance(posterior, pd.DataFrame)
    posterior = get_lvk_posterior("GW150914") # get from cache
    assert posterior is not None