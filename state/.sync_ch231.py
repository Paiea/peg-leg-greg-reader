from pathlib import Path
import re


def replace_once(text, old, new, label):
    count = text.count(old)
    assert count == 1, f'{label}: expected 1 occurrence, found {count}'
    return text.replace(old, new, 1)


manuscript_path = Path('state/manuscript/Peg_Leg_Greg_Running_Manuscript.md')
manuscript = manuscript_path.read_text()
assert manuscript.count('# CHAPTER 231') == 1, 'Chapter 231 missing or duplicated'
tail = '# CHAPTER 231' + manuscript.split('# CHAPTER 231', 1)[1]
assert '## THE MAGISTRATE' in tail
assert tail.count('—') == 0
words = len(re.findall(r"\b[\w’'-]+\b", tail))
assert 2500 <= words <= 4000, words

# MANUSCRIPT_STATE
p = Path('state/MANUSCRIPT_STATE.md')
s = p.read_text()
s = replace_once(s, '- Current story endpoint: Chapter 230 — **THE REPLICATE**.', '- Current story endpoint: Chapter 231 — **THE MAGISTRATE**.', 'manuscript endpoint')
s = replace_once(
    s,
    '- Hessa ends Ch230 with no chosen next experiment. She still has several questions; asked whether there are more or fewer, she says `Different`.',
    '- Hessa ends Ch230 with no chosen next experiment. She still has several questions; asked whether there are more or fewer, she says `Different`.\n- Chapter 231 contains no magic attempt or Hessa appearance. Counts remain 33 / 29 / 45 and all restrictions remain unchanged.',
    'magic rest through 231',
)
s = replace_once(
    s,
    "- Greg's poor shirt-cuff repair worsens from two loose threads to three; he deliberately does not repair it again. No clothing subplot is required.",
    "- Greg's poor shirt-cuff repair worsens from two loose threads to three; he deliberately does not repair it again. No clothing subplot is required.\n- Ch231 the narrow folded brown cloth remains in the same fold with the same three pins at morning and evening; customer, garment, ownership, and use remain unestablished. Greg's cuff remains at three loose threads and is not repaired.",
    'household residue through 231',
)
s = replace_once(
    s,
    '- Ch230 contains no Vale appearance, debt payment, or debt credit. Greg buys one ordinary meat pie and otherwise leaves the debt active and unstated.',
    '- Ch230 contains no Vale appearance, debt payment, or debt credit. Greg buys one ordinary meat pie and otherwise leaves the debt active and unstated.\n- Ch231 contains no Vale appearance, debt payment, or debt credit. Greg receives the normal one copper for theatre work; debt remains active and unstated.',
    'economy through 231',
)
s = replace_once(s, 'Chapters 224–230 do not advance the pressure arc.', 'Chapters 224–231 do not advance the pressure arc.', 'pressure through 231')

chapter231 = '''## Chapter 231 — THE MAGISTRATE
- Full theatre-centered day after Ch230 magic. No Hessa appearance or magic attempt, no Vale appearance or debt credit, and no Bren/pressure movement.
- The window trim Greg helped Jori with in Ch229 is now mounted on the magistrate-room set. Its old cream/green/blue paint history remains visible from backstage, including the small cream transfer mark Greg made; none matters to the audience.
- Greg is cast as the **Magistrate** in **The Crooked Fence**, with Hara as Widow, Marek as Neighbor, and Pell as Clerk. Greg has fifteen lines, begins already seated behind the desk, and stands only once late in the piece.
- Nessa chooses a shorter black stage coat that stays clear of Greg's crutches. The magistrate's wooden seal block belongs on a leather square, with two planned strikes; hitting the desk is specifically prohibited because prior actors damage it.
- Jori shifts the witness rail a few inches so Greg's standing route works cleanly. After the first rail develops a real wobble, Jori and Davin replace it rather than keeping a physical problem merely because the play is about a crooked fence.
- Rehearsal correction: Greg initially leans/chases every answer. Teren narrows him to `The case comes to you` and `Let them bring the mess.` Greg becomes funnier by doing less and letting Pell/Hara/Marek carry the dispute.
- Live mistake: Pell begins a sentence with `Before judgment...`; Greg anticipates the later cue and strikes the block early, cutting Pell off before the older survey is read. Hara continues in character, Pell restarts the sentence, and the scene survives without turning Greg's error into a triumph.
- Teren later corrects Greg's framing: when Greg says `Hara fixed it`, Teren answers `Hara continued.` Preserve the distinction.
- Hara owns the strongest audience beat. After fighting all play for two feet of disputed land, her Widow learns the strip carries responsibility for the drainage ditch and instantly says `His`, then claims she has spent the hour proving Marek's ownership. Greg's later drainage line gets a smaller laugh.
- Company life remains active around the play: Marek steals Davin's apple, Rinna steals Hara's better bread, Nessa controls props, Jori/Davin argue practical geometry, and the set begins changing for another use before Greg leaves.
- Greg receives the normal one copper for theatre work. His body remains ordinary: shoulders/right hand fine, one standing cross substantially easier than the Ch228 flower work, no injury or new limitation.
- Home remains deliberately unresolved. The narrow brown cloth still has the same three pins and fold; Greg's cuff still has three loose threads. Lyssa hears the short version of the show, takes the better piece of bread, and no garment or magic issue is advanced.

'''
marker = '## Immediate next edge — Chapter 231\n'
assert marker in s and '## Chapter 231 — THE MAGISTRATE' not in s
s = s.replace(marker, chapter231 + marker, 1)

