## HACKY SCRIPT TO PLOT CUMULATIVE MEMORY SIZE OF JSON AND HDF5 FILES`
import matplotlib.pyplot as plt
import os
import glob
import pandas as pd

DIR = "/home/avaj040/Documents/projects/data/nrsur_results/"


def get_memsize_in_gb(path):
    bytesize = os.path.getsize(path)
    return bytesize / (1024 * 1024 * 1024)


def get_memsize_df(rootdir):
    jsons = glob.glob(f"{rootdir}/*.json")
    hdf5s = glob.glob(f"{rootdir}/*.hdf5")
    assert len(jsons) == len(hdf5s)
    # SORT BY EVENT NAME
    event_names = [j.split("/")[-1].split(".")[0] for j in jsons]
    jsons = [j for _, j in sorted(zip(event_names, jsons))]
    hdf5s = [h for _, h in sorted(zip(event_names, hdf5s))]
    df = pd.DataFrame(dict(
        name=event_names,
        json=[get_memsize_in_gb(j) for j in jsons],
        hdf5=[get_memsize_in_gb(h) for h in hdf5s],
    ))
    return df


df = get_memsize_df(DIR)
# plot CDF of memsizes
nums = range(len(df))
plt.step(nums, df["json"].cumsum(), label="json")
plt.step(nums, df["hdf5"].cumsum(), label="hdf5")
plt.legend()
plt.xlabel("Event Number")
plt.ylabel("Cumulative Memory Size (GB)")
plt.savefig("memsizes.png")