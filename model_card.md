# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**SerenBeatity**

*Find Your Sound by Vibe*

---

## 2. Intended Use  

SerenBeatity recommends and ranks songs from a small catalog. It uses a listener's favorite genre, favorite mood, target energy, and acoustic preference. It returns the top five songs, each with a score and a short list of reasons.

It assumes each listener can describe their taste with one genre, one mood, and one energy level. It also assumes that taste stays the same every time they listen.

**Intended use:** a small educational simulation for learning how content-based recommenders work.

**Not intended for:** real listeners or real products. It is not a replacement for Spotify, Pandora, or any real personalized recommender. It does not learn from listening history, and its catalog is far too small for everyday use.

---

## 3. How the Model Works  

SerenBeatity gives every song points, adds them up, and shows the highest scores first.

- **Genre match:** +1.0 if the song's genre is exactly the listener's favorite.
- **Mood match:** +1.5 if the song's mood is exactly the listener's favorite.
- **Energy closeness:** up to +3.0. A song with exactly the target energy gets all 3.0 points. The points shrink as the song gets further away, and reach zero at a gap of 0.5 or more.
- **Acoustic preference:** up to +1.0. Listeners who like acoustic music get more points for more acoustic songs. Listeners who don't get more points for less acoustic songs. If no preference is given, every song gets a neutral 0.5.

The best possible score is 6.5. Genre and mood ignore capital letters and extra spaces, so "Pop" matches "pop". If two songs tie, the song with the closer energy wins. If they are still tied, the song with the lower id wins.

The starter scoring and ranking functions were placeholders. I implemented the point system, deterministic tie-breaking rules, and plain-language explanations.

---

## 4. Data  

The catalog has 18 songs. Each song has an id, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness.

The starter catalog contained 10 songs. I added 8 more, expanding it to 18 songs and adding hip-hop, R&B, gospel, afrobeats, reggae, classical, country, and soul.

It covers 15 genres, including pop, lofi, rock, r&b, hip-hop, soul, country, classical, jazz, reggae, gospel, and afrobeats. It covers 14 moods, such as happy, chill, intense, romantic, and nostalgic. Most genres and moods appear only once. Only lofi (3 songs) and pop (2 songs) have more than one song in their genre.

The scoring uses only genre, mood, energy, and acousticness. Tempo, valence, and danceability are stored but not scored yet.

A lot of musical taste is missing. The data has no lyrics, no information about which artists are similar, no listening history, and no context like "studying" or "working out." Popular genres like metal, EDM, and Latin music are not included at all.

---

## 5. Strengths  

SerenBeatity works best when the listener's genre and mood are well represented in the catalog.

- For all three regular profiles, the #1 song matched both genre and mood: Sunrise City for pop, Library Rain for lofi, and Velvet Hours for R&B.
- The Chill Acoustic Lofi profile got the strongest list. All of its top four songs matched the genre or the mood.
- Energy and acoustic preference clearly separate very different listeners. The pop and lofi lists shared no songs at all.
- Every recommendation comes with reasons, so it is easy to see why a song was picked.

---

## 6. Limitations and Bias 

The system's biggest weakness is that energy closeness (worth up to 3.0 points) outweighs an exact genre and mood match combined (2.5 points), and genre and mood get no partial credit for similar styles. As a result, the recommender often behaves more like an "energy matcher" than a taste matcher: for a classical/nostalgic listener asking for energy 0.95, Gym Hero (pop/intense) ranked #1, while Letters in Autumn, the only song matching both genre and mood, ranked #3. The same pattern explains why Gravel Road Home (country) ranked #2 for a Romantic R&B listener: after the catalog's single R&B song, the list was filled by energy closeness, so related genres like hip-hop and soul received no advantage. Doubling the energy weight in an experiment made this worse, pushing Letters in Autumn out of the top five entirely, which shows that the weights need rebalancing rather than amplification.

---

## 7. Evaluation  

I ran `python -m src.main` with four user profiles and checked whether each top five matched what a real listener with that taste would expect.

**Profiles tested**

