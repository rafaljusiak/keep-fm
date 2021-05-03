import spotipy


class SpotifyConnector:
    """Adapter for a Spotify connector"""

    def get_connector(self) -> spotipy.Spotify:
        return spotipy.Spotify(
            client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials(),
        )
