# Website Deployment Notes



```bash
cd do
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



To generate the main website, run:
```bash
build_nrsur_website --event-dir DIR_WITH_RESULTS --outdir out_test_website
ghp-import -n -p -f out_test_website/_build/html
upload_to_zenodo test_cache_dir
rm -rf test_cache_dir
```


Update zenodo URL file:
```bash
zenodo_get --wget='src/nrsur_catalog/api/nrsur_urls.txt' -r 8115310
````