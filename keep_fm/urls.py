from typing import cast, List

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required
from django.urls import path, URLPattern
from keep_fm.common import views as common
from keep_fm.users import views as users


urls = [
    path("admin/", admin.site.urls),
    path("login", users.LoginUserView.as_view(), name="login"),
    path("logout", logout_then_login, name="logout"),
    path("", login_required(common.DashboardView.as_view()), name="dashboard"),
    path(
        "tracks",
        login_required(common.TracksRankingView.as_view()),
        name="top-tracks",
    ),
    path(
        "artists",
        login_required(common.ArtistsRankingView.as_view()),
        name="top-artists",
    ),
    path(
        "combined",
        login_required(common.CombinedRankingView.as_view()),
        name="top-combined",
    ),
    path(
        "combined/tracks",
        login_required(common.CombinedTracksRankingView.as_view()),
        name="top-combined-tracks",
    ),
    path(
        "combined/artists",
        login_required(common.CombinedArtistsRankingView.as_view()),
        name="top-combined-artists",
    ),
]


urlpatterns = cast(List[URLPattern], urls) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
