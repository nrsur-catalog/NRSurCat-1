NRSurCat-1
===========

We present, **NRSurCat-1**, the catalog of posterior samples associated with the paper "Analysis of GWTC-3 with fully precessing numerical relativity surrogate models" {cite:p}`nrsurcat_1`.
This includes 47 binary black hole gravitational wave events (from 2015-2020, LVK O1-O3) analyzed using the `NRSur7dq4` and `NRSur7dq4Remnant` models.

.. image:: https://s11.gifyu.com/images/SQfBI.gif
   :alt: NRSurCat-1

This website contains plots of `NRSurCat-1` posteriors and example code for downloading and interacting with the results.

`events/gw_menu_page.ipynb`
    : Contains a list of all analyzed events with links to their pages (containing `corner plots`_ and `animations`_ for the events).

`catalog_plots.ipynb`
    : Demonstrates how to load the entire catalog and make plots.

`api.rst`
    : Describes the python and command-line interface to the catalog package.

Data availability
-----------------

The posterior samples are available on `Zenodo`_ and can also be downloaded using the python-API, `nrsur_catalog`_:

.. tab-set::

   .. tab-item:: Using CLI
      :sync: key1

      .. code-block:: bash

         ! pip install nrsur_catalog
         get_nrsur_event --event-name GW150914_095045
         get_nrsur_event --all

      See more on the `catalog API page`_.

   .. tab-item:: Using py
      :sync: key2

      Load samples from one event with

      .. code-block:: python

         from nrsur_catalog import NRsurResult

         nrsur_result = NRsurResult.load("GW150914_095045")

      For example, refer to the `page for GW150914_095045`_.

      Load samples from all events with

      .. code-block:: python

         from nrsur_catalog import Catalog

         catalog = Catalog.load()

      See more on the `catalog plots page`_.

Citation
--------

If you make use of this *NRSurrogate Catalog*, please cite this work and its dependencies.

.. literalinclude:: references.bib


License & attribution
---------------------

All analyses were performed with ❤️ using:

- `NRSur7dq4`_
- `parallel_bilby`_
- `dynesty`_

Copyright 2023 NRSur Catalog team.

The source code is made available under the terms of the MIT license.

Website acknowledgements
------------------------

This website was generated using `Jupyter book`_ and code from `Dan Foreman-Mackey`_'s `TESS Atlas`_ project.

.. _corner plots: https://nrsur-catalog.github.io/NRSurCat-1/events/GW150914_095045.html#corner-plots
.. _animations: https://nrsur-catalog.github.io/NRSurCat-1/events/GW150914_095045.html#animations
.. _catalog plots page: catalog_plots.ipynb
.. _Zenodo: https://zenodo.org/record/8115310
.. _nrsur_catalog: https://pypi.org/project/nrsur-catalog/
.. _catalog API page: api.rst
.. _page for GW150914_095045: events/GW150914_095045.ipynb
.. _NRSur7dq4: https://arxiv.org/abs/2301.07215
.. _parallel_bilby: https://git.ligo.org/lscsoft/parallel_bilby
.. _dynesty: https://dynesty.readthedocs.io/
.. _Jupyter book: https://jupyterbook.org/
.. _Dan Foreman-Mackey: https://dfm.io/
.. _TESS Atlas: https://github.com/dfm/tess-atlas
