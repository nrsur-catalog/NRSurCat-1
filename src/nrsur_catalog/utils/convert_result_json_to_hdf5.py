from bilby.gw.result import CBCResult
from glob import glob
from tqdm import tqdm


def convert_result_json_to_hdf5(json_path: str):
    """Convert a result.json file to a result.hdf5 file.

    Parameters
    ----------
    json_path: str
        The path to the result.json file.
    """
    result = CBCResult.from_json(json_path)
    hdf5_path = json_path.replace("result.json", "result.hdf5")
    result.save_to_file(hdf5_path, extension="hdf5")


def convert_all_result_json_to_hdf5(result_regex: str):
    """Convert all result.json files to result.hdf5 files"""
    for json_path in tqdm(glob(result_regex), desc="Converting"):
        convert_result_json_to_hdf5(json_path)
