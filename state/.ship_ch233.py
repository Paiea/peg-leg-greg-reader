from pathlib import Path
import re

def replace_once(text, old, new, label):
    n = text.count(old)
    assert n == 1, f"{label}: expected 1 occurrence, found {n}"
    return text.replace(old, new, 1)

chapter = Path("state/manuscript/.ch233_seat.tmp").read_text().strip() + "\n"
assert chapter.count("# CHAPTER 233") == 1
assert chapter.count("## THE SEAT") == 1
body = chapter.split("## THE SEAT", 1)[1]
words = len(re.findall(r"\b[\w’'-]+\b", chapter))
assert 2500 <= words <= 4000, words
assert "—" not in body, "em dash in Chapter 233 prose"

m = Path("state/manuscript/Peg_Leg_Greg_Running_Manuscript.md")
text = m.read_text()
assert text.count("## Chapter 232 — THE COUNTERSIGN") == 1, "canonical COUNTERSIGN missing/duplicated"
assert "# CHAPTER 232\n\n## THE MATCHER" not in text, "stale MATCHER present"
assert "# CHAPTER 233" not in text and "## Chapter 233" not in text, "Chapter 233 already exists"
m.write_text(text.rstrip() + "\n\n" + chapter.lstrip())

p = Path("state/MANUSCRIPT_STATE.md")
s = p.read_text()
s = replace_once(s, "- Current story endpoint: Chapter 232 — **THE COUNTERSIGN**.", "- Current story endpoint: Chapter 233 — **THE SEAT**.", "state endpoint")
s = replace_once(
    s,
    "- Chapters 231–232 contain no magic attempt or Hessa appearance. Counts remain 33 / 29 / 45 and all restrictions remain unchanged.",
    "- Chapters 231–233 contain no magic attempt or Hessa appearance. Counts remain 33 / 29 / 45 and all restrictions remain unchanged.",
    "magic rest span",
)
s = replace_once(
    s,
    "- Ch232 the same narrow brown cloth remains in the same fold with the same three pins. Lyssa is working on a separate dark sleeve by evening; no relationship between the sleeve and brown cloth is established. Greg's cuff remains at three loose threads.",
    "- Ch232 the same narrow brown cloth remains in the same fold with the same three pins. Lyssa is working on a separate dark sleeve by evening; no relationship between the sleeve and brown cloth is established. Greg's cuff remains at three loose threads.\n- Ch233 the dark sleeve is gone by morning while the narrow brown cloth remains in the same fold with the same three pins. Lyssa is already out and later already eating when Greg returns; no customer/job explanation is added. Greg's cuff remains at three loose threads and he still leaves it alone.",
    "Lyssa Ch233",
)
s = replace_once(
    s,
    "- Ch232 Greg voluntarily seeks suitable Vale work after returning the theatre coat. He matches returned payment acknowledgments against account lines under clerk review and receives legitimate debt credit. Exact credit and current balance remain unstated in narration; Greg sees and knows the balance. No guaranteed job, schedule, or rate is created.",
    "- Ch232 Greg voluntarily seeks suitable Vale work after returning the theatre coat. He matches returned payment acknowledgments against account lines under clerk review and receives legitimate debt credit. Exact credit and current balance remain unstated in narration; Greg sees and knows the balance. No guaranteed job, schedule, or rate is created.\n- Ch233 contains no Vale appearance, office work, payment, or debt credit. Greg pays ordinary money for his own cookshop bowl while the debt remains active and unstated.",
    "economy Ch233",
)
s = replace_once(s, "- Chapters 224–232 do not advance the pressure arc.", "- Chapters 224–233 do not advance the pressure arc.", "pressure span")