edge = '''## Immediate next edge — Chapter 232
Primary recommendation: **LET THE FULL CH231 THEATRE / PERFORMANCE DAY BREATHE. MOVE ONLY THE ENGINE THAT HAS REAL DAILY PRESSURE.**

Reasons:
- Ch231 is a complete rehearsal/performance/workplace chapter immediately after the dense Ch230 magic session; another full performance would overconcentrate theatre even though the company remains available as ordinary background life;
- Hessa has no chosen next experiment after Ch230, and Ch231 correctly leaves 33 / 29 / 45 untouched. Do not reopen magic on a timer;
- Vale has rested since Ch227. Suitable office work can recur if Greg has a concrete work/money reason, but there is still no guaranteed schedule, post, or rate;
- external pressure remains quiet through Ch231. A grounded new fact may arrive through an established commercial contact, but the quiet stretch is not an escalation quota and Greg should not investigate merely because time passed;
- Lyssa's narrow brown cloth remains deliberately undefined and unchanged through Ch231. It can continue to exist without being explained, while her work/life remains independent off-page;
- ordinary Carrow, food, money, errands, friendships, body costs, and household rhythm remain full story engines rather than filler.

Strong Chapter 232 possibilities:
- a Vale/money/work day if Greg has an actual reason to seek suitable labor;
- an ordinary city/social/household day that lets both theatre and magic breathe while Lyssa continues independently;
- one grounded external-pressure fact only if it naturally reaches an existing business/theatre relationship, with no invented plan or investigation;
- theatre may appear briefly as workplace texture or an obligation, but avoid another full rehearsal/performance unless the current day genuinely demands it.

Preserve magic counts 33 / 29 / 45 and all restrictions. Preserve the brown-cloth and cuff uncertainty unless new prose genuinely needs movement. Do not turn Ch231's acting correction into a universal life lesson.

## Chat / handoff behavior'''
s, n = re.subn(r'## Immediate next edge — Chapter 231\n.*?\n## Chat / handoff behavior', edge, s, count=1, flags=re.S)
assert n == 1, 'next edge replacement failed'
p.write_text(s)

