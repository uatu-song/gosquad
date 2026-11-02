"""
_suite.py — the one place the editing suite learns where this book lives.

Every tool imports this instead of hard-coding paths. All paths come from
ledger/config.json (key "suite"), relative to the repo root (two levels above
this file). Change the book's layout there, never inside a tool.
"""
import glob, io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CONFIG_F = os.path.join(ROOT, "ledger", "config.json")

_DEFAULT = {
    "book": "the book",
    "author": "the author",
    "prose_globs": ["chapters/*.txt"],
    "prose_exclude": [],
    "chapter_id_regex": r"(CH\d+[a-z]?|EP|PR)",
    "data_dir": "ledger/codex",
    "codex_globs": ["ledger/codex/*.yaml", "ledger/codex/*.md"],
    "seal_globs": ["chapters/*.txt"],
    "extra_speech_regex": "",
}


def P(*a):
    return os.path.join(ROOT, *a)


def config():
    try:
        cfg = json.load(io.open(CONFIG_F, encoding="utf-8"))
    except (OSError, ValueError):
        cfg = {}
    s = dict(_DEFAULT)
    s.update(cfg.get("suite") or {})
    s["_raw"] = cfg
    return s


CFG = config()


def data(name):
    """Path of a codex file (RULES.yaml, INDEX.yaml, CHAPTER_INDEX.yaml, ...)."""
    return P(CFG["data_dir"], name)


def _expand(globs, exclude=()):
    out = []
    for g in globs:
        out += glob.glob(P(g))
    out = [f for f in sorted(set(out)) if os.path.isfile(f)
           and not os.path.basename(f).startswith("_")
           and not any(x in f for x in exclude)]
    return sorted(out, key=chapter_sort_key)


def prose_files():
    """The edit-of-record chapter files, in reading order."""
    return _expand(CFG["prose_globs"], CFG.get("prose_exclude") or [])


def sealed_files():
    return _expand(CFG["seal_globs"])


def chapter_id(path):
    """'CH07', 'EP', 'PR' … from the filename; the stem if nothing matches."""
    stem = os.path.splitext(os.path.basename(path))[0]
    m = re.search(CFG["chapter_id_regex"], stem)
    return m.group(1) if m else stem


def chapter_num(path):
    cid = chapter_id(path)
    if cid in ("PR", "PROLOGUE"):
        return 0
    m = re.search(r"(\d+)", cid)
    return int(m.group(1)) if m else 999


def chapter_sort_key(path):
    cid = chapter_id(path)
    m = re.search(r"(\d+)([a-z]?)", cid)
    return (chapter_num(path), m.group(2) if m else "", cid)


# ── TYPOGRAPHY ───────────────────────────────────────────────────────────────
# Manuscripts use CURLY quotes (’ “ ”); patterns get written with straight ones.
# A grep that cannot fire returns zero, and zero reads as CLEAN. Normalise first.
def norm(s):
    return (s.replace("’", "'").replace("‘", "'")
             .replace("“", '"').replace("”", '"')
             .replace("—", "--").replace("–", "-"))


def strip_dialogue(line):
    """Remove quoted speech (after norm) — narration-only rules must not fire inside dialogue."""
    t = norm(line)
    t = re.sub(r'"[^"]*"', " ", t)
    extra = CFG.get("extra_speech_regex")
    if extra:
        t = re.sub(extra, " ", t)
    return t


def in_dialogue(line, pos):
    """True if character `pos` of a RAW line sits inside an open curly or straight quote."""
    pre = line[:pos]
    if pre.count("“") > pre.count("”"):
        return True
    if "“" not in line and pre.count('"') % 2 == 1:
        return True
    return False


def load_yaml(p):
    import yaml
    with io.open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_jsonl(p):
    out = []
    if not os.path.exists(p):
        return out
    for ln in io.open(p, encoding="utf-8"):
        ln = ln.strip()
        if not ln:
            continue
        try:
            r = json.loads(ln)
        except ValueError:
            continue
        if isinstance(r, dict) and r.get("id"):
            out.append(r)
    return out


def pov_map():
    """{chapter_id or file stem: pov} from ledger/codex/CHAPTER_INDEX.yaml (the POV authority)."""
    try:
        idx = load_yaml(data("CHAPTER_INDEX.yaml"))["chapters"] or {}
    except Exception:
        return {}
    return {str(k): str((v or {}).get("pov", "")) for k, v in idx.items()}


def pov_of(path, povs=None):
    povs = pov_map() if povs is None else povs
    stem = os.path.splitext(os.path.basename(path))[0]
    return povs.get(stem) or povs.get(chapter_id(path)) or ""


def characters():
    try:
        return load_yaml(data("CHARACTERS.yaml")).get("characters") or {}
    except Exception:
        return {}


def rel(path):
    return os.path.relpath(path, ROOT)
