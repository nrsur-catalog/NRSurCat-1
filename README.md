# NRSur Catalog

This repository contains the code used to generate the NRSur catalog website and its API.

## Development

```bash
pip install -e .[dev]
```

Generate the website:
```bash
build_nrsur_website --fit-dir /home/tousif.islam/NRSurCatalog/merged_results --outdir ../nrsur_web
```
This command will
- look for the NRSur fits in the `fit-dir`
- save the website in the `outdir`