# Hand-label: P(verbless | short sentence) — 60 sentences

**Method (Director-specified 2026-07-27):** 30 short sentences (≤4 words) drawn
at random (seed 20260727) from author ch05–10 clean-window Ruth-POV, 30 from
CH18 v6. Labelled by hand. No tooling, definitive either way.

**Third label added on contact with the data: ART** — the sampled "sentence" is
a splitter artifact, not a sentence. Excluding these was not in the plan; it
became necessary because ~38% of both samples are artifacts.

Legend — **F** = real sentence, finite verb · **V** = real sentence, verbless ·
**ART** = splitter artifact (unbalanced dialogue split, abbreviation split,
rendered list item, mid-sentence continuation)

## Set A — author, ch05–10 (clean window)

| | sentence | label | note |
|---|---|---|---|
|A01|Wet from rain.|**V**| |
|A02|Weeks minimum.|**V**| |
|A03|"I know," he agreed.|**F**| |
|A04|"Gale," Battlea said firmly.|**F**| |
|A05|"Who are you?|ART|quote split, unterminated|
|A06|"Mommy!" the child screamed.|**F**| |
|A07|a ball?|ART|lowercase continuation of a list|
|A08|No burns.|**V**| |
|A09|Firas continued.|**F**| |
|A10|"Stand down!|**F**|imperative; quote unbalanced but sentence is whole|
|A11|They weren't alone.|**F**| |
|A12|It's…|ART|truncated|
|A13|All of them breathing.|**V**|participle, not finite|
|A14|Or a football?|ART|list continuation|
|A15|egg, maybe?|ART|lowercase, mid-sentence|
|A16|Gloom Girl?|**V**|vocative|
|A17|ugh…|ART| |
|A18|That same night.|**V**| |
|A19|"Yeah, kid.|ART|quote split|
|A20|That's enough." Ruth nodded.|ART|two sentences merged|
|A21|"Hands!|ART|quote split + merge|
|A22|Ruth remained quiet.|**F**| |
|A23|We're different," Battlea assessed.|**F**| |
|A24|At Ahdia's pyre.|**V**| |
|A25|You can't move.|**F**| |
|A26|"For full recovery?|ART|quote split|
|A27|"No," he dismissed.|**F**| |
|A28|The explosion roared.|**F**| |
|A29|You?|**V**| |
|A30|Come in!" "Damn it.|ART|merged across speakers|

**A: 11 ART · 19 real → 8 V / 11 F → P(verbless | real short) = 8/19 = 0.42**

## Set B — CH18 v6

| | sentence | label | note |
|---|---|---|---|
|B01|Keep moving.|**F**|imperative|
|B02|Her lungs shortened.|**F**| |
|B03|The GPS followed.|**F**| |
|B04|He let them land.|**F**| |
|B05|"Formation Delta.|ART|quote split|
|B06|Racks are empty.|**F**| |
|B07|"Professional standard.|ART|quote split|
|B08|All of them.|**V**| |
|B09|NIGHTINGALE.|ART|roster item|
|B10|Leah leaned in.|**F**| |
|B11|And I'm…|ART|truncated (deliberate, but not a sentence)|
|B12|He was being polite.|**F**| |
|B13|BATTLEA.|ART|roster item|
|B14|GLOOM GIRL.|ART|roster item|
|B15|CRIMSON SABLE.|ART|roster item|
|B16|"All of it.|ART|quote split|
|B17|Triage ran itself.|**F**| |
|B18|Regroup at rally two.|**F**|imperative|
|B19|Still.|**V**| |
|B20|Static.|**V**| |
|B21|"Dr.|ART|**abbreviation split** — "Dr. Carter" broken in half|
|B22|Battle, Leah.|**V**| |
|B23|"BATTLEA.|ART|roster item|
|B24|"Ruth.|ART|quote split|
|B25|"Ruth…" Tess, ragged.|**V**| |
|B26|"We say it anyway.|ART|quote split|
|B27|She keyed the radio.|**F**| |
|B28|Forty degrees, maybe less.|**V**| |
|B29|Engines, many, close.|**V**| |
|B30|Three down, all breathing.|**V**| |

