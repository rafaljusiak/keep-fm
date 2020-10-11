from typing import Type

import pytest
from django.core.handlers.wsgi import WSGIRequest
from django.views import View

from keep_fm.common import views


@pytest.mark.parametrize(
    "view_class",
    [
        pytest.param(views.DashboardView),
        pytest.param(views.ArtistsRankingView),
        pytest.param(views.TracksRankingView),
        pytest.param(views.CombinedRankingView),
        pytest.param(views.CombinedArtistsRankingView),
        pytest.param(views.CombinedTracksRankingView),
    ],
)
def test_200(view_class: Type[View], get_request: WSGIRequest):
    view = view_class()
    view.request = get_request
    response = view.dispatch(view.request)
    assert response.status_code == 200
