"""Module to get zenodo URLs from NRSur Catlog zenodo page"""
import functools
import os
import re
from typing import Dict, List

from ..logger import logger
from ..utils import get_event_name

HERE = os.path.dirname(os.path.abspath(__file__))
LVK_URL_FILE = os.path.join(HERE, "lvk_urls.txt")
NR_URL_FILE = os.path.join(
    HERE, "nrsur_urls.txt"
)  # This file's contents are autogenerated
TITLE = "NRSurrogate Catalog Posteriors"


def _commit_url_file():
    try:
        import git

        repo_root = os.path.join(HERE, "../../..")
        repo = git.Repo(repo_root)
        repo.git.add(NR_URL_FILE)
        repo.git.commit(m=f"update urls [automated]")
        repo.git.push()
    except Exception as e:
        pass


def cache_zenodo_urls_file(sandbox=True) -> None:
    """Update the file URLs to the data on zenodo"""
    from zenodo_python import Deposition

    zeno = Deposition.from_title(title=TITLE, test=sandbox)
    logger.info(f"Zenodo {zeno} has {len(zeno.files)} files. Caching download URLs.")
    zeno.save_wget_file(NR_URL_FILE)
    file_contents = open(NR_URL_FILE, "r").read()
    logger.info(f"Finished caching Zenodo URLs to {NR_URL_FILE}:\n{file_contents}")
    _commit_url_file()


def get_zenodo_urls(lvk_posteriors=False) -> Dict[str, str]:
    """Returns a dictionary of the analysed events and their urls"""

    url_file = NR_URL_FILE
    if lvk_posteriors:
        url_file = LVK_URL_FILE

    # read in the zenodo_urls.txt file (each line is a url)
    with open(url_file, "r") as f:
        urls = f.readlines()
        urls = [url.strip() for url in urls]

    if len(urls) == 0:
        raise RuntimeError(f"No URLs found in {url_file}")

    # extract the event name from the url
    event_names = [get_event_name(url) for url in urls]
    return dict(zip(event_names, urls))


def check_if_event_in_zenodo(event_name: str, lvk_posteriors=False) -> bool:
    """Check if the event is in Zenodo"""

    present = False
    urls_dict = get_zenodo_urls(lvk_posteriors)

    shortname = event_name.split("_")[0]
    fullname = shortname + r"\_\d{6}"

    if event_name in urls_dict:
        present = True
    elif shortname in urls_dict:
        present = True
        event_name = shortname
    else:
        for name in urls_dict.keys():
            if re.match(fullname, name):
                present = True
                event_name = name
                break

    return present, event_name


@functools.lru_cache
def get_analysed_event_names(lvk_posteriors=False) -> List[str]:
    """Return a list of analysed events.

    Parameters
    ----------
        lvk_posteriors: Optional[bool]
            True if you want to return the names of the analysed LVK events.
            False if you want to return the names of the analysed NRSur cat events.
    """
    return list(set(get_zenodo_urls(lvk_posteriors).keys()))