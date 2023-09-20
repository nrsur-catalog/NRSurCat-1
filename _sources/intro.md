# NRSurCat-1

We present, **NRSurCat-1**, the catalog of posterior samples associated with the paper "Analysis of GWTC-3 with fully precessing numerical relativity surrogate models", [Islam et al, 2023](PAPER). 
This includes 47 binary black hole gravitational wave events (from 2015-2020, LVK O1-O3) analyzed using the [NRSur7dq4](https://arxiv.org/abs/1905.09300) and [NRSur7dq4Remnant](https://arxiv.org/abs/1905.09300) models.

![](https://s11.gifyu.com/images/SQfBI.gif)

This website contain plots of `NRSurCat-1` posteriors and example code for downloading and interacting with the results. The pages in this website are:

[](events/gw_menu_page.md) 
: Contains a list of all analysed events with links to their pages, containing [corner plots](https://nrsur-catalog.github.io/NRSurCat-1/events/GW150914_095045.html#corner-plots) and [animations](https://nrsur-catalog.github.io/NRSurCat-1/events/GW150914_095045.html#animations) for the events, such as:

 <video width="630" height="315" controls muted loop autoplay><source src="https://nrsur-catalog.github.io/NRSurCat-1-animations-remnant/GW150914_095045_remnant.mp4" type="video/mp4">
 </video>
 <video width="630" height="315" controls muted loop autoplay><source src="https://nrsur-catalog.github.io/NRSurCat-1-animations-spins/GW150914_095045_spins.mp4" type="video/mp4"></video>

[](catalog_plots.ipynb)
: Demonstrates how to load the entire catalog and make plots.

[](api.rst)
: Describes the python and command-line interface to the catalog package.



## Data availability

The posterior samples are available on [Zenodo](https://zenodo.org/record/8115310) and can also be downloaded 
using the python-API, [nrsur_catalog](https://pypi.org/project/nrsur-catalog/):


::::{tab-set}

:::{tab-item} Using CLI 
:sync: key1

```bash
! pip install nrsur_catalog
get_nrsur_event --event-name GW150914_095045 
get_nrsur_event --all
```
See more on the [catalog API page](api.rst).
:::

:::{tab-item} Using py
:sync: key2

Load samples from one event with
```python
from nrsur_catalog import NRsurResult

nrsur_result = NRsurResult.load("GW150914_095045")

```
For example, refer to the [page for GW150914_095045](events/GW150914_095045.ipynb).

Load samples from all events with
```python
from nrsur_catalog import Catalog

catalog = Catalog.load()

```
See more on the [catalog plots page](catalog_plots.ipynb).
:::

::::


(citation_section)=
## Citation

If you make use of the *NRSurCat-1*, please cite this work 
and its dependencies. 


```{literalinclude} references.bib
```


## License & attribution

All analyses were performed with ❤️ using:

*   [NRSur7dq4](https://arxiv.org/abs/1905.09300)
*   [parallel_bilby](https://git.ligo.org/lscsoft/parallel_bilby)
*   [dynesty](https://dynesty.readthedocs.io/)

Copyright 2023 NRSur Catalog team.

The source code is made available under the terms of the MIT license.

## Website acknowledgements
This website was generated using [`Jupyter book`](https://jupyterbook.org/) and code from [Dan Foreman-Mackey](https://dfm.io/)'s [TESS Atlas](https://github.com/dfm/tess-atlas) project.

[catalog paper]: https://arxiv.org/abs/2301.07215
[NRSur7dq4]: https://arxiv.org/abs/2301.07215
[bilby]: https://lscsoft.docs.ligo.org/bilby/index.html
[dynesty]: https://dynesty.readthedocs.io/