chapter_state = '''## Chapter 233 — THE SEAT
- Ch232's Vale office day breathes. Greg checks the theatre only because Rinna's `Tomorrow maybe` from Ch232 gives him a reason to see whether work exists; it is not treated as a guaranteed call.
- Theatre is ordinary strike/setup work only. No rehearsal, role, performance, audience, or acting correction occurs.
- Yesterday's merchant-office set is already being repurposed. The blue-trimmed window remains while desk, shelf, benches, rolled canvas, maps, practice swords, and other pieces move to new uses.
- Jori and Davin continue overlapping practical work without hierarchy exposition: they repair/reset the shelf together and keep their dry credit humor. Davin remains competent.
- Greg and Marek carry a rolled canvas through the rear passage. Marek keeps tension correctly, turns for the doorway before Greg needs to explain it, and checks the storage label before releasing the roll.
- Nessa assigns the square table rather than the low table that Marek has hit before. The callback remains practical object memory rather than a Marek punishment beat.
- Greg makes one mundane strike mistake: he moves the wrong black bench because he identifies it by familiar position instead of the shallow split/chalk X on the intended bench. Nessa sends it back; Jori points out the X. No larger lesson or consequence follows.
- Body cost remains ordinary: used shoulders, normal right hand, mildly tired right leg from repeated short stands/starts, comfortable residual limb, no injury or new limitation.
- After work, Rinna, Hara, Pell, Marek, Greg, and later Nessa eat at a nearby cookshop. Everyone buys their own bowl. Hara silently moves her coat to make Greg a place; Pell shifts his feet for the crutches; the scene stays ordinary rather than announcing belonging.
- Ensemble life continues without routing every problem through Greg: Hara's separating shoe sole becomes a Hara/Pell/Rinna/Marek/Nessa conversation; Greg does not know either proposed cobbler well enough to advise and is not asked.
- Rinna gives a clear `Tomorrow no` rather than another maybe. No future theatre obligation is established.
- No Hessa appearance or magic attempt; counts remain 33 / 29 / 45 and restrictions unchanged. No Vale work/debt credit and no Bren/brown-coat/pressure movement.
- Home: Lyssa is already eating rather than waiting. The dark sleeve is gone; the brown cloth remains same fold/three pins; Greg's cuff remains three loose threads. Lyssa reduces Greg's day to `Furniture` / `And soup` / `Mostly soup`; no garment or magic issue is advanced.

'''
marker = "## Immediate next edge — Chapter 233\n"
assert marker in s and "## Chapter 233 — THE SEAT" not in s
s = s.replace(marker, chapter_state + marker, 1)

edge = '''## Immediate next edge — Chapter 234
Primary recommendation: **LET THE CH233 COMPANY / ORDINARY-WORK DAY BREATHE. FOLLOW THE NEXT REAL OBLIGATION OR QUESTION WITHOUT TURNING RESTED ENGINES INTO A ROTATION QUOTA.**

Reasons:
- Ch233 gives theatre a useful non-performance day and a company-social meal after Ch231's full performance and Ch232's Vale day; another immediate company meal or strike chapter would overconcentrate the same texture;
- Hessa has now remained off-page through Chapters 231–233 after Ch230. A return is available only if she has chosen one genuinely bounded next question; three breathing chapters make it possible, not mandatory;
- Vale received a full workday and debt credit in Ch232 and rests in Ch233. Do not convert suitable work into a schedule;
- external Bren/brown-coat pressure remains quiet through Ch233. One grounded fact through an established contact may move it if earned, but elapsed chapters alone are not evidence;
- Lyssa's brown cloth remains deliberately unexplained and her separate dark sleeve has already moved off-page. Preserve her independent work rather than servicing visible objects;
- ordinary Carrow, household rhythm, food, money, bodies, friendships, errands, and partial reputations remain valid primary engines.

Strong Chapter 234 possibilities:
- Hessa returns only with one bounded question that preserves 33 / 29 / 45 as entering counts and all current restrictions;
- one grounded external-pressure fact arrives through an existing supplier/contact while ordinary life continues around it;
- a non-theatre Carrow/household/social day lets Greg spend time with people or places not recently foregrounded;
- a concrete obligation from existing continuity may outrank all of these if the exact new day supplies one.

Do not reopen magic merely because it has rested three chapters. Do not escalate threat because it has been quiet. Do not resolve the brown cloth, cuff, or Hara's shoe unless a present scene genuinely needs them.

## Chat / handoff behavior'''
s, n = re.subn(r"## Immediate next edge — Chapter 233\n.*?\n## Chat / handoff behavior", edge, s, count=1, flags=re.S)
assert n == 1, "state next edge replacement failed"
p.write_text(s)

