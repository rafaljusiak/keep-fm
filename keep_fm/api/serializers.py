from keep_fm.users.models import User

from keep_fm.scrobbles.models import Scrobble

from keep_fm.tracks.models import Artist, Track
from rest_framework import serializers


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = (
            "artist",
            "name",
        )


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ("name",)


class ScrobbleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scrobble
        fields = ("track",)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "lastfm_username",
            "scrobbles",
        )
