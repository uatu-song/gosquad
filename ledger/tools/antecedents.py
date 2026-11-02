#!/usr/bin/env python3
"""
antecedents.py — does every pronoun have somebody to point at?

    python3 ledger/tools/antecedents.py                 # whole book, narration
    python3 ledger/tools/antecedents.py CH35            # one chapter
    python3 ledger/tools/antecedents.py CH35 --sites    # every pronoun, resolved
    python3 ledger/tools/antecedents.py --dialogue      # include quoted speech

WHY THIS EXISTS
    On 2026-08-09 CH35 carried '"The Meridians are our best option," he says.'
    The intended speaker was Okonkwo, who is a woman. Three separate checks were
    clean: audit.py had no pronoun rule, the codex declared her a man, and the
    typography gate has no opinion about people. The line was only caught because
    the author asked "isn't Okonkwo a woman?"

    R016 (audit.py section 5) now compares DECLARATIONS. It cannot compare
    REFERENCE — the pronoun in that sentence names nobody, so nothing binds it.
    This tool is the reference half: for every pronoun, who is actually available
    to be its antecedent, and is that set unambiguous?

WHAT IT REPORTS
    ORPHAN     no candidate of that gender is live — the pronoun points at nobody
    AMBIGUOUS  two or more live candidates of that gender; a reader must guess
    BARE       a definite description with no referent ("the man", "the woman")

HOW "LIVE" IS DECIDED
    A character is live if named within the last WINDOW paragraphs, reset at each
    scene break. The POV character is ALWAYS live — in an Elena-POV chapter a bare
    "she" is Elena by default, and flagging those would bury the real hits.

NOT A GATE. AUTHOR-RULED 2026-08-09: "This shouldn't be mechanically run, it
should be a flag that you then do a clean analysis of it."
    Deliberately NOT wired into audit.py, and NOT in pre-commit. It emits
    CANDIDATES. Somebody then reads the passages. On the full manuscript it
    returns ~68 mis-attributions, ~537 orphans and ~1,017 ambiguities, and the
    overwhelming majority are correct prose — a two-hander where the nearest
    name is the OTHER speaker reads as mis-attributed to a machine and as
    obvious to a reader. Wiring this to a gate would train everyone to ignore it,
    which is how the pronoun defect survived in the first place.

WHAT IT IS NOT
    Not a coreference resolver. It knows who is AVAILABLE, not who is MEANT. An
    AMBIGUOUS verdict is an invitation to read the passage, not a defect. Silence
    here means every pronoun had exactly one plausible owner — which is a much
    weaker claim than "every pronoun is correct." Do not report a clean run as
    proof the prose is right, and do not report a flag as a defect until the
    passage has been read.
"""
import argparse, glob, os, re, sys

try:
    import yaml
except ImportError:
    sys.exit("pyyaml required")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _suite import CFG, prose_files, chapter_id, characters, pov_of

WINDOW = 6          # paragraphs a name stays "live"
NEAR   = 1          # paragraphs within which two candidates genuinely COMPETE

# Unnamed people are referents too. Without these, every "the big man came around
# the bench... behind him" scans as a pronoun pointing at nobody — 1,118 of the
# first run's 1,118 orphans were ordinary prose introducing someone by description.
UNNAMED = re.compile(
    r"\b(?:a|an|the|one|another|some|this|that)\s+(?:\w+\s+){0,2}"
    r"(man|woman|guy|boy|girl|lady|kid|trader|soldier|technician|officer|doctor|priest)\b",
    re.I)
UNNAMED_G = {"woman": "fem", "girl": "fem", "lady": "fem",
             "man": "masc", "guy": "masc", "boy": "masc"}

C = dict(red="\033[31m", yel="\033[33m", grn="\033[32m", dim="\033[2m",
         bold="\033[1m", cyn="\033[36m", off="\033[0m")
def c(s, k): return f"{C[k]}{s}{C['off']}" if sys.stdout.isatty() else s

# The manuscript uses curly apostrophes. A pattern written with a straight one
# returns zero, and zero reads as clean. (CLAUDE.md, the two traps.)
def norm(s):
    return (s.replace("’", "'").replace("‘", "'")
             .replace("“", '"').replace("”", '"'))

