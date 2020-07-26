from django.utils.text import slugify


def slugify_track(artist_name, track_name):
    full_name = f"{artist_name} {track_name}"
    return slugify(full_name, allow_unicode=True)
