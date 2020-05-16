def map_track_data(track_data):
    flat_keys = ("popularity", "preview_url")
    return {key: track_data[key] for key in flat_keys}


def map_track_features_data(track_audio_features_data):
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
    duration = track_audio_features_data.get("duration_ms") / 1000.0
    duration_str = f"{int(duration / 60)}:{int(duration % 60)}"
    results = {"duration": duration, "duration_str": duration_str}
    results.update({key: track_audio_features_data[key] for key in flat_keys})
    return results


def map_album_data(track_album_data):
    name = track_album_data.get("name")
    return {
        "name": name,
    }
