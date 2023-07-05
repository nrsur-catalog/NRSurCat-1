import os
import re
from glob import glob
from typing import List

from .api.zenodo_interface import get_analysed_event_names
from .logger import logger
from .utils import get_event_name

CACHE_ENV_VAR = "NRSUR_CATALOG_CACHE_DIR"
DEFAULT_CACHE_DIR = "./.nrsur_catalog_cache"
NR_FILE_EXTENSION = "_NRSur7dq4.h5"
LVK_FILE_EXTENSION = "_PEDataRelease_mixed_cosmo.h5"

NR_LABEL = "Bilby:NRSur7dq4"
LVK_LABEL = "C01:IMRPhenomXPHM"


class CatalogCache:
    """CatalogCache helps
    - check which files are in the cache
    - download any required new files
    """

    def __init__(self, cache_dir: str):
        """Class to handle the cache directory"""
        assert cache_dir is not None, "Cache directory must be specified"
        self._cache = cache_dir
        os.makedirs(self._cache, exist_ok=True)

    @property
    def dir(self) -> str:
        return os.path.abspath(self._cache)

    @property
    def list(self):
        return self._list()

    @property
    def list_lvk(self):
        return self._list(lvk_posteriors=True)

    def _list(self, lvk_posteriors=False) -> List[str]:
        """List the contents of the cache directory (sorted by number in filename)"""
        file_extension = LVK_FILE_EXTENSION if lvk_posteriors else NR_FILE_EXTENSION
        file_regex = os.path.join(self._cache, f"*{file_extension}")
        files = glob(file_regex)
        files = sorted(
            files, key=lambda x: int(re.findall(r"\d+", os.path.basename(x))[0])
        )
        return files

    @property
    def event_names(self) -> List[str]:
        """List the event names in the cache directory"""
        return [get_event_name(f) for f in self.list]

    @property
    def num_events(self) -> int:
        """Number of events in the cache directory"""
        return len(self.event_names)

    @property
    def event_names_lvk(self) -> List[str]:
        """List the event names in the cache directory"""
        return [get_event_name(f) for f in self.list_lvk]

    def find(self, name: str, hard_fail=False, lvk_posteriors=False) -> str:
        """Find a file in the cache directory"""
        file_extension = LVK_FILE_EXTENSION if lvk_posteriors else NR_FILE_EXTENSION
        fileregex = os.path.join(self._cache, f"*{name}*{file_extension}")
        filepath = glob(fileregex)
        if len(filepath) == 1:
            return filepath[0]
        if hard_fail:
            logger.debug(f"Current cache: {self.list} doesnt have {filepath}")
            raise FileNotFoundError(
                f"Could not find {name} in cache dir {self.dir}. "
                f"Is filepath:{filepath} present in the cache dir:"
                f"Listdir: {os.listdir(self.dir)}"
            )
        return ""

    def check_if_events_cached_in_zenodo(self, lvk_posteriors=False):
        """Return a list of events that are in the cache and in Zenodo"""
        zenodo_events = set(self.zenodo_events)
        local_events = set(self.event_names)
        if zenodo_events != local_events:
            logger.warning(
                f"Events in cache do not match events in Zenodo.\n"
                f"local: {local_events},\n"
                f"zenodo: {zenodo_events},\n"
                f"missing: {zenodo_events - local_events},\n"
                "Uploading the events to zenodo after building the website."
            )

    @property
    def is_empty(self) -> bool:
        return len(self.list) == 0

    @property
    def missing_events(self):
        zenodo_events = set(self.zenodo_events)
        local_events = set(self.event_names)
        return zenodo_events - local_events

    @property
    def is_incomplete(self) -> bool:
        """If not all events analysed are present"""
        return len(self.missing_events) != 0

    @property
    def zenodo_events(self) -> List[str]:
        if not hasattr(self, "__zenodo_events"):
            self.__zenodo_events = get_analysed_event_names()
        return self.__zenodo_events

    def __repr__(self):
        return f"CatalogCache(nrfiles={len(self.list)}, lvkfiles={len(self.list_lvk)}, cache_dir={self._cache})"
