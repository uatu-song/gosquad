# CODEX CHANGELOG — Book 2

Every change to `RULES.yaml` or a code's declaration in `INDEX.yaml`, newest
first, with the `codex_version` it produced. Bump the version on every rule
change; `audit.py` is re-run after each entry.

This file and `RULES.yaml` are excluded from the fossil scan — they *describe*
fossils, so a fossil quoted here is documentation, not a defect.

Format:

```
## v<N> — YYYY-MM-DD — <what changed>
**Change:** the concrete edit
**Why:** the prose fact or ruling that forced it
**Audit after:** paste the receipt (`AUDIT CLEAN` line or the violation count)
```

---

## v1 — 2026-07-26 — canon layer created (empty)

**Change:** Stood up `canon/book_2/` — INDEX, RULES, CHAPTER_INDEX, CANON_FACTS,
PROMISES, DECISIONS_LOG, this file. All registries deliberately empty.

**Why:** Fresh-start rebuild of the canon system. The engine and the canon are
separate steps by design: a codex bulk-generated in one pass is a codex nobody
can trust. Retroactive ingest happens one namespace at a time, each code citing
its live prose site.

**Audit after:** `AUDIT CLEAN (book_2) — 0 rules run over 23 chapters, 5 codex
files.` — with the standing caveat that a clean audit over 0 rules proves the
wiring, not the canon.
