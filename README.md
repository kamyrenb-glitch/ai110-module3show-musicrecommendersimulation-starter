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

Real-world recommenders often combine two approaches. **Collaborative filtering** uses user behavior, such as "people who liked this song also liked that one." **Content-based filtering** uses the attributes of the items themselves, such as a song's energy or mood. Large platforms usually blend both.

This simulation is **content-based only**. It compares each song's attributes to one user's stated preferences. Energy closeness matters most, followed by mood, then genre and acoustic preference (equal weight).

### What each `Song` stores

`id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`

### What each `UserProfile` stores

`favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`

### Stored vs. used for scoring

A `Song` stores more features than the scoring recipe currently uses. Only features with a matching user preference are scored:

| Song feature | Matching preference | Points |
|---|---|---|
| `energy` | `target_energy`: `3.0 * max(0, 1 - abs(song.energy - user.energy) / 0.5)` | up to 3.0 |
| `mood` | `favorite_mood` (exact match) | 1.5 |
| `genre` | `favorite_genre` (exact match) | 1.0 |
| `acousticness` | `likes_acoustic`: `song.acousticness` if True, otherwise `1 - song.acousticness` | up to 1.0 |

Energy points shrink as the song's energy moves away from the target and reach 0 once the gap is 0.5 or more.

`tempo_bpm`, `danceability`, and `valence` are stored but **not scored yet**, because the profile has no target for them. They are planned as future improvements. `id`, `title`, and `artist` identify the song and are not scored.

### Ranking

Each song gets a score from **0.0 to 6.5 points**. Songs are ranked by:

1. Highest score
2. Smallest energy gap, if scores tie
3. Lowest song `id`, if still tied

The top K songs are returned, each with an explanation of how it earned its points.

### Planned test profile

```python
user_prefs = {
    "genre": "r&b",
    "mood": "romantic",
    "energy": 0.6,
    "likes_acoustic": False,
}
```

### Bias and limitations

- **Small catalog:** only one song is R&B and only one is romantic (the same song), so it gets a large head start over everything else.
- **Exact matching:** related genres and moods, such as hip-hop, soul, or "soulful" vs. "romantic", earn no genre or mood points even when the vibe is similar.
- **Personal choices:** the 0.5 energy cutoff and fixed point values reflect my preferences and may not suit every listener.
- **Missing information:** lyrics, artist relationships, and personal listening context are not represented.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

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

These outputs come from running `python -m src.main` with four stress-test profiles, the last of which is adversarial on purpose.

### High-Energy Happy Pop

```text
Loading songs from data/songs.csv...
Loaded songs: 18

============================================================
Profile: High-Energy Happy Pop
User profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9, 'likes_acoustic': False}
============================================================

Top recommendations:

1. Sunrise City by Neon Echo - Score: 5.84
   - genre match: pop (+1.00)
   - mood match: happy (+1.50)
   - energy 0.82 vs target 0.90 (+2.52)
   - non-acoustic preference (+0.82)

2. Gym Hero by Max Pulse - Score: 4.77
   - genre match: pop (+1.00)
   - mood does not match happy (+0.00)
   - energy 0.93 vs target 0.90 (+2.82)
   - non-acoustic preference (+0.95)

3. Rooftop Lights by Indigo Parade - Score: 4.31
   - genre does not match pop (+0.00)
   - mood match: happy (+1.50)
   - energy 0.76 vs target 0.90 (+2.16)
   - non-acoustic preference (+0.65)

4. Storm Runner by Voltline - Score: 3.84
   - genre does not match pop (+0.00)
   - mood does not match happy (+0.00)
   - energy 0.91 vs target 0.90 (+2.94)
   - non-acoustic preference (+0.90)

5. Sunday Owambe by Kola Breeze - Score: 3.25
   - genre does not match pop (+0.00)
   - mood does not match happy (+0.00)
   - energy 0.80 vs target 0.90 (+2.40)
   - non-acoustic preference (+0.85)
```

### Chill Acoustic Lofi

