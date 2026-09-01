from pathlib import Path
import re

ROOT = Path('.')
manuscript = ROOT / 'state/manuscript/Peg_Leg_Greg_Running_Manuscript.md'
state = ROOT / 'state/MANUSCRIPT_STATE.md'
threads = ROOT / 'state/OPEN_THREADS.md'
index = ROOT / 'state/MANUSCRIPT_CHAPTER_INDEX.md'
workflow = ROOT / 'state/MANUSCRIPT_WORKFLOW.md'
project = ROOT / 'state/PROJECT_STATE.md'
payload_path = ROOT / 'state/.ch239_waiter_payload.md'

chapter = payload_path.read_text()
assert chapter.startswith('# CHAPTER 239\n\n## THE WAITER\n')
assert chapter.count('—') == 0
words = len(re.findall(r"\b[\w’'-]+\b", chapter))
assert 2500 <= words <= 4000, words
assert chapter.rstrip().endswith('It was almost enough to make waiting feel like a job.')

m = manuscript.read_text()
assert '# CHAPTER 239' not in m
m = m.rstrip() + '\n\n------------------------------------------------------------------------\n\n' + chapter.strip() + '\n'
manuscript.write_text(m)

s = state.read_text()
s = s.replace('Current story endpoint: Chapter 238 — **THE SEALER**.', 'Current story endpoint: Chapter 239 — **THE WAITER**.', 1)
magic_238 = '- Chapter 238 contains no Hessa appearance or magic attempt. Counts remain 34 / 30 / 49 and all restrictions remain unchanged.'
assert magic_238 in s
s = s.replace(magic_238, magic_238 + '\n- Chapter 239 contains no Hessa appearance or magic attempt. Counts remain 34 / 30 / 49 and all restrictions remain unchanged.', 1)
lyssa_238 = '- Ch238 Lyssa is already out when Greg leaves for Vale and home when he returns. The small paper-wrapped item from Ch237 is gone without explanation; beans remain off-page/unexplained. Brown cloth remains same fold/three pins and damaged shirt remains three loose threads.'
assert lyssa_238 in s
s = s.replace(lyssa_238, lyssa_238 + '\n- Ch239 Lyssa is home briefly in the morning, asks Greg to buy bread and salt if he is out, then leaves north for her own work. She returns later with an apple and cloth-wrapped cheese. Beans remain off-page/unexplained; the earlier paper-wrapped item remains absent/unexplained. Brown cloth remains same fold/three pins and damaged shirt remains three loose threads.', 1)
econ_238 = '- Ch238 Greg completes suitable Vale sealing work and receives legitimate debt credit. Exact credit and current balance remain unstated; Greg sees the balance remain substantial but smaller. He receives no theatre pay because he does no theatre work.'
assert econ_238 in s
s = s.replace(econ_238, econ_238 + '\n- Ch239 contains no Vale appearance, office work, payment, or debt credit. Greg buys ordinary bread, salt, and his own cookshop bowl while the debt remains active and unstated.', 1)
threat_238 = "- Ch238 does not advance the pressure arc. No new warning, visitor, supplier report, investigation, access change, security response, Bren fact, Mason's Cut movement, or Vale connection appears."
assert threat_238 in s
s = s.replace(threat_238, threat_238 + "\n- Ch239 does not advance the pressure arc. No new warning, visitor, supplier report, investigation, access change, security response, Bren fact, Mason's Cut movement, or Vale connection appears.", 1)

