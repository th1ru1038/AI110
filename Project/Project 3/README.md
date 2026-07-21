# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify and YouTube generally combine two approaches: **content-based filtering**, which recommends items similar to what a user already likes based on the item's own attributes (tempo, genre, mood), and **collaborative filtering**, which recommends items based on what *similar users* liked, regardless of the item's attributes. 

Content-based filtering works even for brand-new items with no listening history, while collaborative filtering can surface unexpected recommendations that content attributes alone would miss. This simulation focuses entirely on the content-based side: it has no user-interaction data (plays, skips, saves), so every recommendation is built by comparing a song's own attributes against a stated user taste profile — there is no "people like you" signal here, only "songs like what you said you like."

**`Song` features used in this system:**
- `genre` — categorical, matched exactly against the user's favorite genre
- `mood` — categorical, matched exactly against the user's favorite mood
- `energy` — numerical (0–1), scored by closeness to the user's target energy rather than by raw value
- `acousticness` — numerical (0–1), used together with the user's `likes_acoustic` preference

**`UserProfile` information stored:**
- `favorite_genre` — the genre the user prefers
- `favorite_mood` — the mood the user prefers
- `target_energy` — the energy level the user prefers, used as a target rather than a minimum/maximum
- `likes_acoustic` — whether the user prefers acoustic-leaning songs

