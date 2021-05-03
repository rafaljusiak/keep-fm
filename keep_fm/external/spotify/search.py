from typing import Dict, Any, List, Optional

import spotipy

from keep_fm.external.spotify.connectors import SpotifyConnector

TYPE_TRACK = "track"
TYPE_ALBUM = "album"
TYPE_ARTIST = "artist"
TYPE_PLAYLIST = "playlist"


class SpotifySearch:
    """
    SpotifySearch is a generic class used to make an API call to Spotify API
    to load data about tracks, albums, artists or playlists.
    """

    search_type: str

    def __init__(self):
        self._client: spotipy.Spotify = SpotifyConnector().get_connector()

    def search(self, query: str, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        if not self.search_type:
            raise Exception("search_type must be defined for SpotifySearch class")
        return self._client.search(
            q=query, limit=limit, offset=offset, type=self.search_type
        )


class SpotifyAlbumSearch(SpotifySearch):
    """Specific implementation of SpotifySearch that loads data about albums."""

    search_type = TYPE_ALBUM


class SpotifyTrackSearch(SpotifySearch):
    """Specific implementation of SpotifySearch that loads data about tracks."""

    search_type = TYPE_TRACK


class SpotifySearchQueryBuilder:
    """SpotifySearchQueryBuilder creates a valid query form a given params"""

    def __init__(self):
        self._query_params: List[str] = []

    def build_query(self) -> str:
        return " ".join(self._query_params)

    def add_param(self, value: str, key: Optional[str] = None) -> None:
        if key:
            self._query_params.append(f"{key}:{value}")
        else:
            self._query_params.append(value)
