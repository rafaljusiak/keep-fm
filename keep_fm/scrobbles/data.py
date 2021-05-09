import enum
from datetime import timedelta
from typing import Sequence, Union

from django.db.models import Count, QuerySet
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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
    period_type: RankingPeriodType
    period_label: str

    def __init__(
        self,
        queryset: QuerySet["Scrobble"],
        ranking_type: RankingType,
        ranking_period_type: RankingPeriodType,
    ):
        self.queryset = queryset
        self.type = ranking_type
        self.period_type = ranking_period_type
        self.period_label = ranking_period_type.label

    @classmethod
    def construct(
        cls,
        offset: int,
        limit: int,
        ranking_type: RankingType,
        ranking_period_type: RankingPeriodType = RankingPeriodType.ALL_TIME,
        user_ids: Sequence[Union[int, str]] = None,
        scrobbles: QuerySet[Scrobble] = None,
        descending: bool = False,
    ) -> "Ranking":
        """Creates ranking of tracks for given parameters"""
        # Only one of user_ids/scrobbles must be provided
        assert bool(user_ids) ^ (scrobbles is not None)

        # Get scrobbles associated only to chosen listeners
        if scrobbles is None:
            scrobbles = Scrobble.objects.filter(user_id__in=user_ids)

        # Get scrobbles only from specified period
        date_from, date_to = ranking_period_type.date_from, ranking_period_type.date_to
        if date_from:
            scrobbles = scrobbles.filter(scrobble_date__date__gte=date_from)
        if date_to:
            scrobbles = scrobbles.filter(scrobble_date__date__lte=date_to)

        # Select related
        scrobbles = scrobbles.select_related("track", "track__artist")

        # Handle specific type of ranking
        if ranking_type == RankingType.TRACK:
            scrobbles = scrobbles.values(
                "track_id", "track__name", "track__artist__name"
            ).annotate(count=Count("track_id"))
        elif ranking_type == RankingType.ARTIST:
            scrobbles = scrobbles.values("track__artist__name").annotate(
                count=Count("track__artist__name"),
            )

        scrobbles = scrobbles.order_by("count" if descending else "-count")
        scrobbles = scrobbles[offset : offset + limit]

        ranking = cls(
            queryset=scrobbles,
            ranking_type=ranking_type,
            ranking_period_type=ranking_period_type,
        )
        return ranking
