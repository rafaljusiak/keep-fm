from typing import Optional, Dict, Any

from keep_fm.external.spotify.connectors import SpotifyConnector

from keep_fm.external.spotify.search import (
    SpotifySearchQueryBuilder,
    SpotifyTrackSearch,
)


def get_tracks_search_data(
    track_name: str, artist_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Shortcut function that uses SpotifyTrackSearch to retrieve tracks data
    basing on a track name and optionally an artist name. It can return
    multiple items.
    """
    builder = SpotifySearchQueryBuilder()
    builder.add_param(track_name)
    if artist_name:
        builder.add_param(artist_name, "artist")
    query = builder.build_query()
    search = SpotifyTrackSearch()
    results = search.search(query)
    return results["tracks"]


def get_track_data(
    track_name: str, artist_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Shortcut function that uses SpotifyTrackSearch to retrieve a certain track
    data basing on a track name and optionally an artist name. It returns only
    a single item or an empty dictionary.
    """
    data = get_tracks_search_data(track_name, artist_name)
    for item in data["items"]:
        if artist_name and artist_name not in item["artists"][0]["name"]:
            continue
        if track_name in item["name"]:
            return item
    return {}


def get_track_uri(track_name: str, artist_name: Optional[str] = None) -> Optional[str]:
    """
    Shortcut function that uses SpotifyTrackSearch to retrieve a track URI
    basing on a track name and optionally an artist name.
    """
    data = get_track_data(track_name, artist_name)
    return data["uri"] if data else None


def get_track_audio_analysis(track_spotify_uri: str) -> Dict[str, Any]:
    """
    Shortcut function that retrieves a Spotify audio analysis for a track
    specified by its Spotify URI.
    """
    client = SpotifyConnector().get_connector()
    return client.audio_analysis(track_spotify_uri)


def get_track_audio_features(track_spotify_uri: str) -> Dict[str, Any]:
    """
    Shortcut function that retrieves a Spotify audio features for a track
    specified by its Spotify URI.
    """
    client = SpotifyConnector().get_connector()
    return client.audio_features([track_spotify_uri])[0]
