import pytest

from keep_fm.conftest import TEST_TRACK_NAME, TEST_ARTIST_NAME
from keep_fm.tracks.models import Artist, Track


@pytest.mark.parametrize(
    "artist_name,should_create",
    [
        pytest.param("Madonna", True),
        pytest.param("The Beatles", True),
        pytest.param("Nick Cave & The Bad Seeds", True),
        pytest.param(TEST_ARTIST_NAME, False),
    ],
)
def test_artist_process_and_save(
    artist: Artist,
    artist_name: str,
    should_create: bool,
) -> None:
    artist, created = Artist.process_and_save(artist_name)
    assert artist.name == artist_name
    assert created == should_create


@pytest.mark.parametrize(
    "artist_name,track_name,should_create",
    [
        pytest.param("Madonna", "Holiday", True),
        pytest.param("The Beatles", "Ticket to Ride", True),
        pytest.param("Nick Cave & The Bad Seeds", "Tupelo", True),
        pytest.param(TEST_ARTIST_NAME, "Ask", True),
        pytest.param(TEST_ARTIST_NAME, TEST_TRACK_NAME, False),
    ],
)
def test_track_process_and_save(
    track: Track,
    artist_name: str,
    track_name: str,
    should_create: bool,
):
    track, created = Track.process_and_save(
        artist_name=artist_name,
        track_name=track_name,
    )
    assert track.artist.name == artist_name
    assert track.name == track_name
    assert created == should_create
