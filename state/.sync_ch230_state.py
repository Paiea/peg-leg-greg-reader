from pathlib import Path


def replace_once(text, old, new, label):
    count = text.count(old)
    assert count == 1, f"{label}: expected 1 match, got {count}"
    return text.replace(old, new, 1)

# MANUSCRIPT_STATE
p = Path('state/MANUSCRIPT_STATE.md')
text = p.read_text()
text = replace_once(text, '- Current story endpoint: Chapter 229 — **THE ROAD ONE**.', '- Current story endpoint: Chapter 230 — **THE REPLICATE**.', 'manuscript endpoint')
start = text.index('## Current magic continuity\n')
end = text.index('\n## Greg / Lyssa\n', start)
magic = '''## Current magic continuity
- 33 successful supervised minimal draws.
- 29 supervised deliberate shaping attempts.
- 45 supervised external-effect attempts.
- Attempt 38 FAR/AWAY: no observed response; control unchanged.
- Attempt 39 INTERMEDIATE/AWAY: small observed target response, net AWAY, minor rotation; control unchanged.
- Attempt 40 FAR/AWAY: target movement observed and control movement observed; contaminated for target-specific interpretation; cause not established; no target-specific response counted.
- Attempt 41 INTERMEDIATE/AWAY: small observed target response, net AWAY, no obvious rotation; control unchanged.
- Ch226 used the predeclared order FAR → INTERMEDIATE → FAR → INTERMEDIATE, AWAY only, same target/control/glass/body setup.
- Ch230 deliberately reverses that four-condition order to INTERMEDIATE → FAR → INTERMEDIATE → FAR while preserving the same marks, target/control, glass, direction, room, and body geometry as closely as practical.
- Attempt 42 INTERMEDIATE/AWAY: small observed target response with net displacement away; control unchanged.
- Attempt 43 FAR/AWAY: no observed response; control unchanged.
- Attempt 44 INTERMEDIATE/AWAY: no observed response; control unchanged. Greg explicitly expected it to move and noticed the urge to increase effort without acting on that urge.
- Attempt 45 FAR/AWAY: no observed response; control unchanged.
- All four Ch230 external attempts are clean for apparatus/control interpretation: no control movement, no apparatus disturbance, and no body change large enough to stop the session.
- Across the current apparatus record, INTERMEDIATE has produced more clean observed responses than FAR across more than one session, so the apparent INTERMEDIATE/FAR response-frequency difference remains supported.
- INTERMEDIATE response is **not reliable**: Ch230 includes one clean INTERMEDIATE response and one clean INTERMEDIATE no-response in the same session.
- Earlier clean FAR responses from prior sessions remain real; Ch230's two FAR no-responses do not erase them and do not strengthen FAR reliability.
- Reversing the alternating order does not establish whether order matters. There is now one session beginning FAR and one beginning INTERMEDIATE under the same four-condition structure, with different results.
- NO RANGE ESTABLISHED. NOT GENERALIZED.
- Restrictions unchanged: no independent draw, shaping, external testing, paper, coins, thread, larger objects, practice, Barrier broadening, theatrical magic, or loopholes.
- Hessa ends Ch230 with several possible next questions still unchosen. Asked whether there are more or fewer, she says `Different.` No next experiment is established.
'''
text = text[:start] + magic + text[end:]
text = replace_once(text,
    '- Ch229 the blue-gray cloth is established only as cloth Lyssa asks Greg to carry to Marra; Jessa finds two short chalk marks near its edge and calls it `Marked`, but customer, garment, use, and ownership remain unknown. Lyssa later works on the north side and Jessa finds her independently.\n- Lyssa understands the control logic quickly from Ch226 but remains independent of Hessa\'s domain.',
    '- Ch229 the blue-gray cloth is established only as cloth Lyssa asks Greg to carry to Marra; Jessa finds two short chalk marks near its edge and calls it `Marked`, but customer, garment, use, and ownership remain unknown. Lyssa later works on the north side and Jessa finds her independently.\n- Ch230 lets that work ecology breathe. Lyssa is already out in the morning; no Marra/Jessa/customer callback occurs. By evening a narrow folded brown piece with three pins is on the table, but its customer, garment, ownership, and use remain unknown. Lyssa returns carrying turnips and no garment.\n- Greg\'s poor shirt-cuff repair progresses from two loose threads to three. He notices and deliberately does not repair it; no clothing subplot or Lyssa rescue is required.\n- Lyssa asks narrow human questions about the Ch230 session (`Paper?`, how many, which distance moved, rules) but does not pretend to own Hessa\'s interpretation or produce a larger conclusion.\n- Lyssa understands the control logic quickly from Ch226 but remains independent of Hessa\'s domain.',
    'Greg/Lyssa ch230')