```text
============================================================
Profile: Chill Acoustic Lofi
User profile: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.3, 'likes_acoustic': True}
============================================================

Top recommendations:

1. Library Rain by Paper Lanterns - Score: 6.06
   - genre match: lofi (+1.00)
   - mood match: chill (+1.50)
   - energy 0.35 vs target 0.30 (+2.70)
   - acoustic preference (+0.86)

2. Midnight Coding by LoRoom - Score: 5.49
   - genre match: lofi (+1.00)
   - mood match: chill (+1.50)
   - energy 0.42 vs target 0.30 (+2.28)
   - acoustic preference (+0.71)

3. Spacewalk Thoughts by Orbit Bloom - Score: 5.30
   - genre does not match lofi (+0.00)
   - mood match: chill (+1.50)
   - energy 0.28 vs target 0.30 (+2.88)
   - acoustic preference (+0.92)

4. Focus Flow by LoRoom - Score: 4.18
   - genre match: lofi (+1.00)
   - mood does not match chill (+0.00)
   - energy 0.40 vs target 0.30 (+2.40)
   - acoustic preference (+0.78)

5. Letters in Autumn by Elena Varga Quartet - Score: 3.49
   - genre does not match lofi (+0.00)
   - mood does not match chill (+0.00)
   - energy 0.22 vs target 0.30 (+2.52)
   - acoustic preference (+0.97)
```

### Romantic R&B

```text
============================================================
Profile: Romantic R&B
User profile: {'genre': 'r&b', 'mood': 'romantic', 'energy': 0.6, 'likes_acoustic': False}
============================================================

Top recommendations:

1. Velvet Hours by Amara Lux - Score: 5.48
   - genre match: r&b (+1.00)
   - mood match: romantic (+1.50)
   - energy 0.48 vs target 0.60 (+2.28)
   - non-acoustic preference (+0.70)

2. Gravel Road Home by Dusty Rowe - Score: 3.20
   - genre does not match r&b (+0.00)
   - mood does not match romantic (+0.00)
   - energy 0.58 vs target 0.60 (+2.88)
   - non-acoustic preference (+0.32)

3. Crown Talk by Vel Kingsley - Score: 3.20
   - genre does not match r&b (+0.00)
   - mood does not match romantic (+0.00)
   - energy 0.72 vs target 0.60 (+2.28)
   - non-acoustic preference (+0.92)

4. Morning Glory Rise by Grace Avenue Choir - Score: 3.07
   - genre does not match r&b (+0.00)
   - mood does not match romantic (+0.00)
   - energy 0.68 vs target 0.60 (+2.52)
   - non-acoustic preference (+0.55)

5. Honeyed Testimony by Marvella Jones - Score: 3.02
   - genre does not match r&b (+0.00)
   - mood does not match romantic (+0.00)
   - energy 0.52 vs target 0.60 (+2.52)
   - non-acoustic preference (+0.50)
```

### Adversarial Classical Nostalgic

```text
============================================================
Profile: Adversarial Classical Nostalgic
User profile: {'genre': 'classical', 'mood': 'nostalgic', 'energy': 0.95}
============================================================

Top recommendations:

1. Gym Hero by Max Pulse - Score: 3.38
   - genre does not match classical (+0.00)
   - mood does not match nostalgic (+0.00)
   - energy 0.93 vs target 0.95 (+2.88)
   - no acoustic preference given (+0.50)

2. Storm Runner by Voltline - Score: 3.26
   - genre does not match classical (+0.00)
   - mood does not match nostalgic (+0.00)
   - energy 0.91 vs target 0.95 (+2.76)
   - no acoustic preference given (+0.50)

3. Letters in Autumn by Elena Varga Quartet - Score: 3.00
   - genre match: classical (+1.00)
   - mood match: nostalgic (+1.50)
   - energy 0.22 vs target 0.95 (+0.00)
   - no acoustic preference given (+0.50)

4. Sunrise City by Neon Echo - Score: 2.72
   - genre does not match classical (+0.00)
   - mood does not match nostalgic (+0.00)
   - energy 0.82 vs target 0.95 (+2.22)
   - no acoustic preference given (+0.50)

5. Sunday Owambe by Kola Breeze - Score: 2.60
   - genre does not match classical (+0.00)
   - mood does not match nostalgic (+0.00)
   - energy 0.80 vs target 0.95 (+2.10)
   - no acoustic preference given (+0.50)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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



