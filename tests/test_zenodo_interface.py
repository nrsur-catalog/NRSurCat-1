import unittest
from nrsur_catalog.api import zenodo_interface



def test_update_cache():
    zenodo_interface.cache_zenodo_urls_file(sandbox=True)

def test_names_of_events():
    events = zenodo_interface.get_zenodo_urls()
    event0 = list(events.keys())[0]
    present, name = zenodo_interface.check_if_event_in_zenodo(event0)
    assert present

def test_zenodo_check():
    assert zenodo_interface.check_if_event_in_zenodo("GW150914", lvk_posteriors=True)

if __name__ == "__main__":
    unittest.main()
