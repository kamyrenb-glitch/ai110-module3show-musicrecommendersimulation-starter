"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

# Named test profiles. "Adversarial Classical Nostalgic" leaves out likes_acoustic
# on purpose so score_song uses its neutral 0.5 acoustic fallback.
PROFILES = {
    "High-Energy Happy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    "Chill Acoustic Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.3,
        "likes_acoustic": True,
    },
    "Romantic R&B": {
        "genre": "r&b",
        "mood": "romantic",
        "energy": 0.6,
        "likes_acoustic": False,
    },
    "Adversarial Classical Nostalgic": {
        "genre": "classical",
        "mood": "nostalgic",
        "energy": 0.95,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\n" + "=" * 60)
        print(f"Profile: {name}")
        print(f"User profile: {user_prefs}")
        print("=" * 60)
        print("\nTop recommendations:\n")
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} by {song['artist']} - Score: {score:.2f}")
            # Explanation is joined with "; " in recommend_songs; split only for display
            for reason in explanation.split("; "):
                print(f"   - {reason}")
            print()


if __name__ == "__main__":
    main()
