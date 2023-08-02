VIDEO_IFRAME = """<iframe width="560" height="315" src="https://www.youtube.com/embed/{ID}?loop=1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>"""


REMNANT_VIDEO = dict(
    GW150914_095045="https://youtu.be/mkxggi9SM8M",
    DEFAULT="https://youtu.be/mkxggi9SM8M", # None
)

SPIN_VIDEO = dict(
    GW150914_095045="https://youtu.be/msRN00Spjbs",
    DEFAULT="https://youtu.be/msRN00Spjbs", # None
)


def __extract_id(l) -> str:
    """extract the id after last / from a link"""
    return l.split("/")[-1]


def get_video_html(event: str, type: str) -> str:
    """Returns the link for the given event"""
    if type == "remnant":
        link = REMNANT_VIDEO.get(event, REMNANT_VIDEO["DEFAULT"])
    elif type == "spin":
        link = SPIN_VIDEO.get(event, SPIN_VIDEO["DEFAULT"])
    else:
        raise ValueError(f"Unknown type: {type}")
    if link is None:
        return ""
    id = __extract_id(link)
    return VIDEO_IFRAME.format(ID=id)