text = replace_once(text,
    '- Ch229 contains no Vale appearance or debt credit. Greg buys ordinary bread and cheese while the debt remains active and unstated.\n- No Vale/Bren connection established.',
    '- Ch229 contains no Vale appearance or debt credit. Greg buys ordinary bread and cheese while the debt remains active and unstated.\n- Ch230 contains no Vale appearance, office work, payment, or debt credit. Greg buys a meat pie in advance of Hessa\'s session; ordinary food spending coexists with the unresolved debt.\n- No Vale/Bren connection established.',
    'economy ch230')
text = replace_once(text, '- Chapters 224–229 do not advance the pressure arc.', '- Chapters 224–230 do not advance the pressure arc.', 'pressure through 230')
edge_start = text.index('## Immediate next edge — Chapter 230\n')
edge_end = text.index('\n## Chat / handoff behavior\n', edge_start)
new_edge = '''## Chapter 230 — THE REPLICATE
- Full Hessa / controlled-evidence chapter after three chapters of magic breathing room. No theatre work/role, no Vale work/debt credit, no Bren/brown-coat/threat movement, and no Marra/Jessa/customer callback.
- Hessa's note requires `AFTER MIDDAY / SAME ROOM / EAT / LIGHT MORNING`. Greg treats `Jori said maybe` as not a call, does not volunteer for Vale work, buys/eats a meat pie, and arrives with an intentionally light physical morning.
- Apparatus remains the established same room, chair/floor marks, board, glass shield, paper-fin target/control, INTERMEDIATE and FAR marks, AWAY only.
- Hessa predeclares the reversed alternating order **INTERMEDIATE → FAR → INTERMEDIATE → FAR**, specifically giving INTERMEDIATE the first/third positions after Ch226 gave it second/fourth.
- One supervised minimal draw succeeds cleanly, bringing the count to **33**. One supervised deliberate shaping attempt completes cleanly, bringing the count to **29**.
- Attempt 42 INTERMEDIATE/AWAY: small clean target response, net away, control unchanged.
- Attempt 43 FAR/AWAY: no observed response, control unchanged.
- Attempt 44 INTERMEDIATE/AWAY: no observed response, control unchanged. Greg expected response and notices but resists an urge to increase effort.
- Attempt 45 FAR/AWAY: no observed response, control unchanged.
- Session ends at **33 / 29 / 45**. INTERMEDIATE still has more clean observed responses than FAR under the current apparatus across multiple sessions, but INTERMEDIATE is explicitly **not reliable** because it also fails cleanly in Ch230.
- Reversing order does not establish an order effect; the two alternating sessions now have different results. Earlier clean FAR responses remain real, FAR reliability remains unestablished, no range is established, and nothing is generalized.
- Restrictions remain completely unchanged.
- Hessa still has several possible questions, but after the new record she calls them `Different`; next experiment remains undecided.
- Home: a narrow folded brown piece with three pins appears without explanation. Greg's bad cuff worsens to three loose threads and he leaves it alone. Lyssa returns with turnips, asks only the narrow session/rules questions, and gives no grand interpretation. Greg oversalts the food; final line: `No one recorded the result.`

## Immediate next edge — Chapter 231
Primary recommendation: **LET MAGIC BREATHE AFTER THE FULL CH230 REPLICATION SESSION. RETURN TO ORDINARY PEOPLE / WORK / CITY LIFE, WITH THEATRE A STRONG AVAILABLE ENGINE IF THE DAY OFFERS REAL WORK.**

Reasons:
- Ch230 materially changes the magic record and is already a full experimental chapter; another immediate Hessa session would risk turning evidence into a procedural ladder.
- Theatre last received a full performance in Ch228, only compact window-trim work in Ch229, and no movement in Ch230. It is available for rehearsal, performance, backstage labor, social friction, or ordinary company work without needing to serve future bluff utility.
- Vale has not foregrounded since Ch227. Suitable work may recur if naturally available, but Greg does not have a guaranteed job or scheduled rotation.
- External pressure has remained quiet through Ch224–230. One grounded fact through an existing commercial/social contact can move the thread if earned; quiet chapters do not create an escalation quota.
- Lyssa/Marra/Jessa were foregrounded in Ch229 and deliberately rested in Ch230. Their work can continue off-page; the new brown pinned cloth and prior blue-gray cloth remain intentionally undefined unless a present scene needs them.
- Ordinary Carrow relationships, food, money, errands, bodies, theatre people, and partial reputations remain valid primary engines.

Do not mechanically rotate to the oldest untouched engine. Choose the actual next-day pressure that creates the most life per word while preserving the new magic ceiling.
'''
text = text[:edge_start] + new_edge + text[edge_end:]
p.write_text(text)

