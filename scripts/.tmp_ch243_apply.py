from pathlib import Path
import re

ROOT = Path('.')
MANUSCRIPT = ROOT / 'state/manuscript/Peg_Leg_Greg_Running_Manuscript.md'
STATE = ROOT / 'state/MANUSCRIPT_STATE.md'
OPEN = ROOT / 'state/OPEN_THREADS.md'
INDEX = ROOT / 'state/MANUSCRIPT_CHAPTER_INDEX.md'
WORKFLOW = ROOT / 'state/MANUSCRIPT_WORKFLOW.md'
PROJECT = ROOT / 'state/PROJECT_STATE.md'
CHAPTER_PATH = ROOT / 'scripts/.tmp_ch243.txt'

chapter = CHAPTER_PATH.read_text(encoding='utf-8').strip()
assert '# CHAPTER 243' in chapter
assert '## THE MINDER' in chapter
assert '—' not in chapter
body = chapter.split('## THE MINDER\n\n', 1)[1]
word_count = len(re.findall(r"\b[\w’'-]+\b", body))
assert 2500 <= word_count <= 4000, word_count

manuscript = MANUSCRIPT.read_text(encoding='utf-8')
assert '# CHAPTER 243' not in manuscript
assert '# CHAPTER 242' in manuscript
manuscript = manuscript.rstrip() + '\n\n' + chapter + '\n'
MANUSCRIPT.write_text(manuscript, encoding='utf-8')

state = STATE.read_text(encoding='utf-8')
assert '- Current story endpoint: Chapter 242 — **THE SPENDER**.' in state
state = state.replace('- Current story endpoint: Chapter 242 — **THE SPENDER**.', '- Current story endpoint: Chapter 243 — **THE MINDER**.', 1)
state = state.replace('- Chapters 241–242 contain no Hessa appearance or magic attempt. Counts remain 35 / 31 / 53, all restrictions remain unchanged, and Hessa still has no selected next experiment.', '- Chapters 241–243 contain no Hessa appearance or magic attempt. Counts remain 35 / 31 / 53, all restrictions remain unchanged, and Hessa still has no selected next experiment.', 1)
state = state.replace('- Chapters 240–242 do not advance the pressure arc. Ch236 remains the newest grounded pressure fact; no new warning, supplier report, investigation, security response, Bren fact, Mason\'s Cut movement, or Vale connection appears.', '- Chapters 240–243 do not advance the pressure arc. Ch236 remains the newest grounded pressure fact; no new warning, supplier report, investigation, security response, Bren fact, Mason\'s Cut movement, or Vale connection appears.', 1)
needle = '- Ch240–241 contain no Vale work, payment, or debt credit. In Ch242 Greg pays an ordinary crutch-grip repair cost, then voluntarily checks Vale for suitable work. The clerk has no suitable work for Greg that day, so Greg receives no credit. `Tomorrow, maybe` sealing is conditional only. Debt remains active and unstated.'
assert needle in state
state = state.replace(needle, needle + '\n- Ch243 contains no Vale appearance, work, payment, or debt credit. Greg buys ordinary onions and a flat cake while the debt remains active and unstated. Ch242\'s `Tomorrow, maybe` does not become a Chapter 243 task.', 1)
lyssa_anchor = '- Lyssa understands the control logic quickly from Ch226 but remains independent of Hessa\'s domain.'
assert lyssa_anchor in state
state = state.replace(lyssa_anchor, '- Ch243 Lyssa is already out when Greg discovers the household is out of onions. She returns after dark with an ordinary small packet of greens used in supper and no recognizable work bundle. Brown cloth remains same fold/three pins; Ch241 dark cloth remains absent/unexplained; damaged shirt remains three loose threads; better shirt keeps its blue paint streak. Beans and the older paper-wrapped item remain absent/unexplained.\n' + lyssa_anchor, 1)

