from nrsur_catalog.api.download_event import main, get_cli_args
import pytest
from nrsur_catalog.logger import logger

from _pytest.logging import LogCaptureFixture


@pytest.fixture(autouse=True)
def caplog(caplog: LogCaptureFixture):
    """
    Make pytest work with loguru. See:
    https://loguru.readthedocs.io/en/stable/resources/migration.html#making-things-work-with-pytest-and-caplog
    """
    handler_id = logger.add(caplog.handler, format="{message}")
    yield caplog
    logger.remove(handler_id)


def test_arg_parser():
    """Test the argparser"""
    event_name, all, cache_dir, clean = get_cli_args(args=["--event-name", "GW150914"])
    assert event_name == "GW150914"
    assert all is False
    assert cache_dir == "./.nrsur_catalog_cache"
    assert clean is False

    event_name, all, cache_dir, clean = get_cli_args(args=["--all"])
    assert event_name == ""
    assert all is True
    assert cache_dir == "./.nrsur_catalog_cache"
    assert clean is False

    # check that the following raises an error
    with pytest.raises(ValueError, match="Either --all or --event-name must be specified"):
        get_cli_args(args=["--cache-dir", "./.nrsur_catalog_cache"])

    with pytest.raises(ValueError, match="Either --all or --event-name must be specified"):
        get_cli_args(args=["--all", "--event-name", "GW150914"])


@pytest.fixture
def mock_download(monkeypatch):
    """Mock the download function from nrsur_catalog.utils.download
    download(url: str, fname: str) -> None:

    Generate a fake tmp file in a tmp dir with the appropriate name
    """

    def mock_nrsur_download(url, fname):
        """Mock the mock_nrsur_download function"""
        # Create a fake file
        with open(fname, "w") as f:
            f.write("")

    # Monkeypatch the requests.get function
    monkeypatch.setattr("nrsur_catalog.utils.download", mock_nrsur_download)


def test_download_event(mock_download, tmp_path, caplog):
    base_args = ["--cache-dir", str(tmp_path)]
    event_name = "GW150914_095045"
    fname = f"{tmp_path}/{event_name}_NRSur7dq4.h5"
    # download the event for the 1st time
    main(args=["--event-name", event_name] + base_args)
    assert f"Downloading {event_name} from the NRSur Catalog -> {fname}" in caplog.text
    assert "Download completed!" in caplog.text
    # trying to redownload the event (should not download it again)
    main(args=["--event-name", event_name] + base_args)
    assert f"File for {event_name} already downloaded: {fname}" in caplog.text
    # trying to redownload the event (with clean)
    main(args=["--event-name", event_name, '--clean'] + base_args)
    assert f"Downloading {event_name} from the NRSur Catalog -> {fname}" in caplog.text
    assert "Download completed!" in caplog.text


def test_download_all_missing_events(mock_download, tmp_path, caplog):
    base_args = ["--cache-dir", str(tmp_path)]
    # download one event
    main(args=["--event-name", "GW150914_095045"] + base_args)
    # download all missing events
    main(args=["--all"] + base_args)
    # 47 events in total, 1 already downloaded
    assert "Downloading all 46 events..." in caplog.text


def test_download_fake_event(mock_download, tmp_path, caplog):
    base_args = ["--cache-dir", str(tmp_path)]
    event_name = "GW150912"
    # download the event for the 1st time
    main(args=["--event-name", event_name] + base_args)
    assert f"Event {event_name} not found on Zenodo. Please choose an event from:" in caplog.text
    assert "0) GW150914_095045" in caplog.text
