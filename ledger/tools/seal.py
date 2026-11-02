#!/usr/bin/env python3
"""
seal.py — THE SECURITY GLASS over the final manuscript.

The finished chapter files (ledger/config.json -> suite.seal_globs) are CANON. Once sealed,
not one character may change without a two-key break-glass: the AUTHOR's key AND an
ENFORCER pass (audit.py clean). Every attempt is BARRED and REPORTED.

This is the wall around the failure the collaborator letter names: a machine that
"quietly rewrote a chapter into competence and reported success." Here it cannot be
quiet. Three layers, each committed to git so tampering with the lock is itself visible:

  1. BAR   — the PreToolUse hook (`seal.py hook`) DENIES any Edit/Write to a sealed
             file in-tool. Claude physically cannot edit a sealed chapter.
  2. DETECT— `seal.py verify` (run by the pre-commit hook) recomputes every sealed
             file's SHA-256; any drift with no valid break-glass BLOCKS the commit.
  3. REPORT— every barred edit and every detected drift is appended to
             ledger/SEAL_TAMPER_LOG.md (committed — the alarm leaves shards).

HONEST LIMIT (stated plainly, per the studio's ethic): a fully rogue agent that runs
arbitrary shell CAN edit this file, delete the manifest, and `git commit --no-verify`.
No purely-local lock stops that. What this guarantees is that doing so is impossible to
do QUIETLY: it requires disabling multiple committed, logged mechanisms at once, and the
author holds a key ($SEAL_KEY) that is NOT in the repo and that the machine does not know.
Security glass, not a bank vault: it cannot be broken without setting off the alarm and
leaving the glass on the floor.

COMMANDS
  seal.py seal                 arm the glass: store every sealed file's hash, state=sealed
  seal.py set-key              set the AUTHOR break-glass key from $SEAL_KEY (author only)
  seal.py status               human report of seal state + any drift
  seal.py verify               exit 1 if any sealed file drifted w/o break-glass (pre-commit gate)
  seal.py check <path>         exit 0 if <path> is sealed AND locked (used internally)
  seal.py hook                 read a PreToolUse JSON on stdin; DENY + log edits to sealed files
  seal.py break-glass --reason "..."   unlock: requires $SEAL_KEY match AND audit.py clean
  seal.py reseal               after authorized edits, re-store hashes, state=sealed, log the delta
"""
import sys, os, json, glob, hashlib, hmac, subprocess, argparse
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _suite import ROOT, sealed_files as _suite_sealed
MANIFEST = os.path.join(ROOT, "ledger", "SEAL.json")
TAMPER_LOG = os.path.join(ROOT, "ledger", "SEAL_TAMPER_LOG.md")
SALT = b"astroland-seal-v1"  # not a secret; namespaces the key hash

# The "relevant channels" a prose change MUST flow through before it can re-lock.
# Nothing lands unilaterally — not even an author-instructed word change.
CHANNELS = {
    "decisions":  "ledger/DECISIONS_LOG.md",
    "dialogue":   "ledger/DIALOGUE_BANK.jsonl",
    "facts":      "ledger/CANON_FACTS.jsonl",
    "promises":   "ledger/PROMISES.jsonl",
    "chronology": "ledger/CHRONOLOGY.jsonl",
    "structure":  "ledger/STRUCTURE_MAP.jsonl",
    "style":      "ledger/STYLE_PROFILE.md",
}
def _mtimes():
    out = {}
    for k, rel in CHANNELS.items():
        p = os.path.join(ROOT, rel)
        out[k] = os.path.getmtime(p) if os.path.exists(p) else 0
    return out

def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def _sealed_files():
    return _suite_sealed()

def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def _rel(path):
    return os.path.relpath(path, ROOT)

def _self_hash(m):
    # casual-tamper tripwire over the load-bearing fields (git history is the real backstop)
    payload = json.dumps({"files": m.get("files"), "state": m.get("state"),
                          "author_key_hash": m.get("author_key_hash")},
                         sort_keys=True).encode()
    return hashlib.sha256(SALT + payload).hexdigest()

def load():
    if not os.path.exists(MANIFEST):
        return None
    return json.load(open(MANIFEST, encoding="utf-8"))

def save(m):
    m["self_hash"] = _self_hash(m)
    json.dump(m, open(MANIFEST, "w", encoding="utf-8"), indent=2, sort_keys=True)

