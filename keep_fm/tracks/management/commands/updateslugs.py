from tqdm import tqdm

from django.core.management import BaseCommand

from keep_fm.tracks.models import Track


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--overwrite", type=bool, required=False)

    def handle(self, *args, **options):
        overwrite = options.get("overwrite", False)
        tracks = (
            Track.objects.all()
            if overwrite
            else Track.objects.filter(slug__isnull=True,)
        )
        tracks = tracks.select_related("artist")

        total_count = tracks.count()
        counter = 0
        with tqdm(total=total_count) as pbar:
            for track in tqdm(tracks.iterator()):
                track.set_slug(overwrite=overwrite)
                counter += 1
                pbar.update(1)

        print(f"Finished! {counter} tracks are updated")
