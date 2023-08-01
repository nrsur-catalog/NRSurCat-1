from generate_mock_data import write_pesummary_like_result, get_mock_cache_dir
import pytest
from nrsur_catalog.logger import logger
import os

@pytest.fixture
def mock_download(monkeypatch):
    from nrsur_catalog import utils

    def _mock_download(url, path):
        logger.info("<<MOCKING DOWNLOAD>>")
        write_pesummary_like_result(path)

    monkeypatch.setattr(utils, "download", _mock_download)

@pytest.fixture
def mock_nrsur_result(tmpdir):
    path = f"{tmpdir}/GW101010_NRSur7dq4.h5"
    write_pesummary_like_result(path, 'Bilby:NRSur7dq4')
    return path


@pytest.fixture
def mock_cache_dir(tmpdir):
    return get_mock_cache_dir(test_dir=tmpdir, num_events=3)
