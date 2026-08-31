from pathlib import Path
import re


def replace_once(text, old, new, label):
    n = text.count(old)
    assert n == 1, f'{label}: expected 1 occurrence, found {n}'
    return text.replace(old, new, 1)


manuscript = Path('state/manuscript/Peg_Leg_Greg_Running_Manuscript.md').read_text()
assert '# CHAPTER 230' in manuscript and '## THE REPLICATE' in manuscript

p = Path('state/MANUSCRIPT_STATE.md')
s = p.read_text()
s = replace_once(s, '- Current story endpoint: Chapter 229 — **THE ROAD ONE**.', '- Current story endpoint: Chapter 230 — **THE REPLICATE**.', 'manuscript endpoint')
magic = '''## Current magic continuity
- 33 successful supervised minimal draws.
- 29 supervised deliberate shaping attempts.
- 45 supervised external-effect attempts.
- Attempt 38 FAR/AWAY: no observed response; control unchanged.
- Attempt 39 INTERMEDIATE/AWAY: small observed target response, net AWAY, minor rotation; control unchanged.
- Attempt 40 FAR/AWAY: target movement observed and control movement observed; contaminated for target-specific interpretation; cause not established; no target-specific response counted.
- Attempt 41 INTERMEDIATE/AWAY: small observed target response, net AWAY, no obvious rotation; control unchanged.
- Ch226 used predeclared order FAR → INTERMEDIATE → FAR → INTERMEDIATE.
- Ch230 reverses that predeclared order while preserving the same room, board, glass shield, paper-fin target/control, INTERMEDIATE/FAR marks, body geometry, and AWAY-only direction: INTERMEDIATE → FAR → INTERMEDIATE → FAR.
- Attempt 42 INTERMEDIATE/AWAY: small observed target response, net AWAY; control unchanged.
- Attempt 43 FAR/AWAY: no observed response; control unchanged.
- Attempt 44 INTERMEDIATE/AWAY: no observed response; control unchanged.
- Attempt 45 FAR/AWAY: no observed response; control unchanged.
- All four Ch230 external attempts are clean for apparatus/control interpretation: no control movement and no apparatus disturbance observed.
- INTERMEDIATE has now produced clean observed target response across more than one session under the current apparatus, but Attempt 44 establishes that INTERMEDIATE response is not reliable.
- INTERMEDIATE continues to produce clean observed response more consistently than FAR under the current apparatus.
- FAR response remains established as having occurred cleanly in earlier sessions, but FAR reliability remains unestablished. Attempts 43 and 45 do not strengthen FAR-response evidence.
- Reversing the order does not establish an order effect; the two four-condition sessions simply provide different recorded outcomes under opposite starting conditions.
- Distance dependence remains supported in the current apparatus.
- NO RANGE ESTABLISHED. NOT GENERALIZED.
- Restrictions unchanged: no independent draw, shaping, external testing, paper, coins, thread, larger objects, practice, Barrier broadening, theatrical magic, or loopholes.
- Hessa ends Ch230 with no chosen next experiment. She still has several questions; asked whether there are more or fewer, she says `Different`.

## Greg / Lyssa'''
s, n = re.subn(r'## Current magic continuity\n.*?\n## Greg / Lyssa', magic, s, count=1, flags=re.S)
assert n == 1, 'magic block replacement failed'
s = replace_once(
    s,
    "- Lyssa understands the control logic quickly from Ch226 but remains independent of Hessa's domain.",
    "- Ch230 Lyssa is off-page through the experiment day, later returns with turnips and no garment, and asks only narrow questions about the paper result and whether the rules changed. A narrow folded brown cloth with three pins appears at home; customer, garment, ownership, and use are unestablished.\n- Greg's poor shirt-cuff repair worsens from two loose threads to three; he deliberately does not repair it again. No clothing subplot is required.\n- Lyssa understands the control logic quickly from Ch226 but remains independent of Hessa's domain.",
    'Greg Lyssa Ch230',
)
s = replace_once(
    s,
    '- Ch229 contains no Vale appearance or debt credit. Greg buys ordinary bread and cheese while the debt remains active and unstated.',
    '- Ch229 contains no Vale appearance or debt credit. Greg buys ordinary bread and cheese while the debt remains active and unstated.\n- Ch230 contains no Vale appearance, debt payment, or debt credit. Greg buys one ordinary meat pie and otherwise leaves the debt active and unstated.',
    'economy Ch230',
)
s = replace_once(
    s,
    "- Chapters 224–229 do not advance the pressure arc. In Ch228 Olin simply sends the theatre's oil with no message, question, warning, or stranger attached. Bren remains off-page. No Mason's Cut investigation and no Vale-paper clue.",
    "- Chapters 224–230 do not advance the pressure arc. In Ch228 Olin simply sends the theatre's oil with no message, question, warning, or stranger attached. Bren remains off-page. No Mason's Cut investigation and no Vale-paper clue.",
    'pressure through 230',
)
ch230 = '''## Chapter 230 — THE REPLICATE
- Hessa returns after three full breathing chapters with one bounded question rather than a power-up: whether the apparent INTERMEDIATE/FAR difference remains under the same four-condition structure when the predeclared order is reversed.
- Greg deliberately keeps the morning light, eats before the session, and does no theatre or Vale work. No threat fact appears.
- Same apparatus and restrictions are preserved. Entering counts are 32 minimal / 28 deliberate shaping / 41 external.
- One supervised minimal draw succeeds cleanly, bringing the count to 33.
- One supervised deliberate shaping attempt succeeds cleanly, bringing the count to 29.
- Predeclared external order is INTERMEDIATE → FAR → INTERMEDIATE → FAR, AWAY only.
- Attempt 42 INTERMEDIATE/AWAY: clean small target response, net AWAY; control unchanged.
- Attempt 43 FAR/AWAY: no observed response; control unchanged.
- Planned break follows the first two external attempts. Greg has ordinary sitting stiffness/worked shoulders only; no pain, weakness, tingling, residual-limb issue, or reason to stop.
- Attempt 44 INTERMEDIATE/AWAY: no observed response; control unchanged. Greg notices the urge to increase effort because he expects the condition to work and does not act on it.
- Attempt 45 FAR/AWAY: no observed response; control unchanged.
- Session conclusion remains narrow: INTERMEDIATE response has now repeated across sessions, but is not reliable; FAR reliability remains unestablished; reversing order does not establish an order effect; no range; not generalized; restrictions unchanged.
- Final counts: 33 supervised minimal draws / 29 deliberate shaping attempts / 45 external-effect attempts.
- Hessa has no chosen next experiment. Her possible questions are `Different`, not resolved into a ladder.
- Home: an undefined narrow brown cloth with three pins is present while Lyssa is elsewhere. She later returns with turnips and no garment, asks only narrow evidence/rules questions, and does not become Hessa's co-analyst.
- Greg's bad shirt-cuff repair reaches three loose threads; he leaves it alone.
- Final beat stays domestic and comic: Greg oversalts the turnip, Lyssa moves the bowl away, and nobody records the result.

'''
marker = '## Immediate next edge — Chapter 230\n'
assert marker in s and '## Chapter 230 — THE REPLICATE' not in s
s = s.replace(marker, ch230 + marker, 1)
edge = '''## Immediate next edge — Chapter 231
Primary recommendation: **LET THE CH230 MAGIC SESSION BREATHE. CHOOSE THE NEXT ENGINE FROM ACTUAL DAILY PRESSURE, NOT A ROTATION QUOTA.**

Reasons:
- Ch230 answers only a narrow replication/order question and explicitly leaves Hessa with different unresolved questions; another immediate experiment would begin to feel like a test ladder;
- Lyssa's work ecology remains independent and mostly off-page in Ch230. The new narrow brown cloth is intentionally undefined and does not require servicing;
- theatre has had only compact labor since the full Ch228 performance, so ordinary theatre work, rehearsal, or a role is available without needing another major performance chapter;
- Vale has now rested through Chapters 228–230. Suitable work may recur if the day gives Greg a reason to seek it, but no employment schedule exists;
- external pressure remains quiet through Chapter 230. One grounded new fact may move it, but seven quiet chapters do not create an escalation quota;
- ordinary Carrow, money, friendship/company life, household rhythm, and bodily work remain valid engines in their own right.

Strong Chapter 231 possibilities:
- ordinary theatre/company work that advances belonging or repertory life without making Ch230's magic useful;
- a Vale or money day if Greg has a concrete reason to seek suitable work;
- one grounded external-pressure fact through an existing commercial contact, only if exact current authority earns it;
- another ordinary city/work/social day that lets both magic and Lyssa's returned work node breathe.

Preserve 33 / 29 / 45 as entering magic counts. Do not answer the order question more strongly than Ch230 supports. Do not resolve the brown cloth or cuff merely because they exist.

## Chat / handoff behavior'''
s, n = re.subn(r'## Immediate next edge — Chapter 230\n.*?\n## Chat / handoff behavior', edge, s, count=1, flags=re.S)
assert n == 1, 'next edge replacement failed'
p.write_text(s)

