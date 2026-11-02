#!/usr/bin/env python3
"""
suite_check.py — prove the suite is pointed at the book before trusting any tool.

Every tool here reads the chapter files from ledger/config.json -> suite.prose_globs.
If that glob matches nothing, or misses a chapter, every census, gate and audit
reports CLEAN on the text it never read. Zero reads as clean. Resonance lost a
session to a glob that silently dropped the epilogue.

This prints exactly which files the suite sees, the chapter id each one gets,
gaps in the numbering, duplicate ids, and whether the codex files parse.
Exit 1 if the suite would run blind.

Usage: python3 ledger/tools/suite_check.py
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _suite import CFG, CONFIG_F, ROOT, data, prose_files, sealed_files, chapter_id, rel, pov_map

def main():
    bad = 0
    print(f"SUITE CHECK — {CFG['book']}  (repo: {ROOT})")
    if not os.path.exists(CONFIG_F):
        print("  ✗ ledger/config.json missing — run install.py"); return 1
    fs = prose_files()
    print(f"\n  prose_globs {CFG['prose_globs']} → {len(fs)} files")
    if not fs:
        print("  ✗ NOTHING MATCHED. Every tool would report clean on zero text. Fix suite.prose_globs.")
        return 1
    ids = [chapter_id(f) for f in fs]
    for f, i in zip(fs, ids):
        print(f"    {i:8} {rel(f)}")
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        bad += 1; print(f"  ✗ duplicate chapter ids: {dup} (two files map to one id; fix chapter_id_regex or filenames)")
    nums = sorted(int(m.group(1)) for i in ids for m in [re.match(r"CH(\d+)$", i)] if m)
    if nums:
        missing = [n for n in range(nums[0], nums[-1] + 1) if n not in nums]
        if missing:
            print(f"  ! numbering gaps: {missing} — a missed chapter, or deliberate? Check before trusting counts.")
    unid = [rel(f) for f, i in zip(fs, ids) if not re.match(CFG["chapter_id_regex"], i)]
    if unid:
        print(f"  ! files with no chapter id (the stem is used): {unid}")
    sf = sealed_files()
    print(f"\n  seal_globs {CFG['seal_globs']} → {len(sf)} files"
          + ("" if set(sf) == set(fs) else "   (differs from prose_globs — intended?)"))
    print("\n  codex files:")
    try:
        import yaml
    except ImportError:
        print("  ✗ pyyaml not installed: pip install pyyaml"); return 1
    for name in ("RULES.yaml", "RULES_CANDIDATES.yaml", "INDEX.yaml", "CHAPTER_INDEX.yaml",
                 "CHARACTERS.yaml", "CORE.yaml"):
        p = data(name)
        if not os.path.exists(p):
            print(f"    -  {name:24} absent"); continue
        try:
            yaml.safe_load(open(p, encoding="utf-8")); print(f"    ✓  {name:24} parses")
        except Exception as e:
            bad += 1; print(f"    ✗  {name:24} DOES NOT PARSE: {str(e).splitlines()[0]}")
    povs = pov_map()
    unpov = [i for i in ids if i not in povs]
    print(f"\n  CHAPTER_INDEX: {len(ids) - len(unpov)}/{len(ids)} chapters have a POV entry"
          + ("" if not unpov else "   (POV-scoped rules skip the rest; fill as you verify)"))
    style = CFG.get("typography_house_style") or {}
    print(f"  typography house style: {style if style else 'NOT RULED — check_typography runs as census only'}")
    print(f"  motifs registered: {len(CFG['_raw'].get('motifs') or [])}"
          + ("" if CFG['_raw'].get('motifs') else "   (author to confirm motif_candidates before Pass 4)"))
    print("\n" + ("SUITE READY" if not bad else f"✗ {bad} problem(s) — fix before trusting any tool"))
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
