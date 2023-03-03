# NRSurrogate Catalog

We present the posterior samples of the 47 GW events with signal durations 
less than 64 seconds from the 
NRSurrogate Catalog {cite}`NRSurrogate_Catalog`.
The catalog fits use the [NRSur7dq4] {cite}`NRSur7dq4` surrogate model.
For details on the analysis, please refer to the [catalog paper].


**Main Dependencies**

All fits were performed with ❤️ using:

*   [NRSur7dq4] {cite}`NRSur7dq4`
*   [bilby] {cite}`bilby_paper`
*   [dynesty] {cite}`dynesty_paper`


---

## Citation
If you make use of this *NRSurrogate Catalog*, please cite this work 
and its dependencies. 

Please add the following line within your methods, conclusion 
or acknowledgements
sections:

>    This research has made use of 
>    NRSurrogate Catalog v1.0~\cite{NRSurrogate_Catalog_v1}, 
>    generated using the waveform NRSur7dq4~\cite{NRSur7dq4},
>    and the \textsc{bilby} Bayesian inference 
>    libraries~\cite{bilby, parallel_bilby}.
>    Bayesian parameter estimation was performed using 
>    \textsc{dynesty}~\cite{dynesty_paper, skilling2004, skilling2006}, 
>    a nested sampler.

```{literalinclude} references.bib
```

```{bibliography}
:style: unsrt
```


## License & attribution

Copyright 2023 NRSur Catalog team.

The source code is made available under the terms of the MIT license.


[catalog paper]: https://arxiv.org/abs/2301.07215
[NRSur7dq4]: https://arxiv.org/abs/2301.07215
[bilby]: https://lscsoft.docs.ligo.org/bilby/index.html
[dynesty]: https://dynesty.readthedocs.io/
