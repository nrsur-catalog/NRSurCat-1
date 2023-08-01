# [NRSurrogate catalog](https://cjhaster.github.io/NRSurrogateCatalog)
GW event posteriors obtained using numerical relativity surrogate models

This repository contains the code used to generate the NRSur catalog website and its API.


To generate the website, run:
```bash
build_nrsur_website --event-dir DIR_WITH_RESULTS --outdir out_test_website
ghp-import -n -p -f out_test_website/_build/html
upload_to_zenodo test_cache_dir
rm -rf test_cache_dir
```



## Development



```bash
pip install -e .[dev]
```

Generate a test website:
```bash
python tests/generate_mock_data.py
upload_to_zenodo "tests/test_cache_dir/*.json"
build_nrsur_website --event-dir tests/test_cache_dir --outdir out_test_website
ghp-import -n -p -f out_test_website/_build/html
rm -rf test_cache_dir
```