# OPEN_THREADS
p = Path('state/OPEN_THREADS.md')
o = p.read_text()
o = replace_once(o, '- **Current endpoint:** Chapter 230 — **THE REPLICATE**.', '- **Current endpoint:** Chapter 231 — **THE MAGISTRATE**.', 'open endpoint')
o = replace_once(
    o,
    '- **Ch230 Hessa replication:** reversed predeclared order yields one clean INTERMEDIATE response, one clean INTERMEDIATE non-response, and two clean FAR non-responses. Counts end 33 / 29 / 45; restrictions unchanged.',
    '- **Ch230 Hessa replication:** reversed predeclared order yields one clean INTERMEDIATE response, one clean INTERMEDIATE non-response, and two clean FAR non-responses. Counts end 33 / 29 / 45; restrictions unchanged. Ch231 contains no magic attempt; counts remain 33 / 29 / 45.',
    'open magic rest',
)
o = replace_once(o, '**Threat restraint:** Chapters 224–230', '**Threat restraint:** Chapters 224–231', 'open pressure')
o = replace_once(o, 'Chapters 228–230 have no Vale movement.', 'Chapters 228–231 have no Vale movement.', 'open vale rest')
o = replace_once(
    o,
    '- **Next engine rotation:** let Ch230 magic breathe. Theatre, Vale/money, ordinary Carrow/social life, or one genuinely grounded pressure fact are available; none is owed on a timer.',
    '- **Next engine rotation:** let the full Ch231 theatre/performance day breathe. Vale/money, ordinary Carrow/social/household life, or one genuinely grounded pressure fact are available; none is owed on a timer. Hessa still has no chosen next experiment.',
    'open next rotation',
)
anchor = '- **Theatre:** Ch228 is a full **The Wrong Funeral** rehearsal/performance/workplace chapter. Greg performs six lines as `Man with flowers` and a later unlined basket pickup. Hara owns the strongest live recovery and audience beat.\n'
assert anchor in o and '- **Ch231 theatre:**' not in o
insert = '''- **Ch231 theatre:** full **The Crooked Fence** rehearsal/performance day. Greg plays the fifteen-line, mostly seated **Magistrate**; Hara = Widow, Marek = Neighbor, Pell = Clerk. The Ch229 window trim is now part of the magistrate-room set.
- **Ch231 acting correction:** Teren narrows Greg from chasing every answer to `The case comes to you` / `Let them bring the mess.` In performance Greg anticipates the seal-block cue and strikes early when Pell begins `Before judgment...`; Hara continues and Pell restarts. Post-show, Teren corrects Greg's `Hara fixed it` to `Hara continued.` Keep all of this theatre-specific, not a life maxim.
- **Ch231 strongest beat:** Hara's Widow abandons her hard-fought land claim the instant Pell reveals the disputed strip includes the drainage ditch: `His.` / `I have spent an hour proving your ownership.` She owns the room; Greg's later line gets a smaller laugh.
- **Ch231 stagecraft/body:** Nessa uses a shorter black stage coat and protects the desk with a leather strike square. Jori shifts the witness rail for clean route geometry; Jori/Davin later replace the first rail when it genuinely wobbles. Greg's one standing cross is ordinary; shoulders/right hand remain fine.
- **Ch231 pay:** Rinna pays the normal one copper for theatre work. No Vale movement or debt arithmetic follows.
- **Ch231 household:** narrow brown cloth remains same fold / same three pins; Greg's cuff remains three loose threads. Neither is resolved.
'''
o = o.replace(anchor, insert + anchor, 1)
o = replace_once(o, '- **Crutch maintenance:** one worn LEFT tip replaced Ch223; it remains normal through Ch229.', '- **Crutch maintenance:** one worn LEFT tip replaced Ch223; it remains normal through Ch231.', 'crutch through 231')
p.write_text(o)

# INDEX
p = Path('state/MANUSCRIPT_CHAPTER_INDEX.md')
i = p.read_text()
i = replace_once(i, '# PEG-LEG GREG — CHAPTER INDEX — CH230', '# PEG-LEG GREG — CHAPTER INDEX — CH231', 'index heading')
i = replace_once(i, '**Current endpoint:** Chapter 230 — THE REPLICATE', '**Current endpoint:** Chapter 231 — THE MAGISTRATE', 'index endpoint')
assert '231. **THE MAGISTRATE**' not in i
assert i.rstrip().endswith('230. **THE REPLICATE**')
i = i.rstrip() + '\n231. **THE MAGISTRATE**\n'
p.write_text(i)

# WORKFLOW
p = Path('state/MANUSCRIPT_WORKFLOW.md')
w = p.read_text()
w = replace_once(w, 'Chapter 230 — **THE REPLICATE**.', 'Chapter 231 — **THE MAGISTRATE**.', 'workflow edge')
w = replace_once(w, 'See `state/MANUSCRIPT_STATE.md` for current canon and the Chapter 231 edge.', 'See `state/MANUSCRIPT_STATE.md` for current canon and the Chapter 232 edge.', 'workflow next')
p.write_text(w)

# PROJECT STATE
p = Path('state/PROJECT_STATE.md')
ps = p.read_text()
ps = replace_once(ps, 'Current recorded story endpoint is Chapter 230 — **THE REPLICATE**.', 'Current recorded story endpoint is Chapter 231 — **THE MAGISTRATE**.', 'project endpoint')
p.write_text(ps)

print('chapter_words', words)
print('state_sync_ready', True)
