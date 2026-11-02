#!/usr/bin/env python3
"""
speaker_volley.py — does anyone answer themselves?

    python3 ledger/tools/speaker_volley.py              # whole book
    python3 ledger/tools/speaker_volley.py CH2          # one chapter
    python3 ledger/tools/speaker_volley.py --gap 2      # allow N narration paras between
    python3 ledger/tools/speaker_volley.py --sites      # show every resolved speaker

WHY THIS EXISTS
    CH2:41-43, found 2026-08-10 by two human review lenses reading independently:

        "I just want to register," AIKIN says, "that this is not in my contract."
        "You don't have a contract," OTIS says.
        "Then I'd like to register it informally," OTIS says.     <-- Otis answers Otis

    It survived every build including both Kirkus copies. NOTHING in the toolchain could
    see it: audit.py has no speaker rule, antecedents.py resolves PRONOUNS not named tags,
    census counts only patterns someone thought to name. A tag naming the WRONG LIVE
    CHARACTER is well-formed, real, and in the room — invisible to all three.

    This closes exactly that gap and nothing wider.

WHAT IT FLAGS
    Two consecutive DIALOGUE paragraphs whose explicit speaker tag names the same
    character. In a volley that means somebody replied to themselves.

WHAT IT IS NOT
    Not proof of a defect. A character legitimately speaks twice in a row — pressing a
    point, getting no answer, a speech broken across paragraphs. The signature of the
    REAL defect is a tagged reply to a tagged line by the same mouth, which is why both
    paragraphs must carry an explicit tag to flag. Untagged runs are the attribution
    rule working, not a fault.

    NOT A GATE. Emits candidates; a human reads the passage. Same standing as
    antecedents.py (author-ruled 2026-08-09: "a flag that you then do a clean analysis of").

FIRST FULL RUN, 2026-08-10 — READ THIS BEFORE RE-RUNNING
    Regression-tested against the pre-fix CH2 text FIRST: returned exactly one flag,
    Otis :42 then :43, and nothing else. Only then was its output on the rest of the
    book trusted. Do the same after any change to the tag patterns.

    gap 0 (the real defect signature): 0 flagged across 48 chapters. CH2 was the only
    instance in the book.

    gap 2: 18 flagged, ALL READ, ALL LEGITIMATE. Three shapes, none a defect —
      · narration answers instead of a person (CH16:50-52, Elena hisses "Stay in the
        car," Hendricks puts his hand on the door, "No." — the beat IS his reply)
      · one speech broken by a gesture (CH13:42-44, the hand that reaches and pulls back)
      · interrogation cadence, questions into silence (CH6:80/82/84, CH9:47/50)
    So gap>0 is a noise floor of correct prose, exactly like antecedents.py. Run at gap 0
    for signal; widen only when hunting a specific suspected passage.
"""
import argparse, glob, os, re, sys

try:
    import yaml
except ImportError:
    sys.exit("pyyaml required")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _suite import CFG, prose_files, chapter_id, characters

# The manuscript uses curly quotes and apostrophes. A pattern written with straight
# ones returns zero, and zero reads as clean. (CLAUDE.md, the two traps.)
def norm(s):
    return (s.replace("’", "'").replace("‘", "'")
             .replace("“", '"').replace("”", '"'))

SAID = (r"says?|said|asks?|asked|adds?|added|calls?|called|orders?|ordered|replies|replied|"
        r"murmurs?|murmured|whispers?|whispered|breathes?|breathed|hisses|hissed|snaps|snapped|"
        r"growls|growled|shouts|shouted|answers?|answered|finishes|finished|continues|continued|"
        r"repeats?|repeated|offers?|offered|starts|started|begins|began|manages|managed")

C = dict(red="\033[31m", yel="\033[33m", grn="\033[32m", dim="\033[2m",
         bold="\033[1m", cyn="\033[36m", off="\033[0m")
def c(s, k): return f"{C[k]}{s}{C['off']}" if sys.stdout.isatty() else s