marker = '## Immediate next edge — Chapter 243'
chat_marker = '## Chat / handoff behavior'
assert marker in state and chat_marker in state
prefix, tail = state.split(marker, 1)
_, chat = tail.split(chat_marker, 1)
new_tail = r'''## Chapter 243 — THE MINDER
- Chapter 243 lets Ch242's maintenance/no-work money day breathe. No theatre call/work/pay, Hessa appearance/magic attempt, Vale appearance/work/credit, Bren/brown-coat fact, warning, investigation, or pressure escalation occurs. Magic remains **35 / 31 / 53** with all restrictions unchanged.
- The day's actual claim is ordinary household need: Greg discovers they are fully out of onions and returns to the established market onion seller. She recognizes his recent buying pattern strongly enough to preempt him with `Three`; she still does not establish Greg's name or any broader reputation.
- A delivery handcart arrives with one split onion sack. The seller leaves Greg on her stool with the narrow instruction to watch the onions and, when he asks `Sell?`, answers `No.` Greg interprets that literally and makes three existing customers wait rather than allowing their already-established arrangements to continue.
- The waiting customers expose social knowledge Greg does not have: an older woman routinely takes three small onions at an established price, a cookshop boy collects a prepared six-onion bag on later payment, and a young woman arrives with the correct copper for two large onions. The seller clears the entire backlog almost immediately on return and explains that Greg was not authorized to sell, not that regular customers had stopped being customers.
- The seller gives Greg a more precise second instruction set: regulars who know what they take/owe can continue; Greg does not set prices, make change, promise credit, or decide for strangers. A green-scarf customer later takes four medium onions and leaves the expected coin; Greg correctly lets the arrangement stand without pretending to know the price.
- The split-sack dispute remains the seller's commercial problem. Greg does not learn the supplier terms or exact loss. He helps only with bounded damaged-onion sorting under her direction: trim soft sections, put clean usable remainder in a same-day basket, and reject anything wet through / wrong-smelling. The seller corrects one Greg judgment after showing him a translucent bad base.
- Greg receives no wage and no market job. He pays full ordinary price for his three onions. The seller adds one small damaged-but-usable `today` onion from the split-sack pile; this is practical food salvage, not formal compensation or a new favor debt.
- The Ch242 right-grip repair remains successful and mostly invisible in use. The grip stays flat/even, tack does not contact Greg's hand, repaired LEFT tip/grip remain normal, and Greg has only brief ordinary sitting stiffness at the stall. No injury or new limitation occurs.
- Home remains bounded. Lyssa returns with ordinary greens used for supper and no recognizable work bundle. She laughs hard when Greg explains that he stopped three customers because he interpreted `Don't sell` as a ban on all transactions. Brown cloth remains same fold/three pins; Ch241 dark cloth stays absent; damaged shirt remains three loose threads; better shirt retains the blue paint streak; beans and the older wrapped item remain absent/unexplained.

## Immediate next edge — Chapter 244
Primary recommendation: **LET CH243'S MARKET-SOCIAL DAY BREATHE. FOLLOW THE NEXT ACTUAL CLAIM RATHER THAN TURNING THE ONION STALL INTO A JOB, RESURRECTING VALE'S EXPIRED `TOMORROW, MAYBE`, OR MAKING CH240'S FAR RESPONSE INTO A MAGIC LADDER.**

Reasons:
- Ch240 was a full bounded Hessa FAR-only session; Ch241 was ordinary theatre scenery labor; Ch242 was crutch maintenance plus a Vale check that produced no suitable work; Ch243 is ordinary Carrow market/social life with no institutional engine movement.
- The onion seller now has a little more social memory with Greg, but Greg is not her employee, clerk, apprentice, regular stall minder, or pricing authority. The temporary stall episode needs no immediate repeat.
- Ch242's `Tomorrow, maybe` sealing possibility has already passed through Ch243 without becoming work. Do not treat it as a standing Vale promise. Debt remains active/unstated, and Greg still has no guaranteed post, schedule, promotion, or rate.
- Magic remains **35 / 31 / 53**. Attempt 52 remains one clean FAR/AWAY response inside the fixed FAR-only block; no range, rate, equivalence, generalization, or new permission is established. Hessa still has no selected next experiment.
- External pressure still last moved in Ch236. Ch237–243 add no new clue or defensive escalation. The repaired theatre back latch remains ordinary maintenance and no Vale/Bren connection exists.
- Household objects remain bounded rather than queued for explanation: brown cloth same fold/three pins; damaged shirt three loose threads; better shirt blue streak; Ch241 dark cloth absent/unexplained; beans and the older wrapped item absent/unexplained.

Strong Chapter 244 possibilities:
- an established social route or ordinary Carrow obligation with its own independent momentum;
- theatre only if a genuinely new call/task arrives, since Greg still has no standing role;
- Vale only if suitable ordinary work actually exists now, through a fresh real circumstance rather than the stale Ch242 maybe;
- Lyssa/household/work only if a real obligation surfaces without servicing tracked objects by checklist;
- one grounded pressure fact through an established natural carrier only if it genuinely arrives;
- NOT Hessa unless she independently selects a genuinely new bounded question after considering the Ch240 record.

Ask: **WHAT ACTUALLY HAS A REASON TO HAPPEN TODAY?** Favor **LIFE PER WORD**.

Preserve magic counts **35 / 31 / 53** and all restrictions. Preserve Attempt 52 as one clean FAR/AWAY response without power-up. Preserve active unstated Vale debt, Ch238 credit, Ch242's no-work/no-credit result, and the fact that its `Tomorrow, maybe` did not create Ch243 work. Preserve Ch236's delivery/access evidence ceiling and no Vale/Bren connection. Preserve ordinary back-latch interpretation, Greg's body continuity, successful right-grip repair and normal left tip/grip, onion-seller social memory without converting it into employment, brown-cloth identity limits, three-thread damaged-shirt continuity, blue-streak better-shirt residue, bean-purpose limits, absent older wrapped-item identity ceiling, absent Ch241 dark-cloth identity ceiling, Lyssa customer/garment boundaries, and **Marra ≠ Maren**.

'''
state = prefix + new_tail + chat_marker + chat
STATE.write_text(state, encoding='utf-8')