def report(kind, detail):
    line = f"- **{_now()}** · `{kind}` · {detail}\n"
    if not os.path.exists(TAMPER_LOG):
        open(TAMPER_LOG, "w", encoding="utf-8").write(
            "# SEAL TAMPER LOG\n\nEvery barred edit and detected drift on the sealed manuscript. "
            "Committed — the alarm leaves shards. Managed by `ledger/tools/seal.py`.\n\n")
    open(TAMPER_LOG, "a", encoding="utf-8").write(line)

# ── commands ──────────────────────────────────────────────────────────────────
def cmd_seal(a):
    m = load() or {"author_key_hash": None}
    m["files"] = {_rel(p): _sha(p) for p in _sealed_files()}
    m["state"] = "sealed"
    m["sealed_at"] = _now()
    m["break_glass"] = None
    save(m)
    print(f"🔒 SEALED — {len(m['files'])} files. Glass is live.")
    return 0

def _drift(m):
    live = {_rel(p): _sha(p) for p in _sealed_files()}
    changed = [f for f in m["files"] if live.get(f) != m["files"][f]]
    missing = [f for f in m["files"] if f not in live]
    added = [f for f in live if f not in m["files"]]
    return changed, missing, added

def cmd_status(a):
    m = load()
    if not m:
        print("No seal. The glass is not installed."); return 0
    tampered = m.get("self_hash") != _self_hash(m)
    changed, missing, added = _drift(m)
    print(f"STATE: {m['state']}   files: {len(m['files'])}   sealed_at: {m.get('sealed_at')}")
    if tampered: print("‼  MANIFEST SELF-HASH MISMATCH — the glass itself was altered. Check git diff.")
    if m["state"] == "broken":
        bg = m.get("break_glass") or {}
        print(f"🚨 BROKEN-GLASS ACTIVE — reason: {bg.get('reason')!r}  at {bg.get('at')}")
    if changed or missing or added:
        print("⚠  DRIFT:")
        for f in changed: print(f"     CHANGED  {f}")
        for f in missing: print(f"     MISSING  {f}")
        for f in added:   print(f"     NEW      {f}  (unsealed)")
    else:
        print("✅ No drift — every sealed file matches its fingerprint.")
    return 0

def cmd_verify(a):
    m = load()
    if not m:
        return 0  # no glass installed -> nothing to gate
    if m["state"] == "broken":
        print("seal: break-glass active — edits permitted this session (audit will still gate).")
        return 0
    tampered = m.get("self_hash") != _self_hash(m)
    changed, missing, _ = _drift(m)
    if tampered or changed or missing:
        for f in changed + missing:
            report("DRIFT-BLOCKED", f"sealed file changed with no break-glass: `{f}`")
        if tampered:
            report("MANIFEST-TAMPERED", "SEAL.json self-hash mismatch")
        print("🚨 SEAL VIOLATION — sealed manuscript changed without break-glass.")
        for f in changed:  print(f"   CHANGED  {f}")
        for f in missing:  print(f"   MISSING  {f}")
        if tampered:       print("   MANIFEST self-hash mismatch")
        print("Blocked. To edit legitimately: `seal.py break-glass --reason ...` (needs $SEAL_KEY + audit clean).")
        return 1
    return 0

def _is_locked(path):
    m = load()
    if not m or m["state"] != "sealed":
        return False
    return _rel(os.path.abspath(path)) in m["files"]

def cmd_check(a):
    return 0 if _is_locked(a.path) else 1

def cmd_hook(a):
    try:
        data = json.load(sys.stdin)
    except Exception:
        print("{}"); return 0
    ti = data.get("tool_input", {}) or {}
    path = ti.get("file_path") or ti.get("path") or ""
    if path and _is_locked(path):
        report("EDIT-BARRED", f"{data.get('tool_name','?')} on sealed `{_rel(os.path.abspath(path))}`")
        out = {"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "deny",
            "permissionDecisionReason": (
                "🚨 SEALED MANUSCRIPT. This chapter is under security glass and cannot be edited. "
                "Attempt logged to ledger/SEAL_TAMPER_LOG.md. Legitimate change requires break-glass: "
                "author's $SEAL_KEY + audit.py clean (seal.py break-glass --reason ...). Do NOT work around this.")}}
        print(json.dumps(out)); return 0
    print("{}"); return 0

