python generate_mock_data.py
build_nrsur_website --event-dir test_cache_dir --outdir out_test_website
ghp-import -n -p -f out_test_website/_build/html
rm -rf test_cache_dir