def speaker_names():
    """Every name the prose might use as a dialogue tag."""
    names = set()
    chars = characters()
    # titles that are not names (config: suite.name_skip_tokens)
    skip = {"Doctor", "Dr"} | set(CFG.get("name_skip_tokens") or [])
    for k, v in (chars or {}).items():
        for nm in (str((v or {}).get("canonical_name") or k),):
            for t in re.findall(r"[A-Z][a-z]{2,}", nm):
                if t not in skip:
                    names.add(t)
    # speakers the prose tags who are not (yet) in CHARACTERS.yaml (config: suite.speaker_extra_names)
    names |= set(CFG.get("speaker_extra_names") or [])
    return names


def resolve(para, names):
    """The tagged speaker of a dialogue paragraph, or None if untagged."""
    if '"' not in para:
        return None
    # Tags only count OUTSIDE the quotes — a name spoken aloud is not an attribution.
    outside = re.sub(r'"[^"]*"', " \x00 ", para)
    for pat in (rf"\b({'|'.join(names)})\b\s+(?:{SAID})\b",
                rf"\b(?:{SAID})\b\s+({'|'.join(names)})\b"):
        m = re.search(pat, outside)
        if m:
            return m.group(1)
    return None


def scan(path, names, gap, sites):
    out, prev = [], None          # prev = (speaker, line_no, text)
    since = 0
    for i, raw in enumerate(open(path, encoding="utf-8").read().split("\n"), 1):
        line = norm(raw).strip()
        if not line or line == "---" or line.isupper():
            prev, since = None, 0     # scene break resets the volley
            continue
        spk = resolve(line, names)
        if spk is None:
            if '"' in line:
                prev, since = None, 0   # untagged dialogue breaks the chain we can reason about
            else:
                since += 1
                if since > gap:
                    prev = None
            continue
        if sites:
            out.append(("ok", i, spk, line))
        if prev and prev[0] == spk:
            out.append(("SAME", i, spk, line, prev[1], prev[2], since))
        prev, since = (spk, i, line), 0
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter", nargs="?")
    ap.add_argument("--gap", type=int, default=0,
                    help="narration paragraphs tolerated between the two (default 0 = adjacent)")
    ap.add_argument("--sites", action="store_true")
    a = ap.parse_args()

    names = speaker_names()
    files = prose_files()
    if a.chapter:
        files = [f for f in files if chapter_id(f).upper() == a.chapter.upper()]
        if not files:
            sys.exit(f"no chapter matching {a.chapter!r}")

    print(c("\nSPEAKER VOLLEY — consecutive tagged lines by the same mouth", "bold"))
    print(c(f"  {len(names)} known speakers · gap tolerance {a.gap}", "dim"))
    if not names:
        print(c("  ✗ no speaker names known — nothing can be checked (an empty list would match everything).\n"
                "    Fill ledger/codex/CHARACTERS.yaml (canonical_name) or suite.speaker_extra_names, then rerun.", "red"))
        return 1
    total = 0
    for f in files:
        hits = [h for h in scan(f, names, a.gap, a.sites) if h[0] == "SAME"]
        if not hits:
            continue
        print(c(f"\n  {chapter_id(f)}", "cyn"))
        for _, ln, spk, text, pln, ptext, since in hits:
            total += 1
            mid = "" if since == 0 else f"  ({since} narration para{'s' if since > 1 else ''} between)"
            print(f"   {c('SAME', 'red')} {spk} at :{pln} then :{ln}{mid}")
            print(f"       :{pln}  {ptext[:96]}")
            print(f"       :{ln}  {text[:96]}")
    print(c("\n" + "─" * 62, "dim"))
    print(f"  {c(str(total) + ' flagged', 'red' if total else 'grn')}")
    print(c("  A tagged reply to a tagged line by the same mouth. Read each before\n"
            "  calling it a defect — pressing a point unanswered is legitimate.", "dim"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
