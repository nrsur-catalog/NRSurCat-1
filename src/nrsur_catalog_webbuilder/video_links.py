VIDEO_IFRAME = """<video width="630" height="315" controls muted loop autoplay><source src="{ID}" type="video/mp4"> Your browser does not support the video tag.</video>"""

REMNANT_VIDEO = "https://nrsur-catalog.github.io/NRSurCat-1-animations-remnant/{event_name}_remnant.mp4"
SPIN_VIDEO = "https://nrsur-catalog.github.io/NRSurCat-1-animations-spins/{event_name}_spins.mp4"


def get_video_html(event: str, type: str) -> str:
    """Returns the link for the given event"""
    if type == "remnant":
        vid_id = REMNANT_VIDEO.format(event_name=event)
    elif type == "spin":
        vid_id = SPIN_VIDEO.format(event_name=event)
    else:
        raise ValueError(f"Unknown type: {type}")
    if vid_id is None:
        return ""
    return VIDEO_IFRAME.format(ID=vid_id)
