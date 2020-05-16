REDUNDANT_ENDINGS = (
    "remaster",
    "live",
    "edit",
    "version",
    "mono",
    "stereo",
)


def clean_track_name(track_name):
    if "-" in track_name:
        lower_parsed = track_name.lower().split("-")
        if any([ending in lower_parsed[-1] for ending in REDUNDANT_ENDINGS]):
            cleaned_track_name = track_name.rsplit("-", 1)[0]
            if cleaned_track_name[-1] == " ":
                return cleaned_track_name[:-1]
            return cleaned_track_name
    return track_name
