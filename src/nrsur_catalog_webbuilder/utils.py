import os

import pandas as pd

from nrsur_catalog import Catalog
from nrsur_catalog.utils import LATEX_LABELS
from nrsur_catalog import __website__
from PIL import Image

from .video_links import get_video_html

LINK = "[{txt}]({l})"

ANIM_CELL = """
# + [markdown] tags=["full-width"]
# ## Animations  
# Here are some animations of the posterior.
# 
# |Spin       | 
# |-----------|
# | {spin}    |  
# 
# Posterior samples for the dimensionless spin vectors (chi1, chi2) 
# of the component black holes. Each purple marker indicates a posterior sample; 
# an arrow drawn from the origin to the marker would show the spin vector. 
# The outer radii of the spheres correspond to the maximum spin magnitude of 1. 
# The spins are shown in the "wave frame" defined at a reference frequency of 20 Hz. 
# The x-axis (orange) and y-axis (green) are shown as arrows near the origin; 
# the x-y plane is orthogonal to the orbital angular momentum direction. 
# The color reflects posterior probability density.
#
# |Remnant       | 
# |-----------|
# | {remnant}    | 
#
# Posterior samples for the dimensionless spin vector (chif) and the recoil kick velocity 
# (vf, units of km/s). Each purple marker indicates a posterior sample; 
# an arrow drawn from the origin to the marker would show the spin or kick vector. 
# For the spin, the outer radii of the spheres correspond to the maximum spin magnitude of 1. 
# For the kick, the outer radius of the sphere corresponds to a kick magnitude of 2500 km/s.
# The remnant spin and kick are shown in the "wave frame" defined at a 
# reference time of -100 M_det before the peak waveform amplitude,
# where M_det is the detector frame total mass.
#
# -
"""


def get_animation_cell(event_name: str) -> str:
    """Returns the animation cell for the given event"""
    remnant_html = get_video_html(event_name, "remnant")
    spin_html = get_video_html(event_name, "spin")
    if remnant_html is None or spin_html is None:
        return ""
    return ANIM_CELL.format(spin=spin_html, remnant=remnant_html)


def get_catalog_summary(events_dir: str, cache_dir: str, columns=None) -> pd.DataFrame:
    """
    Get a summary dataframe of the catalog
        events_dir: Dir with the notebooks
        cache_dir: Dir with the NRSurResults
    """
    catalog = Catalog.load(cache_dir)
    df = __load_processed_links_dataframe(catalog, events_dir)
    posterior_summary = __load_posterior_summary(catalog, columns=columns)

    # merge the posterior summary ('event') with the catalog summary ('event_name') columns
    df = df.merge(posterior_summary, on="event_id")
    df = df.sort_values(by="event_id")
    df = df.drop(columns=["event_id"])
    return df


def __check_fn(fname):
    if not os.path.isfile(fname):
        return ""
    return fname


def resize_image(orig_fname, out_fn, frac, dpi=200):
    """Resizes an image by the given fraction"""
    outdir = os.path.dirname(orig_fname)
    output_image_path = os.path.join(outdir, out_fn)
    # Open the image using Pillow
    image = Image.open(orig_fname)
    # Calculate the new size (frac of the original size)
    width, height = image.size
    new_width = int(width * frac)
    new_height = int(height * frac)
    # Resize the image
    resized_image = image.resize((new_width, new_height))
    resized_image.info['dpi'] = (dpi, dpi)
    # Save the resized image with the specified DPI
    resized_image.save(output_image_path, dpi=(dpi, dpi))
    # Save the resized image
    resized_image.save(output_image_path)


def __thumbnail(fname, event_link):
    if not os.path.isfile(fname):
        return "NA"
    thumb_image = fname.replace("waveform", "thumbnail")
    base_fn= os.path.basename(thumb_image)
    resize_image(fname, thumb_image, 0.05)
    return f"[![{base_fn}]({base_fn})]({event_link})"


def __load_processed_links_dataframe(catalog: Catalog, events_dir: str) -> pd.DataFrame:
    event_data = []
    for event in catalog.event_names:
        event_link = f"{event}.ipynb"
        event_url = LINK.format(l=event_link, txt=event)
        event_data.append(
            {
                "event_id": event,
                "Event": event_url,
                "Waveform": __thumbnail(f"{events_dir}/{event}_waveform.png", event_link),
            }
        )
    return pd.DataFrame(event_data)


def __load_posterior_summary(catalog, columns=None):
    posterior_summary = catalog.get_latex_summary()
    posterior_summary["event_id"] = posterior_summary.index
    posterior_summary.index = range(len(posterior_summary))
    if columns is None:
        columns = posterior_summary.columns.values
    else:
        columns = ["event_id"] + columns
    posterior_summary = posterior_summary[columns]
    posterior_summary = posterior_summary.rename(
        columns={p: LATEX_LABELS.get(p, p) for p in columns}
    )
    return posterior_summary


def is_file(f):
    return os.path.exists(f) or os.path.islink(f)
