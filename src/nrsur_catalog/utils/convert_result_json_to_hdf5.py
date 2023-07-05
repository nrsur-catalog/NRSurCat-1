from glob import glob

import numpy as np
from bilby.gw.result import CBCResult
from tqdm import tqdm


def compute_ln_prior(result: CBCResult) -> np.ndarray:
    """Compute the log prior for a result object"""
    priors = result.priors
    priors_keys = list(priors.keys())
    # drop any keys with "recalib"
    priors_keys = [key for key in priors_keys if "recalib" not in key]
    samples = result.posterior[priors_keys]
    ln_prior = np.array([priors[key].ln_prob(samples[key]) for key in priors_keys])
    ln_prior = np.sum(ln_prior, axis=0)
    return ln_prior


def convert_result_json_to_hdf5(json_path: str):
    """Convert a result.json file to a result.hdf5 file.

    Parameters


    for key in result.posterior:
        print(key, result.posterior[key].dtype)

    ----------
    json_path: str
        The path to the result.json file.
    """
    result = CBCResult.from_json(json_path)
    result.sampling_time = result.sampling_time.total_seconds()
    result.posterior["log_prior"] = compute_ln_prior(result)
    col_to_drop = ["catch_waveform_errors", "waveform_approximant"]
    result.posterior = result.posterior.drop(columns=col_to_drop)
    for key in result.posterior:
        result.posterior[key] = np.array(result.posterior[key].tolist())
    hdf5_path = json_path.replace("result.json", "result.hdf5")
    result.save_to_file(hdf5_path, extension="hdf5")


def convert_all_result_json_to_hdf5(result_regex: str):
    """Convert all result.json files to result.hdf5 files"""
    for json_path in tqdm(glob(result_regex), desc="Converting"):
        convert_result_json_to_hdf5(json_path)