p = Path('state/OPEN_THREADS.md')
o = p.read_text()
o = replace_once(o, '- **Current endpoint:** Chapter 229 — **THE ROAD ONE**.', '- **Current endpoint:** Chapter 230 — **THE REPLICATE**.', 'open endpoint')
o, n = re.subn(r'^- \*\*Magic counts:\*\*.*$', '- **Magic counts:** ACTIVE at 33 supervised minimal draws / 29 deliberate shaping attempts / 45 external-effect attempts.', o, count=1, flags=re.M)
assert n == 1
o, n = re.subn(r'^- \*\*Latest comparison protocol:\*\*.*$', '- **Latest comparison protocol:** Ch230 predeclares INTERMEDIATE → FAR → INTERMEDIATE → FAR, AWAY only, preserving the same target/control/glass/body setup and the same INTERMEDIATE/FAR marks as Ch226.', o, count=1, flags=re.M)
assert n == 1
anchor = '- **Attempt 41:** INTERMEDIATE/AWAY, small observed target response, net AWAY, no obvious rotation, control unchanged.\n'
assert anchor in o and '- **Attempt 42:**' not in o
o = o.replace(anchor, anchor + '- **Attempt 42:** INTERMEDIATE/AWAY, small observed target response, net AWAY, control unchanged.\n- **Attempt 43:** FAR/AWAY, no observed response, control unchanged.\n- **Attempt 44:** INTERMEDIATE/AWAY, no observed response, control unchanged.\n- **Attempt 45:** FAR/AWAY, no observed response, control unchanged.\n', 1)
o, n = re.subn(r'^- \*\*Current distance interpretation:\*\*.*$', "- **Current distance interpretation:** INTERMEDIATE has now produced clean observed response across more than one session under the current apparatus, but Attempt 44 shows it is not reliable. INTERMEDIATE still produces clean response more consistently than FAR. Earlier clean FAR responses remain real; FAR reliability remains unestablished. Ch230's reversed order does not establish an order effect. No range established. Not generalized.", o, count=1, flags=re.M)
assert n == 1
o, n = re.subn(r'^- \*\*Next magic question:\*\*.*$', '- **Next magic question:** Hessa still has several possibilities after Ch230 and has chosen none; when Greg asks whether there are more or fewer, she says `Different`. Do not convert this into a test ladder.', o, count=1, flags=re.M)
assert n == 1
o = o.replace('**Threat restraint:** Chapters 224–229', '**Threat restraint:** Chapters 224–230')
o = o.replace('Chapters 228–229 have no Vale movement.', 'Chapters 228–230 have no Vale movement.')
o, n = re.subn(r'^- \*\*Next engine rotation:\*\*.*$', '- **Next engine rotation:** let Ch230 magic breathe. Theatre, Vale/money, ordinary Carrow/social life, or one genuinely grounded pressure fact are available; none is owed on a timer.', o, count=1, flags=re.M)
assert n == 1
insert = "- **Ch230 Hessa replication:** reversed predeclared order yields one clean INTERMEDIATE response, one clean INTERMEDIATE non-response, and two clean FAR non-responses. Counts end 33 / 29 / 45; restrictions unchanged.\n- **Ch230 household residue:** a narrow folded brown cloth with three pins appears at home; customer/garment/ownership/use remain unknown. Greg's bad cuff repair reaches three loose threads and he leaves it alone. Lyssa returns with turnips and no garment.\n"
anchor2 = '- **Magic restrictions:** unchanged. No independent draw, shaping, external testing, paper, coins, thread, larger objects, practice, Barrier broadening, theatrical magic, or loopholes.\n'
assert anchor2 in o and '- **Ch230 Hessa replication:**' not in o
o = o.replace(anchor2, anchor2 + insert, 1)
p.write_text(o)

