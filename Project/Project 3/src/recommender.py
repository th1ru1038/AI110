import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

GENRE_WEIGHT = 15
MOOD_WEIGHT = 25
ENERGY_WEIGHT = 50
ACOUSTIC_WEIGHT = 20
ACOUSTIC_THRESHOLD = 0.5


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


def _score(
    genre: str,
    mood: str,
    energy: float,
    acousticness: float,
    favorite_genre: str,
    favorite_mood: str,
    target_energy: float,
    likes_acoustic: bool,
) -> Tuple[float, List[str]]:
    """
    Shared scoring logic used by both the OOP and functional recommenders.
    Applies the finalized Algorithm Recipe (see README):
        genre 30 / mood 25 / energy 25 / acoustic 20
    """
    score = 0.0
    reasons: List[str] = []

    if genre == favorite_genre:
        score += GENRE_WEIGHT
        reasons.append(f"matches your favorite genre ({genre})")

    if mood == favorite_mood:
        score += MOOD_WEIGHT
        reasons.append(f"matches your favorite mood ({mood})")

    energy_closeness = 1 - abs(energy - target_energy)
    score += energy_closeness * ENERGY_WEIGHT
    if energy_closeness > 0.8:
        reasons.append(f"energy ({energy}) is very close to your target ({target_energy})")

    is_acoustic = acousticness > ACOUSTIC_THRESHOLD
    if is_acoustic == likes_acoustic:
        score += ACOUSTIC_WEIGHT
        if likes_acoustic:
            reasons.append("has the acoustic feel you prefer")
        else:
            reasons.append("has the non-acoustic feel you prefer")

    if not reasons:
        reasons.append("no strong matches, included as a low-confidence option")

    return score, reasons


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [
            (song, self._score_song(user, song))
            for song in self.songs
        ]
        scored.sort(key=lambda pair: pair[1][0], reverse=True)
        return [song for song, _ in scored[:k]]

    def _score_song(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        return _score(
            song.genre,
            song.mood,
            song.energy,
            song.acousticness,
            user.favorite_genre,
            user.favorite_mood,
            user.target_energy,
            user.likes_acoustic,
        )

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = self._score_song(user, song)
        return "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    return _score(
        song["genre"],
        song["mood"],
        song["energy"],
        song["acousticness"],
        user_prefs.get("genre"),
        user_prefs.get("mood"),
        user_prefs.get("energy", 0.5),
        user_prefs.get("likes_acoustic", False),
    )


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
