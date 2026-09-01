from pathlib import Path
import re

PAYLOAD = Path("state/.ch235_tagalong_payload.md")
MANUSCRIPT = Path("state/manuscript/Peg_Leg_Greg_Running_Manuscript.md")
STATE = Path("state/MANUSCRIPT_STATE.md")
THREADS = Path("state/OPEN_THREADS.md")
INDEX = Path("state/MANUSCRIPT_CHAPTER_INDEX.md")
WORKFLOW = Path("state/MANUSCRIPT_WORKFLOW.md")
PROJECT = Path("state/PROJECT_STATE.md")

chapter = PAYLOAD.read_text().strip()
assert chapter.startswith("------------------------------------------------------------------------\n\n# CHAPTER 235\n\n## THE TAGALONG")
assert chapter.endswith("I stayed anyway.")
assert chapter.count("—") == 0

m = MANUSCRIPT.read_text()
assert "# CHAPTER 235" not in m
assert m.rstrip().endswith("For once, the most reliable thing in the room was not the paper.")
MANUSCRIPT.write_text(m.rstrip() + "\n\n" + chapter + "\n")

s = STATE.read_text()
assert "Current story endpoint: Chapter 234 — **THE CONDITION**." in s
s = s.replace("Current story endpoint: Chapter 234 — **THE CONDITION**.",
              "Current story endpoint: Chapter 235 — **THE TAGALONG**.", 1)