**How the `Recommender` scores each song:**
Each song is scored as a weighted combination of four factors: an exact-match bonus for genre, an exact-match bonus for mood, a closeness score for energy (`1 - abs(song.energy - user.target_energy)`, so songs closer to the target score higher regardless of whether they're above or below it), and a bonus/penalty based on whether the song's acousticness aligns with `likes_acoustic`. Genre is weighted most heavily, since a genre mismatch is a stronger taste violation than a mood mismatch; energy is weighted second, since it is continuous and degrades gracefully; mood and acoustic preference are weighted lightly as secondary modifiers.

**How songs are chosen:**
Every song in the catalog is scored independently (the "Scoring Rule"), then the full list of scored songs is sorted from highest to lowest score and truncated to the top `k` results (the "Ranking Rule"). These are kept as separate steps because scoring a single song requires no knowledge of the rest of the catalog, while deciding what to actually show the user is a separate decision about sorting, ties, and how many results to return.

This section covers the finalized Phase 1 recipe below. Beyond Phase 1, this system also has a set of planned upgrades — semantic search for emotional matching, engagement-weighted collaborative filtering, and per-user importance weighting — documented in [Future Extensions](#future-extensions).

### Finalized Algorithm Recipe

**Weights (out of 100 points total):**

| Signal | Weight | Rationale |
|---|---|---|
| Genre match | 30 | Binary, but the strongest explicit preference signal — a genre mismatch is a strong sign the song isn't "their" music. |
| Mood match | 25 | Nearly as important as genre — mood is often *why* someone picks a song in the moment, but it's fuzzier/more situational than genre. |
| Energy closeness | 25 | Continuous, not binary — scaled smoothly via `1 - abs(song.energy - user.target_energy)` so a near-miss doesn't swamp the score the way a binary factor would. |
| Acoustic match | 20 | Binary, but a secondary/texture preference — real, but shouldn't outweigh genre or mood. |

**Formula:**

```
score = 30 * (genre matches?)
      + 25 * (mood matches?)
      + 25 * (1 - abs(song.energy - user.target_energy))
      + 20 * (acousticness aligns with likes_acoustic?)
```

**Data flow:** `user_prefs` (Input) → loop over every song in `songs.csv`, scoring each one independently against `user_prefs` using the formula above (Process) → sort all scored songs descending and slice to the top `k` (Output).

**Sanity check used to validate the weights:** Storm Runner (rock/intense, high energy, low acousticness) vs. Library Rain (lofi/chill, low energy, high acousticness), scored against a `genre="rock", mood="chill"` profile — chosen deliberately so genre and mood disagree across the two songs, rather than a profile where every signal points the same way. Storm Runner scored 68.5 and Library Rain scored 42.5, confirming genre + acoustic alignment correctly dominates even when energy closeness is nearly tied (0.74 vs. 0.70) between the two songs.

### Potential Biases

- **Over-prioritizing genre**: because genre carries the heaviest weight (30), a song that's a near-perfect mood/energy/acoustic match but in a different genre can be ranked below a same-genre song that matches nothing else — potentially hiding great songs that don't fit the user's stated genre.
- **Cold-start bias toward the user's stated profile**: since there's no behavioral data, the system can only ever recommend toward what a user *says* they like, not what they might actually enjoy but haven't articulated — it can't discover an unexpected taste the way collaborative filtering could.
- **Fixed weights don't fit every listener**: the same 30/25/25/20 split is applied to all users, even though some people may care about mood far more than genre (or vice versa) — see [Future Extensions](#future-extensions) #3.
- **Small catalog skew**: with only a handful of songs per genre, a single mistagged or unusual song can disproportionately affect what looks like the "best" match for a given profile.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

### Baseline profiles

```
=== High-Energy Pop ({'genre': 'pop', 'mood': 'happy', 'energy': 0.85, 'likes_acoustic': False}) ===

Top recommendations:

Sunrise City - Score: 99.25
Because: matches your favorite genre (pop); matches your favorite mood (happy); energy (0.82) is very close to your target (0.85); has the non-acoustic feel you prefer

Gym Hero - Score: 73.00
Because: matches your favorite genre (pop); energy (0.93) is very close to your target (0.85); has the non-acoustic feel you prefer

Rooftop Lights - Score: 67.75
Because: matches your favorite mood (happy); energy (0.76) is very close to your target (0.85); has the non-acoustic feel you prefer

Victory Lap - Score: 44.25
Because: energy (0.88) is very close to your target (0.85); has the non-acoustic feel you prefer

Storm Runner - Score: 43.50
Because: energy (0.91) is very close to your target (0.85); has the non-acoustic feel you prefer


=== Chill Lofi ({'genre': 'lofi', 'mood': 'chill', 'energy': 0.4, 'likes_acoustic': True}) ===

Top recommendations:

Midnight Coding - Score: 99.50
Because: matches your favorite genre (lofi); matches your favorite mood (chill); energy (0.42) is very close to your target (0.4); has the acoustic feel you prefer

Library Rain - Score: 98.75
Because: matches your favorite genre (lofi); matches your favorite mood (chill); energy (0.35) is very close to your target (0.4); has the acoustic feel you prefer

Focus Flow - Score: 75.00
Because: matches your favorite genre (lofi); energy (0.4) is very close to your target (0.4); has the acoustic feel you prefer

Spacewalk Thoughts - Score: 67.00
Because: matches your favorite mood (chill); energy (0.28) is very close to your target (0.4); has the acoustic feel you prefer

Harvest Home - Score: 44.50
Because: energy (0.38) is very close to your target (0.4); has the acoustic feel you prefer


=== Deep Intense Rock ({'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False}) ===

Top recommendations:

Storm Runner - Score: 99.75
Because: matches your favorite genre (rock); matches your favorite mood (intense); energy (0.91) is very close to your target (0.9); has the non-acoustic feel you prefer

Gym Hero - Score: 69.25
Because: matches your favorite mood (intense); energy (0.93) is very close to your target (0.9); has the non-acoustic feel you prefer

Victory Lap - Score: 44.50
Because: energy (0.88) is very close to your target (0.9); has the non-acoustic feel you prefer

Battle Cry - Score: 43.25
Because: energy (0.97) is very close to your target (0.9); has the non-acoustic feel you prefer

Sunrise City - Score: 43.00
Because: energy (0.82) is very close to your target (0.9); has the non-acoustic feel you prefer
```

### Adversarial / edge-case profiles

```
=== Contradictory Signals ({'genre': 'lofi', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': True}) ===

Top recommendations:

Midnight Coding - Score: 63.00
Because: matches your favorite genre (lofi); has the acoustic feel you prefer

Focus Flow - Score: 62.50
Because: matches your favorite genre (lofi); has the acoustic feel you prefer

Library Rain - Score: 61.25
Because: matches your favorite genre (lofi); has the acoustic feel you prefer

Storm Runner - Score: 49.75
Because: matches your favorite mood (intense); energy (0.91) is very close to your target (0.9)

Gym Hero - Score: 49.25
Because: matches your favorite mood (intense); energy (0.93) is very close to your target (0.9)


=== Nonexistent Genre ({'genre': 'opera', 'mood': 'happy', 'energy': 0.7, 'likes_acoustic': False}) ===

Top recommendations:

Rooftop Lights - Score: 68.50
Because: matches your favorite mood (happy); energy (0.76) is very close to your target (0.7); has the non-acoustic feel you prefer

Sunrise City - Score: 67.00
Because: matches your favorite mood (happy); energy (0.82) is very close to your target (0.7); has the non-acoustic feel you prefer

Night Drive Loop - Score: 43.75
Because: energy (0.75) is very close to your target (0.7); has the non-acoustic feel you prefer

Island Sunset - Score: 41.25
Because: energy (0.55) is very close to your target (0.7); has the non-acoustic feel you prefer

Victory Lap - Score: 40.50
Because: energy (0.88) is very close to your target (0.7); has the non-acoustic feel you prefer


=== Worst-Case All-Mismatch ({'genre': 'polka', 'mood': 'furious', 'energy': 0.5, 'likes_acoustic': True}) ===

Top recommendations:

Midnight Coding - Score: 43.00
Because: energy (0.42) is very close to your target (0.5); has the acoustic feel you prefer

Dusty Backroads - Score: 43.00
Because: energy (0.42) is very close to your target (0.5); has the acoustic feel you prefer

Focus Flow - Score: 42.50
Because: energy (0.4) is very close to your target (0.5); has the acoustic feel you prefer

Harvest Home - Score: 42.00
Because: energy (0.38) is very close to your target (0.5); has the acoustic feel you prefer

Coffee Shop Stories - Score: 41.75
Because: energy (0.37) is very close to your target (0.5); has the acoustic feel you prefer
```

**Observations from the adversarial runs:**
- **Contradictory Signals** (lofi genre + intense mood/high energy) resolved as intended: genre's higher weight (30) won the tiebreak, ranking lofi songs above the mood/energy-matched rock and pop songs — confirming the weighting hierarchy behaves as designed even under an internally contradictory profile.
- **Nonexistent Genre** (`opera`, which no song has) still produced a coherent ranking driven entirely by mood, energy, and acoustic signals — the system degrades gracefully rather than breaking when a categorical preference can never match.
- **Worst-Case All-Mismatch** exposed a real gap: Midnight Coding and Dusty Backroads tied at exactly 43.00. The current implementation has no defined tie-breaking rule beyond score, so the order between tied songs is effectively arbitrary (dependent on original CSV order via a stable sort) — documented as a limitation below.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Future Extensions

These are planned upgrades beyond the core content-based recommender, to be implemented later in this project.

**1. Semantic search for emotional matching**
Right now `mood` is a fixed category (e.g., `happy`, `chill`, `intense`) matched by exact string equality — "happy" and "joyful" would be treated as completely unrelated even though they mean nearly the same thing. This extension would:
- Add a free-text `description` field per song (e.g., "an upbeat, sun-drenched pop anthem that feels celebratory").
- Let the user describe their desired vibe in free text instead of picking from a fixed mood list.
- Embed both texts using a sentence-embedding model and score similarity via cosine similarity (same math used for numerical feature closeness, applied to meaning instead of numbers).
- Blend this similarity score into the existing weighted score, and surface the closest-matching phrase as part of the explanation.

**2. Engagement-weighted collaborative filtering ("did they actually vibe to it")**
Raw play counts don't distinguish a song someone loved from one they skipped seconds in. This extension would:
- Add a separate `interactions.csv` (user_id, song_id, played, skipped_after_seconds, replayed, completed) — kept separate from `songs.csv` because engagement is a property of a *user-song pair*, not of the song itself, and a single song can have very different engagement outcomes across different listeners.
- Define an engagement score per listen that weights completions and replays heavily, and treats fast skips as a near-zero or negative signal, rather than treating every play as equal.
- Use engagement-weighted overlap (not raw play overlap) to find users with similar taste, then recommend what those users genuinely engaged with — the collaborative filtering half of the system, layered on top of the content-based scoring already in place.

**3. Per-user importance weighting**
The base recommender uses one fixed weight distribution (genre 30 / mood 25 / energy 25 / acoustic 20) applied to every user — only the *target values* (favorite genre, favorite mood, etc.) differ per person, not how much each feature is allowed to matter. In reality, different listeners prioritize differently: one person picks music almost entirely by mood regardless of genre, while another is fiercely genre-loyal. This extension would:
- Let `UserProfile` optionally carry its own weight distribution (e.g., `genre_importance`, `mood_importance`, `energy_importance`, `acoustic_importance`) instead of relying on the one global default.
- Fall back to the fixed default weights when a user hasn't specified their own, so the base system keeps working unchanged.
- Longer-term, infer these weights from behavior (which connects to extension #2) instead of requiring the user to state them explicitly — e.g., a user who consistently plays full songs outside their stated favorite genre implies genre matters less to them than the default assumes.

---

## Experiments You Tried

### Experiment: Weight Shift — double energy, halve genre

**Change:** In `recommender.py`, `GENRE_WEIGHT` was changed from `30` to `15` (halved) and `ENERGY_WEIGHT` was changed from `25` to `50` (doubled). `MOOD_WEIGHT` (25) and `ACOUSTIC_WEIGHT` (20) were left unchanged.

**Math validity check:** the weights no longer sum to 100 (new total: 15+25+50+20 = 110), so the max possible score is now 110 instead of 100. Every term is still non-negative and bounded — `energy_closeness` stays within [0,1], so its contribution stays within [0,50] — so scores remain internally consistent and comparable to each other; only the "out of 100" framing from the original recipe is no longer literally true.

**Result — a ranking actually flipped:** the clearest effect showed up on the **Contradictory Signals** adversarial profile (`genre="lofi", mood="intense", energy=0.9, likes_acoustic=True`):

| | Original weights (30/25/25/20) | Shifted weights (15/25/50/20) |
|---|---|---|
| 1st place | Midnight Coding (lofi match) — 63.00 | Storm Runner (mood+energy match) — 74.50 |
| 2nd place | Focus Flow (lofi match) — 62.50 | Gym Hero (mood+energy match) — 73.50 |
| 3rd place | Library Rain (lofi match) — 61.25 | Midnight Coding (lofi match) — 61.00 |

Under the original weights, a genre match alone (30 pts) outranked a mood+energy match (25 + ~25 pts) for songs with contradictory profiles. Under the shifted weights, energy's doubled weight (up to 50 pts) combined with a mood match (25 pts) now outranks genre alone (only 15 pts) — flipping which songs land in first and second place entirely.

**Takeaway:** this confirms the weights aren't just cosmetic — they directly determine which feature "wins" when a user's stated preferences conflict with each other. Halving genre's weight measurably weakened its ability to act as a tiebreaker, exactly as the math would predict.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



