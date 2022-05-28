from typing import List, Optional, Type, Union, cast

from django import forms
from django.db.models import QuerySet
from django.views import generic

from keep_fm.scrobbles.forms import CombinedRankingForm
from keep_fm.scrobbles.data import Ranking, RankingType, RankingFilters
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
            ranking_type=RankingType.TRACK,
            scrobbles=scrobbles_qs,
        )
        context["top_tracks"] = top_tracks

        top_artists = Ranking.construct(
            ranking_type=RankingType.ARTIST,
            scrobbles=scrobbles_qs,
        )
        context["top_artists"] = top_artists

        return context


class RankingView(generic.TemplateView):
    template_name = "rankings/basic_ranking.html"
    ranking_type: RankingType
    limit: int = 300

    @property
    def artist_ids(self) -> Optional[List[Union[str, int]]]:
        return None

    @property
    def user_ids(self) -> Optional[List[Union[str, int]]]:
        return None

    @property
    def scrobbles(self) -> Optional[QuerySet[Scrobble]]:
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ranking_filters = RankingFilters.from_request(request=self.request)
        ranking = Ranking.construct(
            offset=0,
            limit=self.limit,
            ranking_filters=ranking_filters,
            ranking_type=self.ranking_type,
            scrobbles=self.scrobbles,
            artist_ids=self.artist_ids,
            user_ids=self.user_ids,
        )

        context["ranking"] = ranking
        context["ranking_filters"] = ranking_filters
        return context


class PersonalRankingView(RankingView):
    @property
    def user_ids(self) -> List[Union[str, int]]:
        user_id = cast(int, self.request.user.id)
        return [user_id]


class GlobalRankingView(RankingView):
    @property
    def scrobbles(self):
        return Scrobble.objects.all()


class ArtistsRankingView(PersonalRankingView):
    """Ranking of user's 300 top listened artists"""

    ranking_type = RankingType.ARTIST


class TracksRankingView(PersonalRankingView):
    """Ranking of user's 300 top listened tracks"""

    ranking_type = RankingType.TRACK


class CombinedRankingView(generic.FormView):
    """
    Mixin used for combined ranking views. It renders a CombinedRankingForm
    and passes a selected User id in a query string.
    """

    form_class: Type[forms.Form] = CombinedRankingForm
    ranking_type: RankingType
    limit: int = 300
    template_name = "rankings/combined_ranking.html"

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
                limit=self.limit,
                ranking_type=self.ranking_type,
                user_ids=[self.request.user.id, user_id],
            )
            context["ranking"] = top_tracks
        return context


class CombinedTracksRankingView(CombinedRankingView):
    """Ranking of logged in and selected Users 300 top listened tracks"""

    form_class = CombinedRankingForm
    ranking_type = RankingType.TRACK


class CombinedArtistsRankingView(CombinedRankingView):
    """Ranking of logged in and selected Users 300 top listened artists"""

    form_class = CombinedRankingForm
    ranking_type = RankingType.ARTIST


class ArtistLookupMixin(generic.TemplateView):
    @property
    def artist_ids(self) -> Optional[List[Union[str, int]]]:
        return [cast(int, self.kwargs["artist_id"])]


class ArtistGlobalRankingView(ArtistLookupMixin, GlobalRankingView):
    ranking_type = RankingType.TRACK


class ArtistPersonalRankingView(ArtistLookupMixin, PersonalRankingView):
    ranking_type = RankingType.TRACK