magic_anchor = "- Hessa ends Ch234 with no chosen next experiment. Her possible next questions remain unresolved."
assert magic_anchor in s
s = s.replace(magic_anchor, magic_anchor + "\n- Chapter 235 contains no Hessa appearance or magic attempt. Counts remain 34 / 30 / 49 and all restrictions remain unchanged.", 1)
lyssa_anchor = "- Ch234 the narrow brown cloth remains in the same fold with the same three pins. Greg's damaged shirt remains on the shelf with three loose threads and is not repaired. Lyssa is off-page through the experiment day, returns tired in an ordinary non-medical way with no bundle, and asks only the narrow result questions `Paper?`, `Out of four?`, and `Same distance?`; she does not become Hessa's analyst."
assert lyssa_anchor in s
s = s.replace(lyssa_anchor, lyssa_anchor + "\n- Ch235 Lyssa is still home in the morning and invites Greg along on ordinary west-market household errands. She later leaves directly for north-side work and returns after dark with the beans she carried north and no bundle; no customer, garment, or work purpose is established. The narrow brown cloth remains same fold/three pins and Greg's damaged shirt remains on the shelf with three loose threads.", 1)
econ_anchor = "- Ch234 contains no Vale appearance, office work, payment, or debt credit. Greg buys ordinary breakfast and cheese while the debt remains active and unstated."
assert econ_anchor in s
s = s.replace(econ_anchor, econ_anchor + "\n- Ch235 contains no Vale appearance, office work, payment, or debt credit. Greg and Lyssa make ordinary household/food purchases while the debt remains active and unstated.", 1)
s = s.replace("Chapters 224–234 do not advance the pressure arc.", "Chapters 224–235 do not advance the pressure arc.", 1)
start = s.index("## Immediate next edge — Chapter 235")
end = s.index("## Chat / handoff behavior", start)
summary = '''## Chapter 235 — THE TAGALONG
- Chapter 235 deliberately lets the full Ch234 magic session breathe. No Hessa appearance, magic attempt, theatre work, Vale work/debt credit, Bren/brown-coat fact, warning, investigation, or escalation occurs. Magic counts remain **34 / 30 / 49** and all restrictions remain unchanged.
- Lyssa is still home when Greg wakes and is not actively sewing. She invites him along to the west market because she is going, not because he has an assigned job. The morning functions as ordinary couple time rather than plot debrief.
- Greg and Lyssa buy ordinary household food/oil. Lyssa's existing market familiarity is visible in narrow form: a pear seller knows her, a bean seller uses compressed ordinary trade with her, but no formal customer/network status is invented.
- At Olin's, the visit is completely ordinary. Lyssa buys household lamp oil; Olin gives no warning, message, threat update, or new information. The prior pressure arc remains quiet.
- Greg's disability remains materially ordinary in crowd/carrying geometry: bread/oil/bag arrangements interact with two crutches; Lyssa carries the heavier/more awkward shared load without an accommodation speech. Greg has ordinary worked shoulders/right hand only and no injury or new limitation.
- Lyssa leaves directly for north-side work after the market. She carries the newly bought beans with her for an unexplained workday reason; Greg does not turn that into a professional question. She returns after dark with the beans and no bundle. Customer, garment, and job details remain off-page.
- Greg spends the afternoon genuinely unassigned, trims the household lamp wick, naps in a chair, cooks the older beans, and eats his portion without waiting for Lyssa. This reinforces that not waiting for supper can coexist with care rather than becoming relationship distance.
- The narrow brown cloth remains same fold / same three pins and wholly unidentified. Greg's damaged shirt remains on the shelf with three loose threads and is not repaired.
- Home ends with direct relationship texture rather than analysis: Greg tells Lyssa the shared morning was good; she agrees, steals his last piece of bread, and he stays anyway.

## Immediate next edge — Chapter 236
Primary recommendation: **FOLLOW THE NEXT ACTUAL OBLIGATION OR SOCIAL PRESSURE. DO NOT IMMEDIATELY TURN CH235'S ORDINARY COUPLE DAY INTO ANOTHER DOMESTIC CHAPTER BY ROTATION.**

Reasons:
- Ch232 foregrounded Vale/debt work, Ch233 theatre/company life, Ch234 magic evidence, and Ch235 ordinary Greg/Lyssa/Carrow life. The recent sequence has touched all major engines without requiring any one to fire again on schedule.
- Magic should breathe after Ch234. Hessa still has no selected next experiment, and Ch235 creates no reason to reopen testing.
- Theatre has no standing obligation from Ch233–235. It may return only through a genuinely new call or ordinary need.
- Vale work remains available only when suitable work exists. Greg has no schedule or post.
- External pressure has remained quiet through Ch235. One grounded fact through an established commercial contact is available if it naturally arrives, but elapsed chapters still do not create an escalation quota.
- Lyssa's brown cloth and Greg's three-thread damaged shirt remain intentionally unresolved. Do not clean them up merely because they persist.
- Ch235 establishes a pleasant shared morning, not a new daily routine. Lyssa's north-side work remains independent and unexplained.

Strong Chapter 236 possibilities:
- a concrete new theatre or Vale obligation if one actually arrives;
- one grounded pressure fact through Olin, Rinna, the cart repairer, lamp-glass supplier, or another established contact while ordinary work continues;
- another existing social/friend route not recently foregrounded;
- ordinary Carrow life if it has a real person/material problem rather than serving as filler.

Preserve magic counts **34 / 30 / 49** and all restrictions. Preserve active unstated Vale debt. Preserve the threat evidence ceiling. Preserve brown-cloth identity limits, three-thread shirt continuity, Lyssa customer/garment boundaries, and **Marra ≠ Maren**.

'''
s = s[:start] + summary + s[end:]
STATE.write_text(s)

t = THREADS.read_text()
assert "**Current endpoint:** Chapter 234 — **THE CONDITION**." in t
t = t.replace("**Current endpoint:** Chapter 234 — **THE CONDITION**.",
              "**Current endpoint:** Chapter 235 — **THE TAGALONG**.", 1)
t = t.replace("**Threat restraint:** Chapters 224–234 contain no new warning, demand, appearance, violence, sabotage, or investigation.",
              "**Threat restraint:** Chapters 224–235 contain no new warning, demand, appearance, violence, sabotage, or investigation.", 1)
