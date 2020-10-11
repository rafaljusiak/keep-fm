from datetime import datetime
from typing import Tuple

from keep_fm.scrobbles.models import Scrobble

from keep_fm.tracks.models import Artist, Track
from keep_fm.tracks.slugs import slugify_track


class ScrobbleProcessor:
    """ It holds logic of processing and saving scrobbles data in the database """

    @staticmethod
    def process_and_save(
        user_id: int, artist_name: str, track_name: str, timestamp: datetime
    ) -> Tuple[Scrobble, bool]:
        """
        All Scrobble objects have to be created with this method to keep them consistent
        in the database.

        Gets or creates Artist and Track records from the local database that are matching
        the given arguments, and then gets or creates a Scrobble object.
        """
        artist, _ = Artist.objects.get_or_create(name=artist_name)

        # Get a track slug to find if track already exists in the database
        # and to not create any duplicate.
        track_slug = slugify_track(artist_name, track_name)
        track = Track.objects.filter(slug=track_slug).first()

        # If track doesn't exists - create a new one and set slug for it
        if not track:
            track = Track.objects.create(name=track_name, artist=artist)
            track.set_slug()

        # Create Scrobble object and associate it with a proper Track and User
        return Scrobble.objects.get_or_create(
            track=track, user_id=user_id, scrobble_date=timestamp,
        )
