from typing import Any, cast

import pytest
from django.contrib.sessions.backends.base import SessionBase
from django.core.handlers.wsgi import WSGIRequest
from django.test import RequestFactory

from keep_fm.tracks.models import Artist, Track
from keep_fm.users.models import User


@pytest.fixture
def get_request(test_user: User) -> WSGIRequest:
    request = RequestFactory().get("/")
    request.user = test_user
    request.session = cast(SessionBase, {})
    return request


@pytest.fixture
def post_request(test_user: User) -> WSGIRequest:
    request = RequestFactory().post("/")
    request.user = test_user
    request.session = cast(SessionBase, {})
    return request


TEST_ARTIST_NAME = "The Smiths"
TEST_TRACK_NAME = "There Is A Light That Never Goes Out"


@pytest.fixture
def test_user(db: Any) -> User:
    user = User.objects.create_user(
        username="testuser",
    )
    user.lastfm_username = "!@#$%^&*()"
    user.save()
    return user


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
