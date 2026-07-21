# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

VibeMatch recommends songs from a small catalog based on a listener's stated taste. You tell it what genre, mood, energy level, and acoustic-vs-produced sound you like, and it ranks every song in the catalog by how well it matches those four things.

It assumes the user already knows and can state their taste in these exact terms — it does not try to guess taste from listening history, since there is none. This is a classroom simulation, not a production system. It is built for learning how content-based recommenders work, not for real listeners with real music libraries.

---

## 3. How the Model Works  

Every song has four things we check: its genre, its mood, how energetic it is, and how acoustic (vs. electronic/produced) it sounds. Every user profile says what genre they want, what mood they want, what energy level they want, and whether they prefer acoustic or non-acoustic songs.

For each song, the system checks each of these four things one at a time and hands out points:

- If the song's genre matches what the user asked for, it gets a chunk of points.
- If the song's mood matches, it gets another chunk.
- Energy isn't a yes/no match — the system checks *how close* the song's energy is to what the user wants, and gives more points the closer it is, even if it's not a perfect match.
- If the song's acoustic style matches what the user prefers (acoustic or not), it gets a final chunk of points.

All four chunks get added together into one score. The song with the most points wins the top spot. Genre is worth the most points, mood and energy are worth about the same as each other, and acoustic style is worth the least — because a wrong genre feels like a bigger miss to a listener than a slightly-off energy level.

The starter code had none of this built — it was empty placeholders. Everything above (the point values, the closeness math for energy, and the reasons that explain each score) was designed and built from scratch for this project.

---

## 4. Data  

The catalog has 18 songs, each with a title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. It started as a 10-song starter file; I added 8 more songs by hand to bring in genres and moods that weren't represented yet — hip hop, metal, classical, folk, r&b, house, country, and reggae, plus moods like angry, dreamy, nostalgic, romantic, triumphant, bittersweet, and hopeful.

Even after adding those, most genres only have exactly one song. Only pop and lofi have more than two. That means for most possible genre preferences, there's barely any real choice for the system to pick from.

The dataset also has a real gap in energy: it's got plenty of low-energy songs and plenty of high-energy songs, but almost nothing in the middle. A listener who wants "moderately energetic" music is underserved simply because that kind of song isn't in the data at all. There's also nothing about lyrics, vocals, instruments, or language — the dataset only captures a handful of numeric/categorical audio traits, not the fuller feel of a song a real listener would notice.

---

## 5. Strengths  

The system works best for users whose taste lines up cleanly across all four features — for example, someone who wants "lofi, chill, low energy, acoustic" gets a very sensible, obviously-correct top pick (Library Rain or Midnight Coding), because every signal agrees.

It also handles conflicting or impossible requests without breaking. If someone asks for a genre that isn't in the catalog, or contradicts themselves (like wanting an intense, high-energy lofi song), the system doesn't crash or return nonsense — it just falls back to whatever features can still be compared, and still produces a ranked list.

The scoring also captures a pattern that feels intuitive: a song that's "close enough" on energy still gets a fair amount of credit instead of being punished as if it were completely wrong. That closeness-based approach for energy matched my own instincts about how taste actually works — nobody wants only songs at *exactly* their target energy.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

During experiments, the energy-closeness formula (`1 - abs(song.energy - user.target_energy)`) revealed a distributional bias: the catalog's energy values cluster into a low-energy group (0.28–0.55) and a high-energy group (0.75–0.97), leaving a gap between roughly 0.55 and 0.75 with almost no songs. A user who honestly wants moderate energy (e.g., target_energy=0.65) can never score above roughly 0.90 on this factor no matter how well-specified their taste is, simply because the data doesn't contain songs in that range. This means the system unintentionally favors users whose preferences happen to land inside one of the two clusters, and structurally underserves "in-between" listeners — a gap in the data, not a flaw in any individual user's stated profile. The same experiment also showed this bias gets *worse* the more heavily energy is weighted: doubling `ENERGY_WEIGHT` (see Experiments) amplified how much a user's position relative to this gap determined their results.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

### Profiles tested

I tested six profiles: three "normal" ones (High-Energy Pop, Chill Lofi, Deep Intense Rock) and three "adversarial" ones designed to break the system on purpose (Contradictory Signals, Nonexistent Genre, Worst-Case All-Mismatch). For each one, I looked at whether the #1 song actually made sense for that kind of listener, and whether the reasons printed alongside each score matched the math.

### What surprised me

The biggest surprise was that **Gym Hero kept showing up near the top for "Happy Pop"-style profiles, even though its mood is labeled "intense," not "happy."** At first this looks like a mistake — why would an intense song show up for someone who explicitly asked for happy music? But it makes sense once you look at all four things being checked, not just one: Gym Hero is genuinely pop (genre matches), its energy (0.93) is very close to what a high-energy listener asked for, and it's a non-acoustic, produced-sounding track (matches the acoustic preference too). It only fails on one out of four checks — mood. Since genre, energy, and acoustic preference all agree, it earns enough points from those three to land near the top even without the mood match. In plain terms: the system isn't asking "is this song happy," it's asking "how many of the four things you care about does this song get right," and Gym Hero gets three out of four. That's a real and somewhat unintuitive side effect of adding up separate scores instead of requiring every category to match.

