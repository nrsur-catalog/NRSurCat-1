"""Generate the video-info.json needed for the youtube-uploader"""
import os
import sys
import glob
import json
import re
from typing import Tuple

VIDEO_INFO_FILE = 'video_info.json'

DESCRIPTION = {}
DESCRIPTION['spins'] = """
Posterior samples for the dimensionless spin vectors (chi1, chi2) of the component black holes for the gravitational wave event {GW_NAME}, accompanying the paper "Analysis of GWTC-3 with fully precessing numerical relativity surrogate models", Islam et al. (2023).

Each purple marker indicates a posterior sample; an arrow drawn from the origin to the marker would show the spin vector. The outer radii of the spheres correspond to the maximum spin magnitude of 1. The spins are shown in the "wave frame" defined at a reference frequency of 20 Hz. The x-axis (orange) and y-axis (green) are shown as arrows near the origin; the x-y plane is orthogonal to the orbital angular momentum direction. The color reflects posterior probability density.

Video credit: Vijay Varma
"""

DESCRIPTION["remnant"] = """
Posterior samples for the dimensionless spin vector (chif) and the recoil kick velocity (vf, units of km/s) of the final black hole for the gravitational wave event {GW_NAME}, accompanying the paper "Analysis of GWTC-3 with fully precessing numerical relativity surrogate models", Islam et al. (2023).

Each purple marker indicates a posterior sample; an arrow drawn from the origin to the marker would show the spin or kick vector. For the spin, the outer radii of the spheres correspond to the maximum spin magnitude of 1. For the kick, the outer radius of the sphere corresponds to a kick magnitude of 2500 km/s. The remnant spin and kick are shown in the "wave frame" defined at a reference time of -100 M_det before the peak waveform amplitude, where M_det is the detector frame total mass. The x-axis (orange) and y-axis (green) are shown as arrows near the origin; the x-y plane is orthogonal to the orbital angular momentum direction. The color reflects posterior probability density.

Video credit: Vijay Varma
"""


def get_gw_name_and_video_type_from_fname(fname: str) -> Tuple[str, str]:
    """
    Given a fname, extract the GW-name and the type (either remnant or spins)
    GW190517_055101_remnant.mp4 --> GW190517_055101, remnant
    GW190916_200658_spins.mp4 --> GW190916_200658, spins
    """
    file_basename = os.path.splitext(os.path.basename(fname))[0]

    gw_name_match = re.search(r'(GW\d{6}_\d{6})', file_basename)
    if gw_name_match:
        gw_name = gw_name_match.group(1)
    else:
        raise ValueError(f"GW name not found in {fname}.")

    vid_type = file_basename.split("_")[-1]
    return gw_name, vid_type


def generate_video_info(video_folder):
    video_info = []

    if os.path.exists(VIDEO_INFO_FILE):
        with open(VIDEO_INFO_FILE, 'r') as file:
            video_info = json.load(file)

    existing_video_paths = [entry['path'] for entry in video_info]

    video_files = glob.glob(os.path.join(video_folder, '*.mp4'))  # Adjust the file extension if needed
    for video_file in video_files:
        if video_file not in existing_video_paths:
            gw_name, vid_type = get_gw_name_and_video_type_from_fname(video_file)
            title = f"{gw_name} {vid_type}"
            description = DESCRIPTION[vid_type]

            video_entry = {
                'path': video_file,
                'title': title,
                'description': description.format(GW_NAME=gw_name),
                'uploaded': False,
                'youtube_id': ''
            }
            video_info.append(video_entry)

    return video_info


def save_video_info(video_info):
    with open(VIDEO_INFO_FILE, 'w') as file:
        json.dump(video_info, file, indent=4)


def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_video_info_json.py <video_folder>")
        return

    video_folder = sys.argv[1]
    video_info = generate_video_info(video_folder)
    save_video_info(video_info)


if __name__ == "__main__":
    main()
