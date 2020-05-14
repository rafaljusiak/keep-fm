# Generated by Django 3.0.6 on 2020-05-13 19:33

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tracks", "0003_auto_20200513_1850"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("scrobbles", "0002_auto_20200513_1854"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="scrobble", unique_together={("user", "track", "scrobble_date")},
        ),
    ]