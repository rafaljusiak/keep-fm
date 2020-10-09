from keep_fm.external.spotify.connectors import SpotifyConnector

TYPE_TRACK = "track"
TYPE_ALBUM = "album"
TYPE_ARTIST = "artist"
TYPE_PLAYLIST = "playlist"


class SpotifySearch:
    search_type: str

    def __init__(self):
        self._client = SpotifyConnector().get_connector()

    def search(self, query, limit=10, offset=0):
        if not self.search_type:
            raise Exception("search_type must be defined for SpotifySearch class")
        return self._client.search(
            q=query, limit=limit, offset=offset, type=self.search_type
        )


class SpotifyAlbumSearch(SpotifySearch):
    search_type = TYPE_ALBUM


class SpotifyTrackSearch(SpotifySearch):
    search_type = TYPE_TRACK


class SpotifySearchQueryBuilder:
    def __init__(self):
        self._query_params = []

    def build_query(self):
        return " ".join(self._query_params)

    def add_param(self, value, key=None):
        if key:
            self._query_params.append(f"{key}:{value}")
        else:
            self._query_params.append(value)
