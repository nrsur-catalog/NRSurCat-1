"""Prints out the data dicts for the videos in the csv files."""
import pandas as pd
from nrsur_catalog.api.zenodo_interface import get_analysed_event_names
from nrsur_catalog.utils import get_event_name

SPINS_CSV = "spin_playlist_data.csv"
REMNANT_CSV = "remnant_playlist_data.csv"


def read_csv(fname):
    df = pd.read_csv(fname)
    # check that "title,id,thumbnail" are present as columns
    assert "title" in df.columns
    assert "id" in df.columns
    # covert " " to "_" in the title column
    df["title"] = df["title"].str.replace(" ", "_")
    # only keep 1 unique title
    df = df.drop_duplicates(subset=["title"])
    return df


def __get_missing_events(vid_titles, expected_event_names):
    vid_event_names = {get_event_name(vid) for vid in vid_titles}
    expected_event_names = set(expected_event_names)
    if vid_event_names != expected_event_names:
        missing_events = expected_event_names - vid_event_names
        return missing_events
    return []


def __check_all_vids_present(vid_df, type="remnant"):
    all_events = get_analysed_event_names()
    # check that all the videos are present (ie 47 spins and 47 remnants)
    if len(vid_df) != 47:
        print(f"WARNING: Expected 47 {type} vids, got {len(vid_df)}")
        missing_events = __get_missing_events(vid_df.title, all_events)
        if missing_events:
            print(f"WARNING: Missing {type} vids for {missing_events}")
            for event in missing_events:
                if event is not None:
                    print(f"scp $pcdev5:/home/vijay.varma/For_Avi/movies/{event}_{type}.mp4 .")


def get_data_dicts(df):
    dat_str = "dict(\n"
    for _, row in df.iterrows():
        dat_str += f"{row.title}= '{row.id}',\n"
    dat_str += ")\n"
    return dat_str


if __name__ == '__main__':
    spins_df = read_csv(SPINS_CSV)
    remnant_df = read_csv(REMNANT_CSV)
    print(f"Number of spins videos: {len(spins_df)}")
    __check_all_vids_present(spins_df)

    print(f"Number of remnant videos: {len(remnant_df)}")
    __check_all_vids_present(remnant_df)


    print("\n\n")

    print(f"SPIN_VIDEO = {get_data_dicts(spins_df)}")
    print("\n\n")
    print(f"REMNANT_VIDEO = {get_data_dicts(remnant_df)}")