FEM  = {"she", "her", "hers", "herself"}
MASC = {"he", "him", "his", "himself"}
PRON = FEM | MASC
BARE = re.compile(r"\b(?:the|that|this)\s+(man|woman)\b", re.I)


def load_characters():
    """token -> 'fem'/'masc'. Ambiguous tokens (two claimants) are dropped."""
    chars = characters()
    # titles/shared tokens that are not one person's name (config: suite.name_skip_tokens)
    skip = set(CFG.get("name_skip_tokens") or [])
    # Reference follows the PROSE, not the declaration: a character declared it/they whom
    # the book calls "she" is a live feminine candidate (config: suite.pronoun_overrides,
    # {"Name": "fem"|"masc"}). In Resonance this was Four ("Ships are girls.").
    overrides = {str(k): v for k, v in (CFG.get("pronoun_overrides") or {}).items()}
    tok = {}
    for k, v in (chars or {}).items():
        dem = ((v or {}).get("demographics") or {})
        pr = {str(x).lower() for x in (dem.get("pronouns") or [])}
        g = "fem" if pr & FEM else ("masc" if pr & MASC else None)
        names = [str(v.get("canonical_name") or k)]
        if not g:
            continue
        for nm in names:
            for t in re.findall(r"[A-Z][a-z]{2,}", nm):
                if t in skip:
                    continue
                tok[t] = None if tok.get(t, g) != g else g
    tok = {t: g for t, g in tok.items() if g}
    tok.update(overrides)
    return tok


def pov_gender(pov, tok):
    """The POV character is always live. Returns (name, gender) or (None, None)."""
    for t, g in tok.items():
        if re.search(rf"\b{t}\b", pov or ""):
            return t, g
    return None, None


# Dialogue attribution is a CLOSED construction, and readers resolve it by
# proximity: '"...," he says' attaches to the last person the prose named. That
# makes it the one place a bare pronoun can be checked without coreference — and
# it is exactly where the 2026-08-09 defect lived ('"...," he says' three lines
# after Okonkwo, who is a woman, was the last actor named).
ATTRIB = re.compile(r'["\u201d,.!?]\s*(he|she)\s+'
                    r'(says?|said|asks?|asked|adds?|added|calls?|called|orders?|ordered|'
                    r'finishes|finished|repeats?|repeated|offers?|offered)\b', re.I)


def strip_dialogue(s):
    return re.sub(r'"[^"]*"', " ", s)


