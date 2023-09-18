.. module:: nrsur_catalog

.. _api:

API documentation
=================

Here we provide a brief overview of the API. For more details, see the docstrings of the individual classes and functions.


CLI to download results
-----------------------

.. argparse::
   :module: nrsur_catalog.api.download_event
   :func: create_parser
   :prog: get_nrsur_event



Catalog
-------

.. autoclass:: nrsur_catalog.catalog.Catalog
   :members: load, to_dict_of_posteriors, get_all_posteriors, get_event_posterior, get_analysed_event_names, violin_plot, plot_2d_posterior


NRSurrogate Result
------------------
The NRSurrogate result class inherits the `bilby.gw.result.CBCResult <https://lscsoft.docs.ligo.org/bilby/api/bilby.gw.result.CompactBinaryCoalescenceResult.html#bilby.gw.result.CompactBinaryCoalescenceResult>`_ class. It has some additional functionality to load the NRSurrogate result from the h5 format into a python object, and some additional plotting functionality.


.. autoclass:: nrsur_catalog.nrsur_result.NRsurResult
   :members: load, posterior, lvk_result, plot_corner, plot_lvk_comparison_corner



