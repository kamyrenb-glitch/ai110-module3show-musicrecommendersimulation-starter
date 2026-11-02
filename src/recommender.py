from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load song dictionaries from a CSV file and convert numeric fields to int or float."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            row["tempo_bpm"] = int(row["tempo_bpm"])
            for key in ("energy", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return (score, reasons)."""
    score = 0.0
    reasons = []

    # Exact match on genre (1.0) and mood (1.5), ignoring case and surrounding spaces
    for key, points in (("genre", 1.0), ("mood", 1.5)):
        wanted = user_prefs[key].strip().lower()
        if song[key].strip().lower() == wanted:
            score += points
            reasons.append(f"{key} match: {wanted} (+{points:.2f})")
        else:
            reasons.append(f"{key} does not match {wanted} (+0.00)")

    # Energy closeness: full 3.0 at the target, falling to 0 at a gap of 0.5 or more
    target = user_prefs["energy"]
    energy_pts = 3.0 * max(0.0, 1 - abs(song["energy"] - target) / 0.5)
    score += energy_pts
    reasons.append(f"energy {song['energy']:.2f} vs target {target:.2f} (+{energy_pts:.2f})")

    # Acoustic preference: up to 1.0, or a neutral 0.5 when no preference is given
    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is None:
        acoustic_pts = 0.5
        reasons.append(f"no acoustic preference given (+{acoustic_pts:.2f})")
    elif likes_acoustic:
        acoustic_pts = song["acousticness"]
        reasons.append(f"acoustic preference (+{acoustic_pts:.2f})")
    else:
        acoustic_pts = 1 - song["acousticness"]
        reasons.append(f"non-acoustic preference (+{acoustic_pts:.2f})")
    score += acoustic_pts

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score, rank, and return the top k songs as (song, score, explanation) tuples."""
    if k <= 0 or not songs:
        return []

    # Score every song exactly once
    results = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        results.append((song, score, reasons))

    # Highest score first; scores within ~1e-12 count as ties, which go to the
    # smaller energy gap and then the lower id. Rounding only affects the sort key.
    target = user_prefs["energy"]
    ranked = sorted(
        results,
        key=lambda r: (
            -round(r[1], 12),
            round(abs(r[0]["energy"] - target), 12),
            r[0]["id"],
        ),
    )

    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]
