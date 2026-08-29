# STYLE PROFILE — Book 1, ch1–11 (the ruled standard)

**Descriptive and numeric. No claim in this file rests on ear.** Every target is a
measured property of the author's own ch1–11 prose, with ch12–30 as contrast.

Ruled 2026-08-29: *"The second half should align with the first."* ch1–11 is
therefore the standard, and this file defines it in numbers so "aligned" is
checkable rather than arguable.

**Corpus:** `6_manuscript/book_1/first_edition_clean/` ch01–ch11 —
23,488 words · 1,627 sentences · 714 paragraphs. Contrast: ch12–30, 47,547 words.
**Method:** text normalised with `bookconfig.norm()` (curly→straight, ellipsis
collapsed); headers, scene-break markers and provenance comments excluded;
sentences split on `(?<=[.!?])\s+`, matching `tic_census.py`.

---

## 1. Sentence length — the primary signature

|  | ch1–11 STANDARD | ch12–30 | ratio |
|---|---|---|---|
| mean words | **14.4** | 7.1 | 2.0× |
| median | **12** | 5 | 2.4× |
| p10 / p25 | **3 / 6** | 2 / 3 | |
| p75 / p90 | **20 / 29** | 9 / 15 | |
| longest | 77 | 47 | |

**Distribution is the target, not the mean.** A chapter can hit mean 14.4 with
uniform 14-word sentences and be wrong.

| words per sentence | ch1–11 | ch12–30 |
|---|---|---|
| 1–4 | **18.4%** | 41.3% |
| 5–9 | **24.0%** | 34.2% |
| 10–14 | **17.5%** | 14.0% |
| 15–19 | **13.2%** | 5.9% |
| 20–29 | **17.0%** | 3.8% |
| 30+ | **9.8%** | 0.8% |

The discriminator is the long tail: **26.8% of the author's sentences run 20+
words, against 4.6% in the back half.** The front half is not "less fragmented" —
it is *wider*. Short sentences are 18.4% of it. Removing fragments without
restoring long sentences produces neither texture.

---

## 2. Paragraphs

|  | ch1–11 | ch12–30 |
|---|---|---|
| words, mean / median | **32.9 / 22** | 16.6 / 12 |
| words, p25 / p75 / p90 | **10 / 45 / 77** | 6 / 23 / 35 |
| sentences per paragraph | **2.60 / median 2** | 2.71 / median 2 |

Sentences-per-paragraph is **not** a discriminator (2.60 vs 2.71). Paragraph
*mass* is: the author's paragraphs carry twice the words at the same sentence
count.

---

## 3. Punctuation, per 1,000 words

| | ch1–11 | ch12–30 | note |
|---|---|---|---|
| em dash | **1.3** | 10.8 | **8.3× — the single largest gap in the book** |
| ellipsis | **3.4** | 2.5 | author uses MORE |
| comma | **60.0** | 45.9 | author uses MORE |
| exclamation | **5.3** | 1.5 | author uses MORE |
| question | 8.2 | 8.0 | not a discriminator |
| semicolon | 0.5 | 0.0 | |
| colon | 0.4 | 1.8 | |

**The author is not a minimalist.** Three of these move *against* the intuition
that the front half is "cleaner": more commas, more exclamations, more ellipses.
What he does not do is reach for the em dash.

---

## 4. Dialogue and attribution

|  | ch1–11 | ch12–30 |
|---|---|---|
| dialogue, share of words | **24.5%** | 34.2% |
| mean quoted span | **10.5 words** | 8.9 |
| spans carrying a speech tag | **38%** | 31% |
| **said-share of tags** | **34%** | 68% |
| distinct speech verbs | **30** | 26 |
| adverb-on-tag ("said quietly") | **0.38/1K** | 1.18/1K |

> **This overturns the kit's Pass 5 recommendation.** `05_DIALOGUE.md` proposes
> said-default, citing RESONANCE at 79%. The author's own standard is **34%
> said across 30 distinct verbs** — a deliberately varied palette. Converting
> GoSquad toward said-default would move it AWAY from ch1–11, i.e. against the
> ruling. Pass 5 must not run on its default recommendation without a fresh
> Director ruling. Adverb-on-tag is the part worth cutting: the back half runs
> 3.1× the author's rate.
>
> **Dialogue is frozen by ruling** ("don't change any dialogue"). These figures
> are a description of the standard, not a licence to edit spoken lines.

