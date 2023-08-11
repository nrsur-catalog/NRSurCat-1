import re
from typing import Dict, List

import bilby
import h5py
import numpy as np
import pandas as pd
from bilby.core.utils.io import recursively_load_dict_contents_from_group
from bilby.gw.prior import BBHPriorDict
from bilby.gw.result import CBCResult


def pesummary_to_bilby_result(pesummary_result: str):
    """Convert a pesummary result to a bilby result

    parameters
    ----------
    pesummary_result: str
        The path to the pesummary result file

    returns a bilby result object
    """
    try:
        with h5py.File(pesummary_result, "r") as f:
            data = recursively_load_dict_contents_from_group(f, "/")
    except OSError:
        raise OSError(f"The cached {pesummary_result} is corrupt. Please re-download.")

    data = data["Bilby:NRSur7dq4"]
    priors = _parse_prior(data["priors"]["analytic"])
    meta_data = _recursively_unrwap_dict(data["meta_data"]["other"])
    meta_data["likelihood"][
        "parameter_conversion"
    ] = bilby.gw.conversion.convert_to_lal_binary_black_hole_parameters
    meta_data["likelihood"][
        "frequency_domain_source_model"
    ] = bilby.gw.source.lal_binary_black_hole
    meta_data["likelihood"][
        "waveform_generator_class"
    ] = bilby.gw.waveform_generator.WaveformGenerator
    meta_data["likelihood"][
        "time_domain_source_model"
    ] = bilby.gw.source.lal_binary_black_hole

    return CBCResult(
        posterior=_parse_posterior(data["posterior_samples"]),
        priors=priors,
        meta_data=meta_data,
        search_parameter_keys=list(priors.keys()),
    )


def _parse_prior(p: Dict[str, List[str]]) -> BBHPriorDict:
    """Parse a prior string into a bilby prior object

    parameters
    ----------
    p: dict
        p = {
        'a_1': ["Uniform(minimum=0,...)"],
        'a_2': ["Uniform(minimum=0,...)"],
        ...
        }

    returns a bilby prior object
    """
    pri = {k: v[0] for k, v in p.items()}
    # convert 'UniformInComponentsChirpMass' to 'bilby.gw.prior.UniformInComponentsChirpMass'
    for k, v in pri.items():
        if "UniformInComponentsChirpMass" in v:
            full = "bilby.gw.prior.UniformInComponentsChirpMass"
            if full not in v:
                v = v.replace("UniformInComponentsChirpMass", full)
            pri[k] = v
        elif "UniformSourceFrame" in v:
            full = "bilby.gw.prior.UniformSourceFrame"
            v1 = v
            if full not in v:
                v1 = v.replace("UniformSourceFrame", full)
            regex = re.compile(r"cosmology=FlatLambdaCDM\((.*)\), name")
            v1 = regex.sub(r"name", v1)
            v1 = v1.replace("""Unit("Mpc")""", "'Mpc'")
            pri[k] = v1
        elif "UniformInComponentsMassRatio" in v:
            full = "bilby.gw.prior.UniformInComponentsMassRatio"
            if full not in v:
                v = v.replace(
                    "UniformInComponentsMassRatio",
                    full,
                )
            pri[k] = v
    pri = BBHPriorDict(pri)
    return pri


def _parse_posterior(post: np.ndarray) -> pd.DataFrame:
    return pd.DataFrame({name: post[name][:] for name in post.dtype.names})


def _recursively_unrwap_dict(d: Dict[str, List[str]]) -> Dict[str, str]:
    res = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = _recursively_unrwap_dict(v)

        if isinstance(v, np.ndarray) or isinstance(v, list):
            if len(v) == 1:
                v = v[0]

        if isinstance(v, str):
            if "None" in v:
                v = None
        res[k] = v

    return res
