#!/usr/bin/env python3
"""Continuity Review Board — six-agent chapter reader. Spec: REVIEW_BOARD.md

  python3 board.py run  <book> <chapter>      # read one chapter, write minutes + review list
  python3 board.py rule <book> <chapter> <item_id> <FIX_PROSE|FIX_CANON|DISMISS|DEFER:chNN> [note]
  python3 board.py show <book> <chapter>      # print the review list
  python3 board.py run  <book> <chapter> --dry  # no API: print prompt sizes only

book = 1 | 2.  Ledgers live in ledgers/<lens>.yaml.  Requires ANTHROPIC_API_KEY (or `ant auth login`).
"""
import sys, json, re, pathlib, datetime, yaml

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LEDGERS = HERE / 'ledgers'; MINUTES = HERE / 'minutes'
MODEL = 'claude-opus-5'

SOURCES = {
    1: lambda n: ROOT / '6_manuscript/book_1/v1_1' / ('epilogue.txt' if n == 31 else f'chapter_{n:02d}.txt'),
    2: lambda n: ROOT / '6_manuscript/book_2' / f'chapter_{n:02d}.md',
}
BUILD = {1: 'book1 REVIEW v1.1', 2: 'book2 chapter_XX.md @HEAD'}

CANON = (ROOT / 'CLAUDE.md').read_text().split('## Canon Warnings')[1].split('## Key Reference Files')[0]
SPEC = (HERE / 'REVIEW_BOARD.md').read_text()
DIRECTORY = SPEC.split('## 4. Thread directory')[1].split('## 5. Ledger schema')[0]

LENSES = {
 'knowledge': "What each character KNOWS, believes, suspects, has been told, or wrongly believes. Include how they learned it. Never infer Ahdia's interior in Book 2; cite an action or a line spoken to her.",
 'body_ground': "Physical and spatial state: where each character is, injuries, fatigue, possessions, clothing, who is present in each scene. Objects changing hands.",
 'bonds': "Relationships, promises, debts, what others believe about a character, and which arc beat each character has reached.",
 'numbers': "Every measured value in the text: percentages, hours, days, counts, distances, doses, polling, ages. Record the value and direction of change. Entries without a numeric value are out of lane.",
 'chronicle': "Time and world: dates, elapsed time, time of day, season, news items, off-page world events, the news-seed checklist.",
}

def agent_system(lens):
    return f"""You are the {lens.upper()} registrar on a continuity review board for a novel manuscript. You have exactly one lens:
{LENSES[lens]}

Rules:
1. Every entry and every flag carries a cite of the form b<book>:ch<NN>:p<paragraph>:s<sentence>, counting paragraphs and sentences from the chapter text you are given (title line is p0). No cite, no entry.
2. Stay in lane. Ignore facts outside your lens; another registrar owns them.
3. Record facts as the text states them, even when they contradict canon or your ledger. Then FLAG the contradiction.
4. Do not invent. If the text is ambiguous, record the ambiguity as the fact.
5. Superseding: if a new fact replaces a ledger entry, set "supersedes" to that entry's id.
6. Output ONLY a JSON object: {{"delta": [entries], "flags": [flags]}}.
   entry = {{"subject": str, "fact": str, "value": str|null, "cite": str, "supersedes": str|null}}
   flag  = {{"severity": "HIGH|MED|LOW", "kind": "contradiction|canon_break|missing_seed|math|presence|ambiguity", "cites": [str], "says": str}}

CANON WARNINGS (outrank the text; a breach is a HIGH canon_break flag, not a ledger update):
{CANON}

THREAD DIRECTORY (what the Director wants tracked):
{DIRECTORY}"""

CHAIR_SYSTEM = f"""You are the BOARD CHAIR of a continuity review board. Five registrars (knowledge, body_ground, bonds, numbers, chronicle) have each filed a delta and flags for one chapter. Produce the Director's review list.

Enforcement, applied before anything else:
1. Strike any entry or flag with no cite. List what you struck.
2. Strike any entry outside its registrar's lane. List it.
3. A flag that re-raises a DISMISSED item id is dropped and logged.
4. An entry about Ahdia's interior in Book 2 is struck.
Then reconcile: find contradictions BETWEEN registrars' deltas and against their ledgers. Merge duplicate flags. Rank by severity.
Output ONLY JSON: {{"struck": [str], "review": [{{"id": "R-<chapter>-<n>", "severity": "HIGH|MED|LOW", "kind": str, "cites": [str], "says": str, "options": "one line on what a fix would be"}}]}}
Keep "says" concrete: name the two things that disagree, quote the words.

CANON WARNINGS:
{CANON}"""

def load_ledger(lens):
    p = LEDGERS / f'{lens}.yaml'
    return yaml.safe_load(p.read_text()) if p.exists() else {'entries': [], 'flags': []}

def save_ledger(lens, d): (LEDGERS / f'{lens}.yaml').write_text(yaml.safe_dump(d, sort_keys=False, allow_unicode=True))

