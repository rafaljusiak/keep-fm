from keep_fm.scrobbles.models import Scrobble

from keep_fm.tracks.models import Artist, Track
from keep_fm.tracks.slugs import slugify_track


class ScrobbleProcessor:
    @staticmethod
    def process_and_save(user_id, artist_name, track_name, timestamp):
        artist, _ = Artist.objects.get_or_create(name=artist_name)
        track_slug = slugify_track(artist_name, track_name)
        track = Track.objects.filter(slug=track_slug).first()
        if not track:
            track = Track.objects.create(name=track_name, artist=artist)
        return Scrobble.objects.get_or_create(
            track=track, user_id=user_id, scrobble_date=timestamp,
        )
