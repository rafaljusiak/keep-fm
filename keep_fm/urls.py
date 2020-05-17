from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required
from django.urls import path
from keep_fm.common import views as common
from keep_fm.users import views as users


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login", users.LoginUserView.as_view(), name="login"),
    path("logout", logout_then_login, name="logout"),
    path("", login_required(common.DashboardView.as_view()), name="dashboard"),
    path(
        "combined",
        login_required(common.CombinedRankingView.as_view()),
        name="combined",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