def rulings_log():
    p = LEDGERS / 'rulings.yaml'
    return yaml.safe_load(p.read_text()) if p.exists() else []

def chapter_text(book, n):
    p = SOURCES[book](n)
    t = p.read_text()
    paras = [x for x in re.split(r'\n\s*\n|\n', t) if x.strip() and not x.startswith('<!--') and not x.startswith('**Rolls:**')]
    return '\n'.join(f'[p{i}] {x.strip()}' for i, x in enumerate(paras))

def call(client, system, user, max_tokens=16000):
    with client.messages.stream(
        model=MODEL, max_tokens=max_tokens,
        system=[{'type': 'text', 'text': system, 'cache_control': {'type': 'ephemeral'}}],
        messages=[{'role': 'user', 'content': user}],
    ) as s:
        msg = s.get_final_message()
    if msg.stop_reason == 'refusal':
        raise SystemExit(f'refusal: {getattr(msg, "stop_details", None)}')
    text = ''.join(b.text for b in msg.content if b.type == 'text')
    m = re.search(r'\{.*\}', text, re.S)
    return json.loads(m.group(0)) if m else {'error': text}, msg.usage

def run(book, n, dry=False):
    ch = chapter_text(book, n)
    tag = f'b{book}_ch{n:02d}'
    rulings = rulings_log()
    reports, usage = {}, []
    client = None
    if not dry:
        import anthropic; client = anthropic.Anthropic()
    for lens in LENSES:
        led = load_ledger(lens)
        user = [
            {'type': 'text', 'text': f'YOUR LEDGER SO FAR (build tags in each entry):\n{yaml.safe_dump(led, sort_keys=False, allow_unicode=True)}\n\nDIRECTOR RULINGS LOG:\n{yaml.safe_dump(rulings, allow_unicode=True)}'},
            {'type': 'text', 'text': f'CHAPTER TEXT (book {book}, chapter {n}, build {BUILD[book]}):\n{ch}', 'cache_control': {'type': 'ephemeral'}},
            {'type': 'text', 'text': f'File your delta and flags for book {book} chapter {n}.'},
        ]
        if dry:
            print(f'{lens:12} system ~{len(agent_system(lens))//4:>6} tok  user ~{sum(len(u["text"]) for u in user)//4:>6} tok'); continue
        out, u = call(client, agent_system(lens), user); usage.append(u)
        reports[lens] = out
        for e in out.get('delta', []):
            e.update({'id': f'{lens[0].upper()}-{len(led["entries"])+1:04d}', 'chapter': tag, 'build': BUILD[book], 'status': 'active'})
            led['entries'].append(e)
        led['flags'] += [dict(f, chapter=tag) for f in out.get('flags', [])]
        save_ledger(lens, led)
        print(f'{lens:12} +{len(out.get("delta", []))} entries, {len(out.get("flags", []))} flags')
    if dry:
        print(f'chapter text ~{len(ch)//4} tok'); return
    chair_user = [{'type': 'text', 'text': f'CHAPTER {tag}\n\nREGISTRAR REPORTS:\n{json.dumps(reports, indent=1, ensure_ascii=False)}\n\nDISMISSED IDS:\n{[r["item"] for r in rulings if r["ruling"]=="DISMISS"]}'}]
    review, u = call(client, CHAIR_SYSTEM, chair_user); usage.append(u)
    (MINUTES / f'{tag}.json').write_text(json.dumps({'reports': reports, 'review': review}, indent=1, ensure_ascii=False))
    md = [f'# Board minutes {tag}  ({datetime.date.today()}, {BUILD[book]})', '']
    for r in review.get('review', []):
        md.append(f'- **{r["id"]}** [{r["severity"]}/{r["kind"]}] {r["says"]}  \n  cites: {", ".join(r["cites"])}  \n  fix: {r.get("options","")}')
    md += ['', '## Struck by Chair'] + [f'- {s}' for s in review.get('struck', [])]
    tin = sum(x.input_tokens for x in usage); tcr = sum(x.cache_read_input_tokens or 0 for x in usage); tout = sum(x.output_tokens for x in usage)
    md += ['', f'usage: in {tin} (cache read {tcr}) out {tout}']
    (MINUTES / f'{tag}.md').write_text('\n'.join(md))
    print('\n'.join(md))

def rule(book, n, item, ruling, note=''):
    log = rulings_log()
    log.append({'item': item, 'chapter': f'b{book}_ch{n:02d}', 'ruling': ruling, 'note': note, 'date': str(datetime.date.today())})
    (LEDGERS / 'rulings.yaml').write_text(yaml.safe_dump(log, allow_unicode=True))
    print('recorded', item, ruling)

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] not in ('run', 'rule', 'show'): print(__doc__); sys.exit(1)
    book, n = int(a[1]), int(a[2])
    if a[0] == 'run': run(book, n, dry='--dry' in a)
    elif a[0] == 'rule': rule(book, n, a[3], a[4], ' '.join(a[5:]))
    else: print((MINUTES / f'b{book}_ch{n:02d}.md').read_text())