# OPEN_THREADS
p = Path('state/OPEN_THREADS.md')
text = p.read_text()
text = replace_once(text, '- **Current endpoint:** Chapter 229 — **THE ROAD ONE**.', '- **Current endpoint:** Chapter 230 — **THE REPLICATE**.', 'threads endpoint')
text = replace_once(text,
    '- **Magic counts:** ACTIVE at 32 supervised minimal draws / 28 deliberate shaping attempts / 41 external-effect attempts. Chapters 227–229 contain no magic attempt.\n- **Latest comparison protocol:** Ch226 predeclares FAR → INTERMEDIATE → FAR → INTERMEDIATE, AWAY only, same target/control/glass/body setup.',
    '- **Magic counts:** ACTIVE at **33 supervised minimal draws / 29 deliberate shaping attempts / 45 external-effect attempts**.\n- **Ch226 comparison protocol:** predeclared FAR → INTERMEDIATE → FAR → INTERMEDIATE, AWAY only, same target/control/glass/body setup.\n- **Ch230 replication protocol:** predeclared reversed order INTERMEDIATE → FAR → INTERMEDIATE → FAR, AWAY only, same marks/target/control/glass/room/body geometry as closely as practical.',
    'threads protocol')
text = replace_once(text,
    '- **Attempt 41:** INTERMEDIATE/AWAY, small observed target response, net AWAY, no obvious rotation, control unchanged.\n- **Current distance interpretation:** the apparent INTERMEDIATE/FAR difference remains supported under the current apparatus. INTERMEDIATE continues to produce observed response more consistently than FAR. Earlier clean FAR responses across separate sessions remain real, but FAR reliability is unestablished. Attempt 40 does not strengthen FAR-response evidence. No range established. Not generalized.\n- **Magic restrictions:** unchanged. No independent draw, shaping, external testing, paper, coins, thread, larger objects, practice, Barrier broadening, theatrical magic, or loopholes.\n- **Next magic question:** Hessa says she has several possible questions but has not chosen one because the record changed. Chapters 227–229 let this remain unresolved. Do not convert it into a test ladder.',
    '- **Attempt 41:** INTERMEDIATE/AWAY, small observed target response, net AWAY, no obvious rotation, control unchanged.\n- **Attempt 42:** INTERMEDIATE/AWAY, small observed target response, net AWAY, control unchanged.\n- **Attempt 43:** FAR/AWAY, no observed response, control unchanged.\n- **Attempt 44:** INTERMEDIATE/AWAY, no observed response, control unchanged; Greg expected response and resisted an urge to increase effort.\n- **Attempt 45:** FAR/AWAY, no observed response, control unchanged.\n- **Current distance interpretation:** the apparent INTERMEDIATE/FAR response-frequency difference remains supported under the current apparatus across more than one session because INTERMEDIATE has produced more clean observed responses than FAR. INTERMEDIATE is **not reliable**; Ch230 contains one clean response and one clean no-response at INTERMEDIATE. Earlier clean FAR responses remain real, but FAR reliability remains unestablished. Reversing the alternating order did not establish whether order matters. No range established. Not generalized.\n- **Magic restrictions:** unchanged. No independent draw, shaping, external testing, paper, coins, thread, larger objects, practice, Barrier broadening, theatrical magic, or loopholes.\n- **Next magic question:** Hessa still has several possible questions after Ch230; when Greg asks whether there are more or fewer, she says `Different.` No next experiment is chosen. Do not convert this into a test ladder.',
    'threads attempts')
text = replace_once(text, '- **Crutch maintenance:** one worn LEFT tip replaced Ch223; it remains normal through Ch229.', '- **Crutch maintenance:** one worn LEFT tip replaced Ch223; it remains normal through Ch230.', 'threads crutch')
text = replace_once(text,
    '- **Body:** Ch228 the side of Greg\'s right palm/right hand becomes ordinarily worked from long flowers, props, baskets, crutches, and carrying. He redistributes load during reset. Ch229 it is normal again. No pain, weakness, tingling, residual-limb issue, or injury.',
    '- **Body:** Ch228 the side of Greg\'s right palm/right hand becomes ordinarily worked from long flowers, props, baskets, crutches, and carrying. Ch229 it is normal again. Ch230 uses an intentionally light morning; planned experimental breaks manage ordinary forearm warmth/right-leg stiffness, with no pain, weakness, tingling, residual-limb issue, or injury.',
    'threads body')
