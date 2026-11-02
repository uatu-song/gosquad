#!/usr/bin/env python3
"""
style_metrics.py — per-chapter prose metrics for ledger/STYLE_PROFILE.md (harvest duty 6).

DESCRIPTIVE ONLY. These numbers measure; they never recommend. A high fragment rate
may be a protected device (cadence can be armor). Run the function test before
treating any number as a defect.

Columns: words · sentences · mean/median sentence length · fragments (sentences of
<=4 words) % · dialogue share of words · em dashes, ellipses, semicolons, -ly words
per 10k words · "said" share of dialogue tags.

Usage:
  python3 ledger/tools/style_metrics.py              # table to stdout
  python3 ledger/tools/style_metrics.py CH12         # one chapter
  python3 ledger/tools/style_metrics.py --append     # also append dated rows to STYLE_PROFILE.md
"""
import datetime, os, re, statistics as st, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _suite import ROOT, CFG, prose_files, chapter_id, pov_of

DIAL = re.compile(r'“[^”]*”?|"[^"\n]*"?')
PUNCT_ONLY = re.compile(r"^[.…—–,;:!?\"'“”‘’*_-]+$")
TAG = re.compile(r"[”\",]\s+(?:\w+\s+){0,2}?(said|says|asked|asks|replied|shouted|yelled|whispered|"
                 r"snapped|muttered|called|answered|added|murmured|growled|hissed|cried|demanded|"
                 r"sang|sung|told|explained|continued|interrupted|barked|screamed)\b", re.I)
LY_SKIP = {"only", "family", "early", "likely", "reply", "fly", "belly", "holy", "ugly", "silly",
           "apply", "supply", "rally", "ally", "bully", "jelly", "lily", "daily", "july", "italy",
           "rely", "lovely", "lonely", "friendly", "elderly", "ghostly", "deadly", "costly", "kelly"}

def words(s):
    return [t for t in s.split() if not PUNCT_ONLY.match(t)]

def metrics(text):
    text = text.replace("*", "")
    w = words(text)
    n = max(len(w), 1)
    dial_words = sum(len(words(m.group(0))) for m in DIAL.finditer(text))
    # sentence ends at . ! ? … (optionally followed by a closing quote); a closing quote alone
    # does not end one — '“Go,” Bourn said.' is one sentence, not two.
    sents = []
    for para in text.split("\n"):
        sents += [s for s in re.split(r"(?<=[.!?…])[”\"’]?\s+(?=[“\"‘A-Z])", para) if words(s)]
    L = [len(words(s)) for s in sents] or [0]
    tags = [m.group(1).lower() for m in TAG.finditer(text)]
    ly = [t for t in re.findall(r"\b[a-z]+ly\b", text.lower()) if t not in LY_SKIP]
    per10k = lambda k: round(k * 10000 / n, 1)
    return dict(
        words=len(w), sents=len(sents), mean=round(st.mean(L), 1), median=st.median(L),
        frag=round(100 * sum(1 for x in L if x <= 4) / max(len(L), 1), 1),
        dial=round(100 * dial_words / n, 1),
        em=per10k(text.count("—")), ell=per10k(text.count("…") + len(re.findall(r"\.\.\.|\. \. \.", text))),
        semi=per10k(text.count(";")), ly=per10k(len(ly)),
        said=(round(100 * tags.count("said") / len(tags)) if tags else None), tags=len(tags))

def main():
    only = next((a for a in sys.argv[1:] if not a.startswith("--")), None)
    fs = [f for f in prose_files() if not only or chapter_id(f).upper() == only.upper()]
    if not fs: sys.exit("style_metrics: no chapters matched")
    rows, alltext = [], []
    hdr = f"{'ch':7}{'words':>7}{'sents':>6}{'mean':>6}{'med':>5}{'frag%':>7}{'dial%':>7}{'em':>7}{'ell':>6}{'semi':>6}{'-ly':>6}{'said%':>7}"
    print(f"STYLE METRICS — {CFG['book']} (rates per 10k words; descriptive only)\n" + hdr)
    for f in fs:
        t = open(f, encoding="utf-8").read(); alltext.append(t)
        m = metrics(t); rows.append((chapter_id(f), pov_of(f), m))
        print(f"{chapter_id(f):7}{m['words']:7}{m['sents']:6}{m['mean']:6}{m['median']:5}{m['frag']:7}{m['dial']:7}"
              f"{m['em']:7}{m['ell']:6}{m['semi']:6}{m['ly']:6}{(m['said'] if m['said'] is not None else '-'):>7}")
    if len(fs) > 1:
        m = metrics("\n".join(alltext))
        print(f"{'BOOK':7}{m['words']:7}{m['sents']:6}{m['mean']:6}{m['median']:5}{m['frag']:7}{m['dial']:7}"
              f"{m['em']:7}{m['ell']:6}{m['semi']:6}{m['ly']:6}{(m['said'] if m['said'] is not None else '-'):>7}"
              f"   ({m['tags']} dialogue tags)")
    if "--append" in sys.argv:
        p = os.path.join(ROOT, "ledger", "STYLE_PROFILE.md")
        d = datetime.date.today().isoformat()
        with open(p, "a", encoding="utf-8") as fh:
            for ch, pov, m in rows:
                fh.write(f"| {d} | {ch} | {m['words']} | {m['sents']} | {m['mean']} | {m['median']} | {m['frag']} | "
                         f"{m['dial']} | {m['em']} | {m['ell']} | {m['semi']} | | {pov} |\n")
        print(f"\nappended {len(rows)} rows to ledger/STYLE_PROFILE.md")
    return 0

if __name__ == "__main__":
    sys.exit(main())
