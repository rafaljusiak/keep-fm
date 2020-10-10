from django.db.models import QuerySet, Count


class ScrobblesQueryset(QuerySet):
    def top_tracks(self, limit: int = 30) -> QuerySet:
        return (
            self.values("track_id", "track__name", "track__artist__name")
            .annotate(count=Count("track_id"))
            .order_by("-count")[:limit]
        )

    def top_artists(self, limit: int = 30) -> QuerySet:
        return (
            self.values("track__artist__name",)
            .annotate(count=Count("track__artist__name"),)
            .order_by("-count")[:limit]
        )
