from typing import Any

import pytest

from keep_fm.tracks.models import Artist, Track

TEST_ARTIST_NAME = "The Smiths"
TEST_TRACK_NAME = "There Is A Light That Never Goes Out"


@pytest.fixture
def artist(db: Any) -> Artist:
    return Artist.objects.create(name=TEST_ARTIST_NAME)


@pytest.fixture
def track(artist: Artist) -> Track:
    track = Track(
        artist=artist,
        name=TEST_TRACK_NAME,
    )
    track.set_slug(overwrite=True)
    return track