p = Path('state/MANUSCRIPT_CHAPTER_INDEX.md')
i = p.read_text()
i = replace_once(i, '# PEG-LEG GREG — CHAPTER INDEX — CH229', '# PEG-LEG GREG — CHAPTER INDEX — CH230', 'index heading')
i = replace_once(i, '**Current endpoint:** Chapter 229 — THE ROAD ONE', '**Current endpoint:** Chapter 230 — THE REPLICATE', 'index endpoint')
assert '230. **THE REPLICATE**' not in i
assert i.rstrip().endswith('229. **THE ROAD ONE**')
i = i.rstrip() + '\n230. **THE REPLICATE**\n'
p.write_text(i)

p = Path('state/MANUSCRIPT_WORKFLOW.md')
w = p.read_text()
w = replace_once(w, 'Chapter 229 — **THE ROAD ONE**.', 'Chapter 230 — **THE REPLICATE**.', 'workflow edge')
w = replace_once(w, 'See `state/MANUSCRIPT_STATE.md` for current canon and the Chapter 230 edge.', 'See `state/MANUSCRIPT_STATE.md` for current canon and the Chapter 231 edge.', 'workflow next')
p.write_text(w)

p = Path('state/PROJECT_STATE.md')
ps = p.read_text()
ps = replace_once(ps, 'Current recorded story endpoint is Chapter 229 — **THE ROAD ONE**.', 'Current recorded story endpoint is Chapter 230 — **THE REPLICATE**.', 'project endpoint')
p.write_text(ps)
