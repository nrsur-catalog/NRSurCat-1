---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.4
  kernelspec:
    display_name: venv
    language: python
    name: venv
---

# Catalog plots 

Here we have some catalog plots showing the ensemble results of the catalog

```python
from nrsur_catalog import Catalog

catalog = Catalog.load()
```

```python
catalog.violin_plot('mass_1');
```

```python
catalog.violin_plot('chi_eff');
```