### Profile-to-profile comparisons

**High-Energy Pop vs. Chill Lofi:** These landed on completely different top songs (Sunrise City vs. Midnight Coding), which makes sense — every one of the four features (genre, mood, energy, acoustic) points in an opposite direction between these two profiles, so there's no overlap possible. This is the cleanest, most predictable comparison of the six.

**Chill Lofi vs. Deep Intense Rock:** Same story — opposite genres, opposite moods, opposite energy targets, opposite acoustic preference. Storm Runner (rock/intense/loud) topped one list and was nowhere near the top of the other. This comparison mainly confirmed the basics are working, not anything surprising.

**High-Energy Pop vs. Deep Intense Rock:** These two actually share something — both want high energy and both prefer non-acoustic songs. The difference is genre and mood. This showed up clearly in the results: Gym Hero appeared in the top 5 for *both* profiles, since it satisfies the shared energy/acoustic preference regardless of which genre/mood profile is asking. This is a good example of a song "crossing over" between two otherwise different listener types because it happens to sit in the overlap of what they both want.

**Contradictory Signals vs. Nonexistent Genre:** Contradictory Signals (wanting lofi genre but intense mood/high energy) ended up ranking lofi songs highest anyway, purely because genre was worth more points than mood and energy combined at the time. Nonexistent Genre (asking for "opera," which isn't in the catalog) had no choice but to rank purely on mood, energy, and acoustic fit, since genre could never contribute anything. The comparison shows the system doesn't break when a preference can't be satisfied — it just quietly falls back to whatever features *can* still be compared.

**Nonexistent Genre vs. Worst-Case All-Mismatch:** Nonexistent Genre still got mood matches for some songs (happy songs existed), while Worst-Case asked for a mood ("furious") that also doesn't exist anywhere in the catalog. As a result, Worst-Case's rankings were driven by energy and acoustic preference alone — and this is exactly the run where two songs tied at the same score, since with only two working features left, it's much easier for two different songs to land on an identical number by coincidence.

**Overall takeaway:** comparing these profiles side by side shows the system is doing exactly what it's designed to do — reward songs for however many stated preferences they satisfy, in proportion to how much each preference is weighted. The "surprising" results (Gym Hero, the tie) aren't bugs — they're direct, explainable consequences of scoring by addition instead of requiring a perfect match on every category.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

1. **Let users pick more than one favorite genre or mood.** Right now the system forces someone to name exactly one of each, which shuts out anyone with mixed taste. Letting a user list two or three genres they like would fix a real filter-bubble problem, not just a nice-to-have.
2. **Add a real collaborative-filtering layer.** This system only ever recommends toward what a user *says* they like. Adding actual listening/engagement data (see the "engagement-weighted collaborative filtering" idea already sketched in the README) would let it also recommend things a user didn't think to ask for, the way real music apps do.
3. **Force a little diversity into the top 5 instead of pure highest-score-wins.** Right now if three songs are all lofi and chill, all three can dominate the list even though they're barely different from each other. Reserving one slot in the results for something genuinely different would make recommendations feel less repetitive.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

My biggest learning moment was realizing that a "recommendation" isn't some deep understanding of a song — it's just addition. Four numbers get checked, points get handed out, and whichever song has the most points wins. Once I saw the math laid out in front of me (like the Gym Hero case), the whole idea of a recommender system stopped feeling mysterious and started feeling like a spreadsheet with extra steps.

Using AI as a coding assistant helped me most when I needed to turn a vague idea ("energy should count how *close* it is, not just high or low") into an actual formula, and when I needed a sanity check on numbers I'd picked somewhat by feel (like the point weights). I had to double-check it, though, any time it gave me a concrete number or claim I hadn't verified myself — for example, when it proposed weights, I made it walk the math through real songs before I trusted the ranking made sense, and when it suggested a fix ("floor energy at 0"), I checked the data myself and found the fix wasn't even necessary, since energy is already bounded between 0 and 1.

What surprised me most is how convincingly a very simple system can *feel* like it understands your taste. Watching Sunrise City win with a 99.25 score for a "happy pop" listener felt satisfying and correct — even though nothing about the system actually knows what "happy" sounds like. It's just checking a label against another label. That gap between how confident the output feels and how simple the logic actually is changed how I think about real recommendation apps: a lot of the "magic" is really just very well-tuned bookkeeping, layered many times over.

If I extended this project, I'd want to try adding the semantic-search idea from the Future Extensions section — letting the system compare free-text descriptions of vibe instead of relying on fixed categories — since that's the piece that would start to make it feel less like a spreadsheet and more like it actually understands what a song feels like.
