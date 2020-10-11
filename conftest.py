import pytest
from django.core.handlers.wsgi import WSGIRequest
from django.test import RequestFactory

from keep_fm.users.models import User


@pytest.fixture
def get_request(test_user: User) -> WSGIRequest:
    request = RequestFactory().get("/")
    request.user = test_user
    request.session = {}
    return request


@pytest.fixture
def post_request(test_user: User) -> WSGIRequest:
    request = RequestFactory().post("/")
    request.user = test_user
    request.session = {}
    return request


@pytest.fixture
def test_user(db) -> User:
    user = User.objects.create_user(username="testuser",)
    user.lastfm_username = "!@#$%^&*()"
    user.save()
    return user
