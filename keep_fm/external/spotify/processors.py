from typing import Dict, Any, Union, Optional


def map_track_data(track_data: Dict[str, Any]) -> Dict[str, Union[str, int, float]]:
    """
    Maps track data from Spotify API (like a popularity of a track
    and URL to tracks preview) and returns a new dictionary
    """
    flat_keys = ("popularity", "preview_url")
    return {key: track_data[key] for key in flat_keys}


def map_track_features_data(
    track_audio_features_data: Dict[str, Any]
) -> Dict[str, Union[str, int, float]]:
    """
    Maps track features data from Spotify API (like a duration or
    liveness of a song) and returns a new dictionary
    """
    flat_keys = (
        "duration_ms",
        "danceability",
        "energy",
        "loudness",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
    )
    duration = track_audio_features_data.get("duration_ms", 0) / 1000.0
    duration_str = f"{int(duration / 60)}:{int(duration % 60)}"
    results = {"duration": duration, "duration_str": duration_str}
    results.update({key: track_audio_features_data[key] for key in flat_keys})
    return results


def map_album_data(track_album_data: Dict[str, Any]) -> Dict[str, Optional[str]]:
    """ Maps album track data from Spotify API """
    name = track_album_data.get("name")
    return {
        "name": name,
    }