next_anchor = "- **Next engine rotation:** let the full Ch234 Hessa session breathe. Ordinary Carrow/household/social life, one grounded pressure fact, or an actual new work obligation are available; none is owed on a timer."
assert next_anchor in t
thread_add = '''- **Ch235 ordinary Greg/Lyssa day:** Lyssa is home in the morning and invites Greg along to the west market because she is going. They buy household food/oil, share flat cakes, and separate when Lyssa heads north for her own work. No formal Lyssa-work role or customer identity is established.
- **Ch235 Olin:** household oil purchase is completely ordinary. Olin gives no warning, message, stranger report, or new pressure evidence.
- **Ch235 body/household:** ordinary crowd/carry geometry only; no injury. Brown cloth remains same fold/three pins. Damaged shirt remains on the shelf with three loose threads. Lyssa returns after dark with the beans she carried north and no bundle; reason/customer/job remains unestablished.
- **Ch235 magic/Vale/theatre/pressure:** no Hessa or magic attempt, no Vale work/credit, no theatre work/call, and no Bren/brown-coat movement. Magic remains 34 / 30 / 49.
'''
t = t.replace(next_anchor, thread_add + "- **Next engine rotation:** Ch235 supplies a full ordinary Greg/Lyssa/Carrow day after the Ch234 Hessa session. Follow the next actual obligation or social pressure; theatre, Vale, threat, friendship, or continued ordinary life are all available only if the day earns them. Magic should not reopen on a timer.", 1)
THREADS.write_text(t)

idx = INDEX.read_text()
assert "# PEG-LEG GREG — CHAPTER INDEX — CH234" in idx
assert "**Current endpoint:** Chapter 234 — THE CONDITION" in idx
assert "235. **THE TAGALONG**" not in idx
idx = idx.replace("# PEG-LEG GREG — CHAPTER INDEX — CH234", "# PEG-LEG GREG — CHAPTER INDEX — CH235", 1)
idx = idx.replace("**Current endpoint:** Chapter 234 — THE CONDITION", "**Current endpoint:** Chapter 235 — THE TAGALONG", 1)
INDEX.write_text(idx.rstrip() + "\n235. **THE TAGALONG**\n")

w = WORKFLOW.read_text()
assert "Chapter 234 — **THE CONDITION**." in w
WORKFLOW.write_text(w.replace("Chapter 234 — **THE CONDITION**.", "Chapter 235 — **THE TAGALONG**.", 1))

p = PROJECT.read_text()
assert "Current recorded story endpoint is Chapter 234 — **THE CONDITION**." in p
PROJECT.write_text(p.replace("Current recorded story endpoint is Chapter 234 — **THE CONDITION**.",
                             "Current recorded story endpoint is Chapter 235 — **THE TAGALONG**.", 1))

m2 = MANUSCRIPT.read_text()
assert m2.count("# CHAPTER 235") == 1
ch = m2[m2.index("# CHAPTER 235"):]
words = len(re.findall(r"\b[\w’'-]+\b", ch))
assert 2500 <= words <= 4000, words
assert ch.count("—") == 0
assert "## THE TAGALONG" in ch
assert ch.rstrip().endswith("I stayed anyway.")
assert "Current story endpoint: Chapter 235 — **THE TAGALONG**." in STATE.read_text()
assert "34 successful supervised minimal draws." in STATE.read_text()
assert "30 supervised deliberate shaping attempts." in STATE.read_text()
assert "49 supervised external-effect attempts." in STATE.read_text()
assert "235. **THE TAGALONG**" in INDEX.read_text()
assert "Chapter 235 — **THE TAGALONG**." in WORKFLOW.read_text()
assert "Current recorded story endpoint is Chapter 235 — **THE TAGALONG**." in PROJECT.read_text()
assert "**Current endpoint:** Chapter 235 — **THE TAGALONG**." in THREADS.read_text()
print("chapter_words", words)
print("em_dashes", ch.count("—"))