new_tail = '''## Chapter 239 — THE WAITER
- Chapter 239 lets Ch238's Vale/theatre tradeoff breathe. No theatre work or call, Vale work/credit, Hessa appearance/magic attempt, or Bren/brown-coat fact occurs.
- Morning household claim is narrow and ordinary: Lyssa asks Greg to buy bread and salt if he is out, then goes north for her own work. The brown cloth remains same fold/three pins; Greg's damaged shirt remains three loose threads; beans and the prior paper-wrapped item remain absent/unexplained.
- Greg buys bread, then encounters Hara at the west-steps cobbler. This pays off the Ch233 shoe problem without making it Greg's task: the repaired left sole has held, but the new stitching has pulled the heel side tighter and the shoe now rubs. The cobbler owns the diagnosis and adjustment.
- Hara has to wait while the cobbler adjusts the shoe. Greg waits with her because he genuinely has no schedule. Their offstage relationship gets ordinary room without becoming an acting lesson or emotional milestone.
- Greg still completes his salt errand and buys Hara one copper's worth of roasted peas with her money. After the adjustment, Hara asks Greg to walk with her while she tests the shoe. The heel is less painful and does not start biting again during the observed walk; no broader medical issue or permanent fix is established.
- Hara has independent market familiarity: a vegetable seller knows her usual quantity, and a cookshop customer recognizes her as the Widow from **The Crooked Fence**. He recognizes Hara, not Greg, and returns to lunch after saying the show was good.
- Greg and Hara each pay for their own cookshop bowl. Greg's money remains ordinary; no debt arithmetic or compensation for missing Ch238 theatre occurs.
- Body cost is ordinary from the longer walk: used shoulders, warm right palm, ordinarily tired right leg, comfortable residual limb, normal repaired left crutch tip, no injury or new limitation.
- Home stays small. Lyssa checks the ordinary categories `Theatre?`, `Vale?`, `Magic?`; all are no. Greg's day reduces to `Hara's shoe`, and supper is bread, cheese, and apple. No open thread is explained merely because the chapter is quiet.

## Immediate next edge — Chapter 240
Primary recommendation: **LET CH239'S OFFSTAGE HARA/GREG DAY BREATHE. FOLLOW THE NEXT ACTUAL CLAIM RATHER THAN TURNING A NEW SOCIAL BEAT INTO A ROUTINE.**

Reasons:
- Ch239 deliberately moved outside theatre, Vale, magic, and pressure while deepening an existing coworker relationship through ordinary Carrow time.
- Hara's shoe problem has received a narrow material adjustment and does not require another chapter. The repair held at the sole; the heel adjustment reduced the immediate rubbing during the walk. Do not promote this into an injury arc or permanent shoe subplot.
- Greg has no standing theatre obligation. **The Missing Key** remains done for now and Venn's one-day coverage remains ordinary.
- Vale last moved in Ch238 and debt remains active, but Greg still has no guaranteed post, schedule, promotion, or rate.
- Magic has now breathed through Chapters 235–239 after Ch234. Hessa remains increasingly available only if she has actually selected one genuinely bounded next question. Do not invent an experiment from elapsed chapter count alone.
- External pressure last moved in Ch236. Chapters 237–239 add no clue or escalation. One grounded fact may arrive naturally later; there is no quota.
- Lyssa's beans and the earlier paper-wrapped item remain absent/unexplained. Brown cloth remains same fold/three pins and Greg's shirt remains three loose threads. Do not convert any of them into mysteries by state-maintenance pressure.

Strong Chapter 240 possibilities:
- Hessa, if she has now selected one bounded next question under the established apparatus and restrictions;
- a genuinely new theatre or Vale call/task if one actually arrives;
- Lyssa/household/work if a real obligation surfaces without bookkeeping the beans, wrapped item, or brown cloth;
- ordinary Carrow or another established relationship if it produces more life per word;
- one grounded pressure fact through an established natural carrier only if it genuinely arrives.

Preserve magic counts **34 / 30 / 49** and all restrictions unless Ch240 genuinely changes them. Preserve active unstated Vale debt and Ch238 credit. Preserve that **The Missing Key** is done for now and Venn's coverage created no rivalry or hierarchy. Preserve Ch236's delivery/access evidence ceiling and no Vale/Bren connection. Preserve Greg's body continuity, Hara's narrow shoe-adjustment facts, brown-cloth identity limits, three-thread shirt continuity, bean-purpose limits, absent wrapped-item identity ceiling, Lyssa customer/garment boundaries, and **Marra ≠ Maren**.

'''
pattern = r'## Immediate next edge — Chapter 239\n.*?(?=## Chat / handoff behavior)'
assert re.search(pattern, s, flags=re.S)
s = re.sub(pattern, new_tail, s, count=1, flags=re.S)
state.write_text(s)

o = threads.read_text()
o = o.replace('**Current endpoint:** Chapter 238 — **THE SEALER**.', '**Current endpoint:** Chapter 239 — **THE WAITER**.', 1)
old_rotation = "- **Next engine rotation:** let Ch238's Vale/theatre tradeoff breathe. Prefer a fresh social/Carrow/Lyssa claim, or Hessa only if a bounded question is actually selected; theatre, Vale, or pressure return only through a genuinely new obligation/fact."
assert old_rotation in o
new_threads = '''- **Ch239 offstage Hara/Greg:** Greg encounters Hara at the west-steps cobbler while on an ordinary bread/salt errand and waits with her while the same repaired left shoe is adjusted. Their time together is social/Carrow life, not theatre work or a lesson about Ch238.
- **Ch239 Hara shoe:** the Ch233 left-sole repair has held, but the new stitching has pulled the heel side tighter and caused rubbing. The cobbler adjusts it with dark leather; Hara's longer test walk is less painful and the heel does not bite again during the observed route. No injury or permanent footwear arc established.
- **Ch239 Hara social residue:** a vegetable seller knows Hara's usual quantity, and a cookshop diner recognizes her as the Widow from **The Crooked Fence**. This is Hara's partial social visibility, not Greg celebrity or a universal theatre reputation.
- **Ch239 engine restraint:** no theatre call/work/pay, Vale appearance/work/credit, Hessa/magic attempt, or new threat fact. Magic remains 34 / 30 / 49; debt remains active and unstated; Ch236 remains newest pressure fact.
- **Ch239 household/body:** Greg buys bread and salt; Lyssa goes north independently and later returns with an apple and cloth-wrapped cheese. Beans and the old paper-wrapped item remain absent/unexplained. Brown cloth stays same fold/three pins; damaged shirt stays three loose threads. Greg has ordinary longer-walk fatigue only and no injury.
- **Next engine rotation:** let Ch239's offstage Hara/Greg day breathe. Hessa is increasingly available only if she has actually selected one bounded next question; theatre, Vale, Lyssa work, pressure, or another social route should return only through a real new claim rather than rotation inertia.'''
o = o.replace(old_rotation, new_threads, 1)
threads.write_text(o)

i = index.read_text()
i = i.replace('# PEG-LEG GREG — CHAPTER INDEX — CH238', '# PEG-LEG GREG — CHAPTER INDEX — CH239', 1)
i = i.replace('**Current endpoint:** Chapter 238 — THE SEALER', '**Current endpoint:** Chapter 239 — THE WAITER', 1)
assert '239. **THE WAITER**' not in i
i = i.rstrip() + '\n239. **THE WAITER**\n'
index.write_text(i)

w = workflow.read_text()
w = w.replace('Chapter 238 — **THE SEALER**.', 'Chapter 239 — **THE WAITER**.', 1)
w = w.replace('Chapter 239 edge.', 'Chapter 240 edge.', 1)
workflow.write_text(w)

p = project.read_text()
p = p.replace('Current recorded story endpoint is Chapter 238 — **THE SEALER**.', 'Current recorded story endpoint is Chapter 239 — **THE WAITER**.', 1)
project.write_text(p)

print('chapter_words', words)
print('em_dashes', chapter.count('—'))