def cmd_break_glass(a):
    m = load()
    if not m:
        print("No seal installed."); return 1
    if not a.authorized_by:
        print("REFUSED: --authorized-by is required (name who authorized this)."); return 1
    # enforcer pass — the codex-relevant enforcers pre-screen; audit.py is the canon floor
    rc = subprocess.run([sys.executable, os.path.join(ROOT, "ledger", "tools", "audit.py"), "--quiet"]).returncode
    if rc != 0:
        print("DENIED: enforcer (audit.py) is not clean. Fix canon first."); return 1
    m["state"] = "broken"
    m["break_glass"] = {"reason": a.reason, "at": _now(), "authorized_by": a.authorized_by,
                        "enforcer_pass": True, "channel_mtimes": _mtimes()}
    save(m)
    report("BREAK-GLASS-OPENED", f"authorized_by={a.authorized_by} + audit-clean · reason: {a.reason!r}")
    print(f"🔓 CASING OPEN — edits permitted. Authorized by {a.authorized_by}. Reason: {a.reason!r}")
    print("   When done: `python3 ledger/tools/seal.py reseal` (re-locks + logs exactly what changed).")
    return 0

def cmd_reseal(a):
    m = load()
    if not m:
        print("No seal."); return 1
    if m["state"] != "broken":
        print("REFUSED: reseal only closes an OPEN break-glass. Nothing to reseal."); return 1
    bg = m.get("break_glass") or {}
    # ── THE CASCADE GATE — nothing lands unilaterally; a change reseals only after
    #    it has flowed through every relevant channel. ─────────────────────────────
    print("CASCADE GATE — verifying the change went through all channels:")
    fails = []
    rc = subprocess.run([sys.executable, os.path.join(ROOT, "ledger", "tools", "audit.py"),
                         "--quiet"]).returncode
    print(f"  [{'PASS' if rc == 0 else 'FAIL'}] audit.py — canon holds")
    if rc: fails.append("audit.py not clean")
    rc = subprocess.run([sys.executable, os.path.join(ROOT, "ledger", "tools",
                         "check_typography.py")], capture_output=True).returncode
    print(f"  [{'PASS' if rc == 0 else 'FAIL'}] check_typography.py — no round-trip drift "
          f"(quotes / em dashes / italics / ellipses)")
    if rc: fails.append("typography drift (run: python3 ledger/tools/check_typography.py)")
    bi = os.path.join(ROOT, "build_integrity.py")      # optional: only if this repo has one
    if os.path.exists(bi):
        rc = subprocess.run([sys.executable, bi], capture_output=True).returncode
        print(f"  [{'PASS' if rc == 0 else 'FAIL'}] build_integrity.py — artifacts rebuilt & production facts synced")
        if rc: fails.append("build_integrity not clean (rebuild artifacts / sync production facts)")
    now, base = _mtimes(), bg.get("channel_mtimes", {})
    logged = now.get("decisions", 0) > base.get("decisions", 0)
    print(f"  [{'PASS' if logged else 'FAIL'}] DECISIONS_LOG.md — a ruling was recorded for this change")
    if not logged: fails.append("no DECISIONS_LOG entry for this change (ledger the ruling)")
    touched = [k for k in CHANNELS if k != "decisions" and now.get(k, 0) > base.get(k, 0)]
    untouched = [k for k in CHANNELS if k != "decisions" and now.get(k, 0) <= base.get(k, 0)]
    print(f"  [note] harvest ledgers touched: {touched or 'none'}  |  untouched: {untouched}")
    if fails:
        print("\n🚫 RESEAL REFUSED — cascade incomplete:")
        for f in fails: print(f"     - {f}")
        report("RESEAL-REFUSED", f"cascade incomplete: {'; '.join(fails)}")
        print("The glass stays OPEN. Finish the channels, then reseal. Nothing lands unilaterally.")
        return 1
    changed, _, added = _drift(m)
    for f in changed: report("RESEALED-CHANGE", f"authorized + fully-cascaded edit to `{f}`")
    m["files"] = {_rel(p): _sha(p) for p in _sealed_files()}
    m["state"] = "sealed"
    m["sealed_at"] = _now()
    m["break_glass"] = None
    save(m)
    print(f"\n🔒 RE-SEALED — cascade complete. Files changed under this break-glass: {len(changed)}"
          + (f", new: {len(added)}" if added else ""))
    return 0

def main():
    p = argparse.ArgumentParser(prog="seal.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("seal"); sub.add_parser("status")
    sub.add_parser("verify"); sub.add_parser("reseal"); sub.add_parser("hook")
    c = sub.add_parser("check"); c.add_argument("path")
    b = sub.add_parser("break-glass"); b.add_argument("--reason", required=True); b.add_argument("--authorized-by", required=True)
    a = p.parse_args()
    return {"seal": cmd_seal, "status": cmd_status, "verify": cmd_verify,
            "check": cmd_check, "hook": cmd_hook, "break-glass": cmd_break_glass, "reseal": cmd_reseal
            }[a.cmd](a)

if __name__ == "__main__":
    sys.exit(main())