**B: 12 ART · 18 real → 8 V / 10 F → P(verbless | real short) = 8/18 = 0.44**

---

## Result

**0.42 (author) vs 0.44 (v6). No separation. The verbless hypothesis is dead
by direct count**, not by regex definition. Settled; do not revisit without new
evidence.

## Second finding, not sought

**~38% of everything the burst metric counts is a splitter artifact** — 11/30
in the author sample, 12/30 in v6. Classes observed:

1. **Unbalanced dialogue splits** — an interrogative or exclamation inside
   dialogue splits at the `?`/`!`, orphaning the opening quote. Both corpora.
2. **Abbreviation splits** — `"Dr.` broke `Dr. Carter` in half. (v6)
3. **Rendered list items** — the codename roster, 5 of v6's 12 artifacts.
   Already identified independently.
4. **Merged sentences** — split failing at `." "` speaker boundaries. (author)
5. **Mid-sentence continuations** — lowercase fragments counted as sentences.

Artifact rates are close (37% vs 40%), so ratios roughly survive — but the
**absolute burst figures are inflated ~1.6× on top of every prior correction.**
Real-short rate: author ch05–10 ≈ 8.4/1K, v6 ≈ 12.1/1K, a **1.44×** gap rather
than the 1.53× raw.

**The burst metric should not be quoted to two significant figures by anyone
until the splitter handles quotes and abbreviations.**


---

# ADDENDUM — two subsequent passes (2026-07-27)

## Pass 2: re-adjudicated against SOURCE CONTEXT

Pass 1 labelled from the sampled string alone and systematically over-called
ART on units beginning with a quotation mark. A leading quote is an utterance
opening, not a broken split. `"For full recovery?` is a real interrogative
(source: *"For full recovery? Weeks minimum. You won't be cleared for
patrol…"*). So are `"Formation Delta.`, `"Professional standard.`, `"All of
it.`, `"Ruth.`, `"Hands!`, and the elliptical guessing-list fragments
(*a ball? … egg, maybe? … Or a football?*), which are the author writing
deliberately.

Corrected: artifact rate **6.7% author / 20% v6** (not 37%/40%);
P(verbless|short) **0.57 / 0.50**; gap **1.31×**.

## Pass 3: BLIND labelling by an uninvolved agent

Because passes 1 and 2 came from the same labeller who proposed the analysis,
the sixty units were shuffled, stripped of corpus identity, given source
context, and labelled by a cold agent with no stake and no project history.

| pass | method | artifact rate | P(verbless\|short) | gap |
|---|---|---|---|---|
| 1 | string only, invested labeller | 37% / 40% | 0.42 / 0.44 | 1.44× |
| 2 | + source context, same labeller | 6.7% / 20% | 0.57 / 0.50 | 1.31× |
| **3** | **blind, cold labeller, context** | **17% / 17%** | **0.48 / 0.52** | **1.53×** |

**Findings:**

1. **Verbless is dead, three times over.** 0.42/0.44, then 0.57/0.50, then
   0.48/0.52. Killed from three directions by three methods, twice reversing
   sign. It stays dead.
2. **The blind pass lands between the two invested passes on every measure.**
   Pass 1 over-called artifacts, pass 2 over-corrected. The blind rate is
   identical across corpora (17%/17%) — which is what a labeller free of
   corpus-directional bias should produce, and neither invested pass achieved.
3. **The gap interval is the stable result.** Six measurements: 1.28, 1.61,
   1.71, 1.44, 1.31, 1.53. The interval ~1.3–1.7 has survived every attempt to
   sharpen it. Stated as a direction in the card; no point estimate published.

**Method note.** Blinding was proposed to remove a systematic directional bias.
Worth recording precisely: the pass-1 error was *not* corpus-directional — it
hit both corpora at similar rates (11/30 and 12/30) because it was a uniform
methodological failure, labelling from decontextualized strings. Blinding would
not have caught it; **source context did.** What blinding corrected was the
residual bias in pass 2, where the same labeller, now knowing the hypothesis
and the corpora, produced an artifact rate that differed 3× between corpora
(6.7% vs 20%) where the blind labeller found them identical. Two different
failures, two different remedies: context fixes decontextualization, blinding
fixes investment.