---

## 5. Constructions — rate per 1,000 words

| construction | ch1–11 | ch12–30 | verdict |
|---|---|---|---|
| anaphoric `Not X. Not Y.` | **0.00** | 0.25 | **absent from the author's prose** |
| `began/started to` | **0.00** | 0.15 | **absent from the author's prose** |
| `could feel/see/hear` | 0.30 | 0.72 | back half 2.4× |
| `not X, but/just Y` | 0.21 | 0.32 | |
| `X, not Y` | 0.51 | 0.63 | not a discriminator |
| `It was / It wasn't X` | **0.85** | 0.40 | author uses MORE |
| `there was / there were` | **0.64** | 0.19 | author uses MORE |
| sentence opening with "Not" | ~0% | 1.6% | |
| -ly adverbs | **17.8** | 12.1 | author uses MORE |
| `was`/`were` | **22.0** | 14.8 | author uses MORE |
| `-ing` forms | 45.8 | 52.7 | |

**Two constructions measure 0.00 in 23,488 words of the author's prose.** Those
are the only true bans this profile can justify. Everything else is a band, not
a rule.

**Do not "fix" toward fewer adverbs, fewer copulas, or fewer `It was`
openings.** The author uses all three at *higher* rates than the prose being
corrected. Those are exactly the edits an LLM makes by reflex, and here they
push away from the standard.

---

## 6. Somatic register

Per 1,000 words: `chest` **0.21** (back half 1.56, **7.4×**) · `eyes` 1.66 (1.16) ·
`hands` 1.23 (0.82) · `breath` 0.38 (0.29) · `heart` 0.34 (0.46) · `stomach` 0.17 (0.13).

`in her chest` occurs **22 times** in ch12–30 and is not among the author's
repeated phrases at all. It is the clearest single lexical tic in the book.

Filter verbs, per 1K — the author leads with perception, the back half with
sensation: `saw` **1.58** (0.40) · `knew` **1.45** (0.69) · `thought` 1.19 (0.99) ·
`felt` 1.11 (**1.24**) · `heard` 0.72 (0.15).

---

## 7. Formulaicity index

Distinct n-grams repeating ≥3×, per 10,000 words, registered motifs excluded:

| | ch1–11 | ch12–30 |
|---|---|---|
| 4-grams | **10.2** | 25.0 (2.5×) |
| 5-grams | **1.3** | 5.3 (4.1×) |

**The kind of repeat differs, not only the count.** All three of the author's
repeated 5-grams are *content* — "your mother and I have", "next to a stack of",
"Elvis has left the building". The back half's are *construction* — "with the
back of her", "the back of her hand", "that hurt to look at", "I don't know how
to".

This index is the best single measure of the disease, because it is
content-blind and needs no judgement call. **Target: ≤12 repeated 4-grams and
≤2 repeated 5-grams per 10k words.**

Not a discriminator: opener concentration. Top-10 opening words cover 32.9% of
the author's sentences and only 25.5% of the back half's — the author is *more*
concentrated. Do not use opener variety as a quality signal.

---

## 8. The checkable target

A ch12–30 chapter is aligned when all of these hold:

1. short-burst ≤ **that chapter's dialogue floor + 7.2/1K** (per-chapter table in `DECISIONS_LOG.md`)
2. **≥ 20%** of sentences run 20+ words; **≥ 7%** run 30+
3. median sentence **≥ 10** words; mean **≥ 12**
4. em dash **≤ 3.0/1K**
5. repeated 4-grams **≤ 12 per 10k**, repeated 5-grams **≤ 2 per 10k** (motifs excluded)
6. `chest` **≤ 0.5/1K**; zero `Not X. Not Y.`; zero `began/started to`
7. adverb-on-tag **≤ 0.5/1K**
8. paragraph mean **≥ 25** words
9. dialogue unchanged — verify the quoted spans are byte-identical to the source

Criteria 1–8 are measurable by script. Criterion 9 is the ruling's hard boundary.

---

*Derived 2026-08-29 from measurement only. Supersedes the descriptive figures
previously in this file. Where this profile and `GOSQUAD_PROSE_VOICE.md`
disagree, this file has the numbers and that one does not.*