p = Path("state/OPEN_THREADS.md")
o = p.read_text()
o = replace_once(o, "- **Current endpoint:** Chapter 232 — **THE COUNTERSIGN**.", "- **Current endpoint:** Chapter 233 — **THE SEAT**.", "threads endpoint")
o = replace_once(
    o,
    "Chapters 231–232 contain no magic attempt; counts remain 33 / 29 / 45.",
    "Chapters 231–233 contain no magic attempt; counts remain 33 / 29 / 45.",
    "threads magic rest",
)
o = replace_once(
    o,
    "- **Crutch maintenance:** one worn LEFT tip replaced Ch223; it remains normal through Ch231.",
    "- **Crutch maintenance:** one worn LEFT tip replaced Ch223; it remains normal through Ch233.",
    "threads crutch",
)
o = replace_once(
    o,
    "- **Threat restraint:** Chapters 224–232 contain no new warning, demand, appearance, violence, sabotage, or investigation.",
    "- **Threat restraint:** Chapters 224–233 contain no new warning, demand, appearance, violence, sabotage, or investigation.",
    "threads threat",
)
insert = '''- **Ch233 theatre/work:** no rehearsal or performance. Greg helps strike/repurpose the merchant-office set; blue window remains, other furniture moves. He mistakenly moves the wrong black bench by position rather than the intended shallow split/chalk X and simply corrects it.
- **Ch233 Marek/Nessa/Jori/Davin:** Marek carries rolled canvas competently and checks its storage label; Nessa's low-table warning is practical object memory. Jori/Davin repair/reset the shelf together with overlapping competence and dry credit humor.
- **Ch233 company/social:** after work Rinna, Hara, Pell, Marek, Greg, and later Nessa eat at a nearby cookshop. Hara moves her coat to make Greg a place; everyone pays their own bowl; Hara's shoe-repair problem stays with the people actually discussing it rather than becoming Greg's task.
- **Ch233 body/household:** ordinary used shoulders/mild right-leg fatigue only, no injury. Dark sleeve is gone; brown cloth remains same fold/three pins; cuff remains three loose threads. Lyssa is already eating when Greg returns.
- **Ch233 pressure/magic/Vale:** no Hessa, magic attempt, Vale work/credit, Bren/observer fact, warning, investigation, or escalation. Magic remains 33 / 29 / 45.
'''
anchor = "- **Next engine rotation:**"
assert anchor in o and "- **Ch233 theatre/work:**" not in o
o = o.replace(anchor, insert + anchor, 1)
o = replace_once(
    o,
    "- **Next engine rotation:** let the full Ch232 Vale office day breathe. Follow the next actual obligation or ordinary pressure; theatre is only `Tomorrow maybe`, Hessa still has no chosen experiment, and external pressure is not owed on a timer.",
    "- **Next engine rotation:** let the Ch233 ordinary theatre/company day breathe. Hessa may return only if she has a bounded question; an external-pressure fact may arrive only if grounded; ordinary Carrow/household/social life remains equally valid. No engine is owed on a timer.",
    "threads rotation",
)
p.write_text(o)

p = Path("state/MANUSCRIPT_CHAPTER_INDEX.md")
i = p.read_text()
i, n = re.subn(r"# PEG-LEG GREG — CHAPTER INDEX — CH\d+", "# PEG-LEG GREG — CHAPTER INDEX — CH233", i, count=1)
assert n == 1
i, n = re.subn(r"\*\*Current endpoint:\*\* Chapter \d+ — [^\n]+", "**Current endpoint:** Chapter 233 — THE SEAT", i, count=1)
assert n == 1
assert "232. **THE COUNTERSIGN**" in i
assert "232. **THE MATCHER**" not in i
assert "233. **THE SEAT**" not in i
i = i.rstrip() + "\n233. **THE SEAT**\n"
p.write_text(i)

p = Path("state/MANUSCRIPT_WORKFLOW.md")
w = p.read_text()
w = replace_once(w, "Chapter 232 — **THE COUNTERSIGN**.", "Chapter 233 — **THE SEAT**.", "workflow edge")
w = replace_once(w, "See `state/MANUSCRIPT_STATE.md` for current canon and the Chapter 233 edge.", "See `state/MANUSCRIPT_STATE.md` for current canon and the Chapter 234 edge.", "workflow next")
p.write_text(w)

p = Path("state/PROJECT_STATE.md")
q = p.read_text()
q = replace_once(q, "Current recorded story endpoint is Chapter 232 — **THE COUNTERSIGN**.", "Current recorded story endpoint is Chapter 233 — **THE SEAT**.", "project endpoint")
p.write_text(q)

print("chapter_words", words)
print("chapter_em_dashes", body.count("—"))
print("state_sync_ready", True)