- **High-Energy Happy Pop:** pop, happy, energy 0.9, does not like acoustic music.
- **Chill Acoustic Lofi:** lofi, chill, energy 0.3, likes acoustic music.
- **Romantic R&B:** r&b, romantic, energy 0.6, does not like acoustic music.
- **Adversarial Classical Nostalgic:** classical, nostalgic, energy 0.95, no acoustic preference. This profile is built to conflict, because the only classical/nostalgic song in the catalog is very low-energy.

**Biggest surprises**

Two results stood out. Gravel Road Home, a country song, ranked #2 for the Romantic R&B listener, ahead of the hip-hop and soul songs that sound much closer to R&B. And for the Classical Nostalgic listener, Gym Hero (pop/intense) ranked #1 while Letters in Autumn ranked only #3, even though it was the only song matching both the genre and the mood. Both happened for the same reason: energy closeness is worth up to 3.0 points, more than a genre and mood match combined (2.5 points), so a song with the "right" energy can overpower a song with the right musical style.

**Profile comparisons**

- **High-Energy Happy Pop vs. Chill Acoustic Lofi:** The two lists share no songs. Pop got upbeat, low-acoustic songs like Sunrise City and Gym Hero, while lofi got quiet, highly acoustic songs like Library Rain and Midnight Coding. This makes sense because the profiles sit at opposite ends of both energy (0.9 vs. 0.3) and acoustic preference.
- **High-Energy Happy Pop vs. Romantic R&B:** Both users dislike acoustic music, but their lists share no songs because R&B targets medium energy (0.6). Pop had several genre and mood matches, so its scores stayed close together, while R&B had only one match (Velvet Hours) and every song after it dropped by more than two points.
- **High-Energy Happy Pop vs. Adversarial Classical Nostalgic:** Four of the five songs are the same (Gym Hero, Storm Runner, Sunrise City, Sunday Owambe), even though these users asked for completely different styles. Because both target very high energy and the classical listener's only style match had no energy points, energy decided almost the whole list.
- **Chill Acoustic Lofi vs. Romantic R&B:** Each list has a strong #1 that matches both genre and mood. Lofi's top four all matched the genre or the mood because the catalog has three lofi and three chill songs, while R&B's #2–#5 matched neither, because the catalog has only one R&B song. The acoustic preference also pulled the lists apart: lofi favored very acoustic songs, and R&B favored less acoustic ones.
- **Chill Acoustic Lofi vs. Adversarial Classical Nostalgic:** Letters in Autumn appears in both lists, and it actually scored higher for the lofi listener (3.49, #5) than for the classical listener (3.00, #3). For lofi, its low energy and high acousticness fit well; for the classical listener, its energy was too far from 0.95 to earn any energy points.
- **Romantic R&B vs. Adversarial Classical Nostalgic:** Both profiles have exactly one song that matches both genre and mood. Velvet Hours ranked #1 for R&B because its energy (0.48) was close to the target and still earned 2.28 energy points, while Letters in Autumn (0.22) was too far from 0.95 and earned none. A style match only wins when the song's energy is reasonably close.

**Weight-shift experiment**

As a test, I temporarily doubled the energy weight from 3.0 to 6.0 and halved the genre weight from 1.0 to 0.5. The results became different but mostly less accurate. For example, Storm Runner (rock) passed Rooftop Lights (happy indie pop) for the pop listener, and Letters in Autumn dropped out of the adversarial top five entirely. I then restored the original weights and confirmed that all four profiles returned to their verified results.

---

## 8. Future Work  

- **Smarter matching:** give partial credit to related genres and moods, and rebalance the weights.
- **A bigger, balanced catalog:** expand and balance the catalog so every genre and mood has several choices.
- **More information:** use tempo, valence, danceability, lyrics, artist relationships, and listening feedback.

---

## 9. Personal Reflection  

Building SerenBeatity taught me that a recommender is only as good as its data and the choices behind its scoring rules. I was surprised that a simple point system could produce recommendations that sometimes felt personal, even though it did not truly understand music. AI helped me brainstorm features, design the scoring formula, create test profiles, review code changes, and explain unexpected rankings. However, I still needed to double-check the math, terminal results, proposed diffs, and claims about the starter code because AI could make assumptions or overlook small details. My biggest learning moment was seeing how doubling the energy weight made the recommendations less accurate, which showed me how strongly one design choice can affect an entire system. If I continued the project, I would add related-genre matching, expand the catalog, and use listening feedback and more song features.
