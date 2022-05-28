import enum
from dataclasses import dataclass
from datetime import timedelta, date
from typing import Sequence, Union, List, Dict, Optional
from urllib.parse import urlencode

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count, QuerySet
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from keep_fm.common.parse import get_date_or_none, get_str_or_none, get_int_or_none
from keep_fm.scrobbles.models import Scrobble


class RankingType(str, enum.Enum):
    # Ranking of top artists
    ARTIST = "artist"
    # Ranking of top tracks
    TRACK = "track"


class RankingPeriodType(enum.Enum):
    ALL_TIME = (_("All time"), None, None)
    TODAY = (_("Today"), timedelta(days=0), None)
    LAST_DAY = (_("Last day"), timedelta(days=-1), timedelta(days=-1))
    LAST_7_DAYS = (_("Last 7 days"), timedelta(days=-7), None)
    LAST_30_DAYS = (_("Last 30 days"), timedelta(days=-30), None)
    LAST_90_DAYS = (_("Last 90 days"), timedelta(days=-90), None)
    LAST_180_DAYS = (_("Last 180 days"), timedelta(days=-180), None)
    LAST_360_DAYS = (_("Last 360 days"), timedelta(days=-360), None)

    def __init__(
        self, label: str, period_from: timedelta, period_to: timedelta
    ) -> None:
        self.label = label

        today = timezone.now().date()
        self.date_from = today + period_from if period_from else None
        self.date_to = today + period_to if period_to else None


class Ranking:
    queryset: QuerySet["Scrobble"]
    type: RankingType
    label: str

    def __init__(
        self,
        queryset: QuerySet["Scrobble"],
        ranking_type: RankingType,
        label: str,
    ):
        self.queryset = queryset
        self.type = ranking_type
        self.label = label

    @classmethod
    def construct(
        cls,
        ranking_type: RankingType,
        offset: int = 0,
        limit: int = 30,
        default_ranking_period_type: RankingPeriodType = RankingPeriodType.ALL_TIME,
        descending: bool = False,
        ranking_filters: "RankingFilters" = None,
        scrobbles: QuerySet[Scrobble] = None,
        artist_ids: Sequence[Union[int, str]] = None,
        user_ids: Sequence[Union[int, str]] = None,
    ) -> "Ranking":
        """Creates ranking of tracks for given parameters"""
        # Only one of user_ids/scrobbles must be provided
        assert bool(user_ids) ^ (scrobbles is not None)

        # Use empty RankingFilters if none was passed
        if ranking_filters is None:
            ranking_filters = RankingFilters.empty()

        # Get scrobbles associated only to chosen listeners
        if scrobbles is None:
            scrobbles = Scrobble.objects.filter(user_id__in=user_ids)

        # Filter by artist id
        if artist_ids is not None:
            scrobbles = scrobbles.filter(track__artist_id__in=artist_ids)

        # Get scrobbles only from specified period
        date_from, date_to = ranking_filters.date_from, ranking_filters.date_to
        if not date_from:
            date_from = default_ranking_period_type.date_from
        if not date_to:
            date_to = default_ranking_period_type.date_to

        if date_from:
            scrobbles = scrobbles.filter(scrobble_date__date__gte=date_from)
        if date_to:
            scrobbles = scrobbles.filter(scrobble_date__date__lte=date_to)

        # Select related
        scrobbles = scrobbles.select_related("track", "track__artist")

        # Handle specific type of ranking
        if ranking_type == RankingType.TRACK:
            scrobbles = scrobbles.values(
                "track_id",
                "track__name",
                "track__artist__name",
                "track__artist_id",
            ).annotate(count=Count("track_id"))
        elif ranking_type == RankingType.ARTIST:
            scrobbles = scrobbles.values(
                "track__artist__name",
                "track__artist_id",
            ).annotate(
                count=Count("track__artist__name"),
            )
        else:
            raise NotImplementedError

        scrobbles = scrobbles.order_by("count" if descending else "-count")
        scrobbles = scrobbles[offset : offset + limit]

        ranking = cls(
            queryset=scrobbles,
            ranking_type=ranking_type,
            label=ranking_filters.label or default_ranking_period_type.label,
        )
        return ranking


@dataclass
class HTMLRankingFilter:
    label: str
    href: str


@dataclass
class RankingFilters:
    html_period_filters: List[HTMLRankingFilter]
    query_dict: Dict[str, Union[bool, int, str]]

    date_from: Optional[date] = None
    date_to: Optional[date] = None
    label: Optional[str] = None

    artist_id: Optional[int] = None

    @classmethod
    def empty(cls):
        """Returns empty RankingFilter object"""
        return cls(
            html_period_filters=list(),
            query_dict=dict(),
        )

    @classmethod
    def from_request(cls, request: WSGIRequest) -> "RankingFilters":
        """
        Extracts selected filters from the query string.
        Additionally it prepares a list of HTMLRankingFilter objects that can be used in
        HTML template to render filters to select.
        """
        query_dict = dict(request.GET)

        # Extract filters
        date_from = get_date_or_none(query_dict.get("date_from"))
        date_to = get_date_or_none(query_dict.get("date_to"))
        label = get_str_or_none(query_dict.get("label"))
        artist_id = get_int_or_none(query_dict.get("artist_id"))

        # Prepare filter urls
        html_period_filters = []
        for ranking_period in RankingPeriodType:
            query_params = query_dict.copy()

            query_params["date_from"] = ranking_period.date_from or ""
            query_params["date_to"] = ranking_period.date_to or ""
            query_params["label"] = ranking_period.label or ""

            query_string = urlencode(query_params)
            href = f"{request.path}?{query_string}"
            html_period_filters.append(
                HTMLRankingFilter(
                    label=ranking_period.label,
                    href=href,
                )
            )

        return cls(
            html_period_filters=html_period_filters,
            query_dict=query_dict,
            date_from=date_from,
            date_to=date_to,
            label=label,
            artist_id=artist_id,
        )