text = replace_once(text, '- **Threat restraint:** Chapters 224–229 contain no new warning, demand, appearance, violence, sabotage, or investigation.', '- **Threat restraint:** Chapters 224–230 contain no new warning, demand, appearance, violence, sabotage, or investigation.', 'threads threat')
text = replace_once(text, '- **Vale debt:** ACTIVE. Exact balance known in-world but unstated. One-copper payment made Ch218. Ch224 suitable invoice/tally work produces legitimate credit. Ch227 different suitable office work produces another legitimate credit. Chapters 228–229 have no Vale movement. Debt remains unresolved.', '- **Vale debt:** ACTIVE. Exact balance known in-world but unstated. One-copper payment made Ch218. Ch224 suitable invoice/tally work produces legitimate credit. Ch227 different suitable office work produces another legitimate credit. Chapters 228–230 have no Vale movement. Debt remains unresolved.', 'threads Vale')
text = replace_once(text,
    '- **Next engine rotation:** let the Ch229 Lyssa/Marra/Jessa work-network chapter breathe. Hessa may return after three breathing chapters if she has a genuinely bounded next question, but not on a timer. External pressure may move with one grounded fact, but six quiet chapters do not create an escalation quota. Vale and another full performance remain available without becoming automatic.',
    '- **Next engine rotation:** Ch230 is a full Hessa replication session and materially changes the magic record, so let magic breathe. Theatre is available after no theatre movement in Ch230 and only compact work in Ch229; Vale, ordinary city/social life, or one grounded pressure fact are also available without becoming a scheduled rotation.',
    'threads rotation')
insert_anchor = '- **Ch229 household:** Lyssa\'s prior tiredness remains ordinary, not injury. Greg\'s Ch228 worked palm is normal. The chapter ends with the table used only for shared supper, with no active cloth/customer on it.\n'
insert = insert_anchor + '- **Ch230 Hessa replication:** same apparatus and AWAY direction; reversed predeclared order INTERMEDIATE → FAR → INTERMEDIATE → FAR. Results 42 response / 43 no response / 44 no response / 45 no response, all with unchanged control. Counts end **33 / 29 / 45**. INTERMEDIATE remains more responsive on current evidence but is not reliable; no range/generalization and no permission change.\n- **Ch230 expectation control:** before Attempt 44 Greg explicitly says he expects the INTERMEDIATE target to move, then notices and resists the urge to increase effort when it does not. Preserve this as evidence-discipline behavior, not a new magic ability.\n- **Ch230 Lyssa/work:** no Marra/Jessa/customer callback. By evening a narrow folded brown piece with three pins is on the table; customer, garment, ownership, and use are unknown. Lyssa returns carrying turnips and no garment.\n- **Ch230 cuff:** Greg\'s poor shirt repair worsens from two loose threads to three. He deliberately leaves it alone; no forced repair callback.\n- **Ch230 final beat:** Lyssa asks narrow session/rules questions but makes no larger interpretation; Greg oversalts turnip and she moves the bowl. `No one recorded the result.`\n'
text = replace_once(text, insert_anchor, insert, 'threads ch230 insert')
p.write_text(text)

# CHAPTER INDEX
p = Path('state/MANUSCRIPT_CHAPTER_INDEX.md')
text = p.read_text()
text = replace_once(text, '# PEG-LEG GREG — CHAPTER INDEX — CH229', '# PEG-LEG GREG — CHAPTER INDEX — CH230', 'index header')
text = replace_once(text, '**Current endpoint:** Chapter 229 — THE ROAD ONE', '**Current endpoint:** Chapter 230 — THE REPLICATE', 'index endpoint')
assert text.rstrip().endswith('229. **THE ROAD ONE**'), 'index unexpected tail'
text = text.rstrip() + '\n230. **THE REPLICATE**\n'
p.write_text(text)

# MANUSCRIPT WORKFLOW
p = Path('state/MANUSCRIPT_WORKFLOW.md')
text = p.read_text()
text = replace_once(text, 'Chapter 229 — **THE ROAD ONE**.\n\nSee `state/MANUSCRIPT_STATE.md` for current canon and the Chapter 230 edge.', 'Chapter 230 — **THE REPLICATE**.\n\nSee `state/MANUSCRIPT_STATE.md` for current canon and the Chapter 231 edge.', 'workflow edge')
p.write_text(text)

# PROJECT STATE: endpoint only; leave development lane ownership untouched.
p = Path('state/PROJECT_STATE.md')
text = p.read_text()
text = replace_once(text, 'Current recorded story endpoint is Chapter 229 — **THE ROAD ONE**.', 'Current recorded story endpoint is Chapter 230 — **THE REPLICATE**.', 'project endpoint')
p.write_text(text)

print('sync_ch230_state: prepared 5 files')
