from keep_fm.scrobbles.models import Scrobble
from tqdm import tqdm

from django.core.management import BaseCommand

from keep_fm.tracks.models import Track


class Command(BaseCommand):
    def handle(self, *args, **options):
        tracks = Track.objects.all()
        total_count = tracks.count()

        counter = 0
        removed_tracks = []
        with tqdm(total=total_count) as pbar:
            for track in tqdm(tracks.iterator()):
                pbar.update(1)
                if track.id in removed_tracks:
                    continue
                similar_tracks = (
                    Track.objects.filter(slug=track.slug)
                    .exclude(id=track.id)
                    .values_list("id", flat=True)
                )
                if similar_tracks.exists():
                    scrobbles = Scrobble.objects.filter(track_id__in=similar_tracks)
                    removed_tracks += list(similar_tracks)
                    for scrobble in scrobbles:
                        scrobble.track_id = track.id
                        try:
                            scrobble.save()
                        except Exception as e:
                            print("error:", track.id, track.name, str(e))
                    Track.objects.filter(id__in=similar_tracks).delete()
                    counter += 1
        print(f"Finished! {counter}/{total_count} tracks were merged")