open_threads = OPEN.read_text(encoding='utf-8')
assert '- **Current endpoint:** Chapter 242 — **THE SPENDER**.' in open_threads
open_threads = open_threads.replace('- **Current endpoint:** Chapter 242 — **THE SPENDER**.', '- **Current endpoint:** Chapter 243 — **THE MINDER**.', 1)
open_threads = open_threads.replace('one worn LEFT tip was replaced Ch223 and remains normal through Ch242.', 'one worn LEFT tip was replaced Ch223 and remains normal through Ch243.', 1)
onion_anchor = '- **Onion seller recognition:** Ch228 the onion seller remembers Greg as the customer who previously stood too long deciding how many onions to buy. She does not establish his name or a broader reputation. Keep this as tiny Carrow social memory, not celebrity progression.'
assert onion_anchor in open_threads
open_threads = open_threads.replace(onion_anchor, onion_anchor + '\n- **Ch243 onion-stall residue:** the same seller now preempts Greg with `Three` based on his recent buying pattern, then briefly has him mind the stall during a split-sack delivery dispute. Greg over-literalizes `Sell? / No` and delays three regular transactions until she returns. Existing customers have arrangements Greg does not know; the seller handles pricing/credit/supplier loss. Greg later helps sort a few damaged onions under direction. This does NOT establish Greg as stall staff, seller, apprentice, pricing authority, or regular minder.', 1)
OPEN.write_text(open_threads, encoding='utf-8')

index = INDEX.read_text(encoding='utf-8')
assert '# PEG-LEG GREG — CHAPTER INDEX — CH242' in index
assert '**Current endpoint:** Chapter 242 — THE SPENDER' in index
assert '243. **THE MINDER**' not in index
index = index.replace('# PEG-LEG GREG — CHAPTER INDEX — CH242', '# PEG-LEG GREG — CHAPTER INDEX — CH243', 1)
index = index.replace('**Current endpoint:** Chapter 242 — THE SPENDER', '**Current endpoint:** Chapter 243 — THE MINDER', 1)
index = index.rstrip() + '\n243. **THE MINDER**\n'
INDEX.write_text(index, encoding='utf-8')

workflow = WORKFLOW.read_text(encoding='utf-8')
assert 'Chapter 242 — **THE SPENDER**.' in workflow
assert 'Chapter 243 edge.' in workflow
workflow = workflow.replace('Chapter 242 — **THE SPENDER**.', 'Chapter 243 — **THE MINDER**.', 1)
workflow = workflow.replace('Chapter 243 edge.', 'Chapter 244 edge.', 1)
WORKFLOW.write_text(workflow, encoding='utf-8')

project = PROJECT.read_text(encoding='utf-8')
assert 'Current recorded story endpoint is Chapter 242 — **THE SPENDER**.' in project
project = project.replace('Current recorded story endpoint is Chapter 242 — **THE SPENDER**.', 'Current recorded story endpoint is Chapter 243 — **THE MINDER**.', 1)
PROJECT.write_text(project, encoding='utf-8')

changed = [str(p.relative_to(ROOT)) for p in [MANUSCRIPT, STATE, OPEN, INDEX, WORKFLOW, PROJECT]]
print('CH243_WORDS', word_count)
print('CH243_EM_DASHES', chapter.count('—'))
print('CHANGED', ','.join(changed))