def scan(path, tok, include_dialogue, sites):
    stem = chapter_id(path)
    pov = pov_of(path)
    pov_name, pov_g = pov_gender(pov, tok)
    # Intercut chapters swap POV mid-chapter; the default-live assumption does not
    # hold, so we do not apply it there rather than emit confident nonsense.
    if "intercut" in str(pov).lower():
        pov_name = pov_g = None

    live = {}          # token -> paragraphs since last named
    unnamed = {}       # "the big man" -> gender, for people the prose never names
    out = []
    for i, raw in enumerate(open(path, encoding="utf-8").read().split("\n"), 1):
        line = norm(raw)
        if not line.strip() or line.strip() == "---":
            live.clear(); unnamed.clear()                      # scene break resets everyone
            continue
        text = line if include_dialogue else strip_dialogue(line)

        # Who is named in this paragraph, and where?
        named_here = {t: m.start() for t in tok
                      for m in [re.search(rf"\b{t}\b", line)] if m}

        for m in re.finditer(r"\b(" + "|".join(sorted(PRON)) + r")\b", text, re.I):
            w = m.group(1).lower()
            g = "fem" if w in FEM else "masc"
            # candidates live BEFORE this pronoun: named earlier in this paragraph,
            # or carried in from a previous one.
            here  = {t for t, pos in named_here.items() if pos < m.start() and tok[t] == g}
            carry = {t for t, age in live.items() if tok[t] == g}
            cands = here | carry | {u for u, ug in unnamed.items() if ug == g}
            if pov_name and pov_g == g:
                cands.add(pov_name)
            # COMPETING = named close enough that a reader is actually choosing.
            # At the full 6-paragraph window every crowded scene reads as
            # ambiguous, which is a measure of the cast, not of the prose.
            near = here | {t for t, age in live.items() if tok[t] == g and age <= NEAR}
            if pov_name and pov_g == g:
                near.add(pov_name)
            if not cands:
                out.append((i, "ORPHAN", w, sorted(cands), raw.strip()))
            elif len(near) > 1:
                out.append((i, "AMBIGUOUS", w, sorted(near), raw.strip()))
            elif sites:
                out.append((i, "ok", w, sorted(cands), raw.strip()))

        # --- attribution check: nearest named actor wins, gender must agree
        for am in ATTRIB.finditer(line):
            w = am.group(1).lower()
            g = "fem" if w in FEM else "masc"
            before = [(pos, t) for t, pos in named_here.items() if pos < am.start()]
            nearest = max(before)[1] if before else (
                min(live, key=live.get) if live else None)
            if nearest and tok.get(nearest) and tok[nearest] != g:
                out.append((i, "MISATTRIB", f"{w} {am.group(2)}", [nearest], raw.strip()))

        for um in UNNAMED.finditer(text):
            g = UNNAMED_G.get(um.group(1).lower())
            if g:
                unnamed[um.group(0).strip().lower()] = g

        for bm in BARE.finditer(text):
            g = "fem" if bm.group(1).lower() == "woman" else "masc"
            cands = {t for t in named_here if tok[t] == g} | \
                    {t for t in live if tok[t] == g}
            if not cands:
                out.append((i, "BARE", bm.group(0), [], raw.strip()))

        for t in named_here:
            live[t] = 0
        for t in list(live):
            live[t] += 1
            if live[t] > WINDOW:
                del live[t]
    return stem, pov, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter", nargs="?", help="e.g. CH35 (default: whole book)")
    ap.add_argument("--dialogue", action="store_true", help="include quoted speech")
    ap.add_argument("--sites", action="store_true", help="print every pronoun resolved")
    a = ap.parse_args()

    tok = load_characters()
    if not tok:
        print("ANTECEDENTS: no gendered characters known — every pronoun would read as an orphan.\n"
              "  Declare demographics.pronouns in ledger/codex/CHARACTERS.yaml (or suite.pronoun_overrides), then rerun.")
        return 1
    files = prose_files()
    if a.chapter:
        files = [f for f in files if chapter_id(f).upper() == a.chapter.upper()]
        if not files:
            sys.exit(f"no chapter matching {a.chapter!r}")

    print(c("\nANTECEDENTS  — every pronoun, and who is available to own it", "bold"))
    print(c(f"  {len(tok)} gendered characters · window {WINDOW} paragraphs · "
            f"{'dialogue included' if a.dialogue else 'narration only'}", "dim"))

    tot = dict(ORPHAN=0, AMBIGUOUS=0, BARE=0, MISATTRIB=0, ok=0)
    for f in files:
        stem, pov, out = scan(f, tok, a.dialogue, a.sites)
        hits = [o for o in out if o[1] != "ok"]
        for _, v, *_ in out:
            tot[v] += 1
        if not hits and not a.sites:
            continue
        print(c(f"\n  {stem}", "cyn") + c(f"   POV: {pov}", "dim"))
        for ln, verdict, w, cands, raw in out:
            if verdict == "ok" and not a.sites:
                continue
            col = {"ORPHAN": "red", "AMBIGUOUS": "yel", "BARE": "red",
                   "MISATTRIB": "red", "ok": "dim"}[verdict]
            who = ", ".join(cands) if cands else "nobody"
            print(f"   {c(verdict.ljust(9), col)} :{ln}  '{w}'  -> {who}")
            if verdict != "ok":
                print(f"       {c(raw[:96], 'dim')}")

    print(c("\n" + "─" * 62, "dim"))
    print(f"  {c(str(tot['MISATTRIB']) + ' mis-attributed', 'red')}   "
          f"{c(str(tot['ORPHAN']) + ' orphan', 'red')}   "
          f"{c(str(tot['AMBIGUOUS']) + ' ambiguous', 'yel')}   "
          f"{c(str(tot['BARE']) + ' bare description', 'red')}")
    print(c("  AMBIGUOUS means a reader COULD misread it, not that it is wrong.\n"
            "  Silence means each pronoun had one plausible owner — NOT that the\n"
            "  prose is correct. This tool knows availability, not intent.", "dim"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
