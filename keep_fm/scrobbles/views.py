from typing import Type

from django import forms
from django.views import generic

from keep_fm.scrobbles.forms import CombinedRankingForm
from keep_fm.scrobbles.data import Ranking, RankingType, RankingPeriodType
from keep_fm.scrobbles.models import Scrobble


class DashboardView(generic.TemplateView):
    """Main dashboard view - entry point for a user after login."""

    template_name = "dashboard/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        scrobbles_qs = Scrobble.objects.filter(user=user)
        context["total_scrobbles"] = scrobbles_qs.count()

        last_scrobbles = scrobbles_qs.select_related("track", "track__artist").order_by(
            "-scrobble_date"
        )[:30]
        context["last_scrobbles"] = last_scrobbles

        top_tracks = Ranking.construct(
            offset=0,
            limit=30,
            ranking_type=RankingType.TRACK,
            ranking_period_type=RankingPeriodType.ALL_TIME,
            scrobbles=scrobbles_qs,
        )
        context["top_tracks"] = top_tracks

        top_artists = Ranking.construct(
            offset=0,
            limit=30,
            ranking_type=RankingType.ARTIST,
            ranking_period_type=RankingPeriodType.ALL_TIME,
            scrobbles=scrobbles_qs,
        )
        context["top_artists"] = top_artists

        return context


class RankingView(generic.TemplateView):
    template_name = "rankings/basic_ranking.html"
    ranking_type: RankingType

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ranking"] = Ranking.construct(
            offset=0,
            limit=30,
            ranking_type=self.ranking_type,
            ranking_period_type=RankingPeriodType.ALL_TIME,
            user_ids=[self.request.user.id],
        )
        return context


class ArtistsRankingView(RankingView):
    """Ranking of user's 300 top listened artists"""

    ranking_type = RankingType.ARTIST


class TracksRankingView(RankingView):
    """Ranking of user's 300 top listened tracks"""

    ranking_type = RankingType.TRACK


class CombinedRankingView(generic.FormView):
    """
    Mixin used for combined ranking views. It renders a CombinedRankingForm
    and passes a selected User id in a query string.
    """

    form_class: Type[forms.Form] = CombinedRankingForm
    ranking_type: RankingType

    def get_success_url(self):
        user_id = self.request.POST.get("user")
        if user_id:
            return self.request.path + f"?user_id={user_id}"
        return self.request.get_full_path()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.GET.get("user_id")
        if user_id:
            top_tracks = Ranking.construct(
                offset=0,
                limit=30,
                ranking_type=self.ranking_type,
                ranking_period_type=RankingPeriodType.ALL_TIME,
                user_ids=[self.request.user.id, user_id],
            )
            context["ranking"] = top_tracks
        return context


class CombinedTracksRankingView(CombinedRankingView):
    """Ranking of logged in and selected Users 300 top listened tracks"""

    form_class = CombinedRankingForm
    template_name = "rankings/combined_ranking.html"
    ranking_type = RankingType.TRACK


class CombinedArtistsRankingView(CombinedRankingView):
    """Ranking of logged in and selected Users 300 top listened artists"""

    form_class = CombinedRankingForm
    template_name = "rankings/combined_ranking.html"
    ranking_type = RankingType.ARTIST
