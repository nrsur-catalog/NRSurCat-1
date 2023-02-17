import os
from glob import glob
from typing import List, Union
import re

from .logger import logger
from .utils import get_event_name

CACHE_ENV_VAR = "NRSUR_CATALOG_CACHE_DIR"
DEFAULT_CACHE_DIR = "~/.nrsur_catalog_cache"
FILE_EXTENSION = "_NRSur7dq4_merged_result.json"


class _CatalogCache:
    def __init__(self):
        self._cache = os.environ.get(CACHE_ENV_VAR, None)

    @property
    def cache_dir(self) -> str:
        """Get the cache directory environment variable"""
        if self._cache is None:
            logger.warning(
                f"Cache dir not set, setting default cache dir: {DEFAULT_CACHE_DIR}"
            )
            self._cache = DEFAULT_CACHE_DIR
        return self._cache

    @cache_dir.setter
    def cache_dir(self, cache_dir: str) -> None:
        """Set the cache directory environment variable"""
        env_cache = os.environ.get(CACHE_ENV_VAR, None)
        if env_cache is not None and env_cache != cache_dir:
            logger.warning(
                f"Overwriting cache dir {env_cache} with {cache_dir}"
            )
        os.environ[CACHE_ENV_VAR] = cache_dir
        self._cache = cache_dir
        os.makedirs(self._cache, exist_ok=True)

    @property
    def list(self) -> List[str]:
        """List the contents of the cache directory (sorted by number in filename)"""
        file_regex = os.path.join(self.cache_dir, f"*{FILE_EXTENSION}")
        files =  glob(file_regex)
        files = sorted(
            files,
            key=lambda x: int(re.findall(r"\d+", os.path.basename(x))[0])
        )
        return files

    @property
    def event_names(self) -> List[str]:
        """List the event names in the cache directory"""
        return [get_event_name(f) for f in self.list]

    def find(self, name: str, hard_fail=False) -> Union[str, None]:
        """Find a file in the cache directory"""
        filepath = f"{self.cache_dir}/{name}{FILE_EXTENSION}"
        if os.path.exists(filepath):
            return filepath
        if hard_fail:
            logger.debug(
                f"Current cache: {self.list} (doesnt have {filepath})"
            )
            raise FileNotFoundError(
                f"Could not find {name} in cache dir {self.cache_dir}"
            )
        return None


CACHE = _CatalogCache()  # create a singleton instance of the cache
