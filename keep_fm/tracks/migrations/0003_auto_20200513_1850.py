# Generated by Django 3.0.6 on 2020-05-13 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tracks", "0002_auto_20200513_1845"),
    ]

    operations = [
        migrations.AlterField(
            model_name="track",
            name="artist",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tracks",
                to="tracks.Artist",
                verbose_name="Artist",
            ),
        ),
    ]