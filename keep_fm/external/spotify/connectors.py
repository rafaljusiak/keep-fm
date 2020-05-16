import spotipy


class SpotifyConnector:
    def get_connector(self):
        return spotipy.Spotify(
            client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials(),
        )
