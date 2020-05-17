from django.db.models import Count
from django.views import generic

from keep_fm.common.forms import CombinedRankingForm
from keep_fm.scrobbles.models import Scrobble


class DashboardView(generic.TemplateView):
    template_name = "dashboard/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        scrobbles_qs = Scrobble.objects.filter(user=user)
        context["total_scrobbles"] = scrobbles_qs.count()

        last_scrobbles = scrobbles_qs.select_related("track", "track__artist").order_by(
            "-scrobble_date"
        )[:30]
        context["last_scrobbles"] = last_scrobbles

        top_tracks = (
            scrobbles_qs.values("track_id", "track__name", "track__artist__name")
            .annotate(count=Count("track_id"))
            .order_by("-count")[:20]
        )
        context["top_tracks"] = top_tracks

        top_artists = (
            scrobbles_qs.values("track__artist__name",)
            .annotate(count=Count("track__artist__name"),)
            .order_by("-count")[:20]
        )
        context["top_artists"] = top_artists

        return context


class CombinedRankingView(generic.FormView):
    form_class = CombinedRankingForm
    template_name = "rankings/combined.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.GET.get("user_id")
        if user_id:
            scrobbles_qs = Scrobble.objects.filter(
                user__in=[self.request.user.id, user_id]
            )
            context["total_scrobbles"] = scrobbles_qs.count()

            last_scrobbles = scrobbles_qs.select_related(
                "track", "track__artist"
            ).order_by("-scrobble_date")[:30]
            context["last_scrobbles"] = last_scrobbles

            top_tracks = (
                scrobbles_qs.values("track_id", "track__name", "track__artist__name")
                .annotate(count=Count("track_id"))
                .order_by("-count")[:20]
            )
            context["top_tracks"] = top_tracks

            top_artists = (
                scrobbles_qs.values("track__artist__name",)
                .annotate(count=Count("track__artist__name"),)
                .order_by("-count")[:20]
            )
            context["top_artists"] = top_artists
        return context

    def get_success_url(self):
        user_id = self.request.POST.get("user")
        if user_id:
            return self.request.path + f"?user_id={user_id}"
        return self.request.get_full_path()
