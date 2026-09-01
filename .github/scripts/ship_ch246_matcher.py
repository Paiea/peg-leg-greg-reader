from pathlib import Path
import re

def read(p): return Path(p).read_text(encoding="utf-8")
def write(p, s): Path(p).write_text(s, encoding="utf-8")

chapter = read(".github/ch246_payload.md").strip()
assert chapter.startswith("# CHAPTER 246\n\n## THE MATCHER")
assert chapter.endswith("I left the spool alone.")

# Permanent manuscript
mp = "state/manuscript/Peg_Leg_Greg_Running_Manuscript.md"
m = read(mp)
assert "# CHAPTER 245\n\n## THE NAME-TAKER" in m
assert "# CHAPTER 246" not in m
m = m.rstrip() + "\n\n------------------------------------------------------------------------\n\n" + chapter + "\n"
write(mp, m)

# Manuscript state
sp = "state/MANUSCRIPT_STATE.md"
s = read(sp)
assert "Current story endpoint: Chapter 245 — **THE NAME-TAKER**." in s
s = s.replace("Current story endpoint: Chapter 245 — **THE NAME-TAKER**.",
              "Current story endpoint: Chapter 246 — **THE MATCHER**.", 1)
marker = "## Immediate next edge — Chapter 246"
chat = "## Chat / handoff behavior"
assert marker in s and chat in s
before, rest = s.split(marker, 1)
_, after_chat = rest.split(chat, 1)
entry = """## Chapter 246 — THE MATCHER
- Chapter 246 lets Ch245's Vale front-room day breathe. No Vale appearance/work/credit, theatre call/work/pay, Hessa appearance/magic attempt, or Bren/brown-coat movement occurs. Magic remains **35 / 31 / 53** with all restrictions unchanged; debt remains active/unstated; Ch236 remains the newest pressure fact.
- Lyssa gives Greg one bounded Maren errand: a small dull reddish-brown cloth sample, the nearly empty old spool, and `If exact, exact. If not, darker.` Customer, garment, ownership, and exact use remain unestablished. The sample is separate from the long-standing brown cloth and absent Ch241 dark cloth.
- The same counter woman from Ch222 remembers Greg narrowly as `Blue last time`. This establishes Greg-specific shop memory only. Her name remains unestablished; `Maren` is still not established as her personal name; no personal seller/Lyssa relationship is established.
- Maren's has independent customers and finite stock. The exact match is unavailable. The counter woman owns matching judgment; Greg initially misreads one match in indoor light, then follows Lyssa's narrow darker-if-not-exact instruction and chooses between two near options after checking them outside. He does not become Lyssa's garment analyst or standing supply runner.
- A thread-delivery crate arrives immediately after Greg pays. Greg leaves without learning its contents. It is NOT established that the exact shade was inside or that he missed a better purchase.
- Greg pays ordinary money for one spool. Body/equipment remain ordinary: repaired LEFT tip / LEFT grip normal, retensioned RIGHT grip functionally invisible, no injury or new limitation.
- At home Lyssa calls the substitute `Close` and does not identify the customer/garment or begin a procedural sewing scene. Brown cloth remains same fold/three pins; damaged shirt remains three loose threads; better shirt retains the blue streak; Ch241 dark cloth, older beans, and older wrapped item remain absent/unexplained."""

edge = """## Immediate next edge — Chapter 247
Primary recommendation: **LET CH246'S SMALL MAREN SUPPLY-ROUTE DAY BREATHE. FOLLOW THE NEXT ACTUAL CLAIM RATHER THAN TURNING NARROW SHOP RECOGNITION, THE NEW SAMPLE, THE DELIVERY CRATE, OR ANY RECENT MAYBE INTO AN AUTOMATIC NEXT STEP.**

- Maren's now carries one narrow Greg-specific memory: `Blue last time`. No friendship, standing errand role, seller name, or personal seller/Lyssa relationship is established.
- The Ch246 sample remains low-information. Customer, garment, ownership, exact use, and delivery-crate contents remain unestablished. Do not merge the sample with the long-standing brown cloth, Ch241 dark cloth, or older blue-gray material.
- **The Guest Pot** remains `Not paired yet`; Uncle / same-piece return remain only `Maybe`.
- Vale debt remains active/unstated. Ch245's credit creates no tomorrow, schedule, rate, promotion, or standing front-room role.
- Magic remains **35 / 31 / 53**. Attempt 52 remains one clean FAR/AWAY response; no rate, range, equivalence, generalization, or new permission. Hessa still has no selected next experiment.
- External pressure still last moved in Ch236; no Vale/Bren connection exists.

Ask: **WHAT ACTUALLY HAS A REASON TO HAPPEN TODAY?** Favor **LIFE PER WORD**."""
s = before.rstrip() + "\n\n" + entry + "\n\n" + edge + "\n\n" + chat + after_chat
write(sp, s)

# Open threads
op = "state/OPEN_THREADS.md"
ot = read(op)
assert "**Current endpoint:** Chapter 245 — **THE NAME-TAKER**." in ot
ot = ot.replace("**Current endpoint:** Chapter 245 — **THE NAME-TAKER**.",
                "**Current endpoint:** Chapter 246 — **THE MATCHER**.", 1)
old = "- **Next engine rotation:** let Ch245's fresh Vale front-room workday breathe. Do not convert the name list into a standing job, resurrect the conditional Guest Pot, or turn Attempt 52 into an automatic next step; follow the next actual claim."
new = "- **Next engine rotation:** let Ch246's small Maren supply-route day breathe. Do not turn narrow shop recognition into a standing errand role, service the new sample / delivery crate by checklist, resurrect recent maybes, or turn Attempt 52 into an automatic next step; follow the next actual claim."
assert old in ot
ot = ot.replace(old, new, 1)
bullets = """
- **Ch246 Maren return:** Lyssa sends Greg with a small dull reddish-brown sample and nearly empty spool, instructing `If exact, exact. If not, darker.` Sample customer/garment/ownership/use remain unestablished and it is separate from the long-standing brown cloth / absent Ch241 dark cloth.
- **Ch246 Maren social residue:** the same counter woman from Ch222 remembers Greg narrowly as `Blue last time`. Seller name remains unknown; `Maren` is not established as her personal name; no personal seller/Lyssa relationship is established.
- **Ch246 stock / authority ceiling:** exact match unavailable; other customers demonstrate finite stock and independent shop history. Counter woman owns matching judgment. Greg follows Lyssa's narrow instruction and does not become a garment analyst or standing supply runner.
- **Ch246 delivery ceiling:** a thread-delivery crate arrives immediately after Greg pays, but he leaves without learning its contents. Do not claim the exact shade was inside or turn the crate into a mystery.
- **Ch246 restraint / household:** no Vale, theatre, Hessa/magic, or pressure movement. Magic remains 35 / 31 / 53; debt active/unstated; Ch236 newest pressure evidence. Brown cloth same fold/three pins; damaged shirt three loose threads; better shirt blue streak; Ch241 dark cloth / old beans / older wrapped item absent or unexplained. Lyssa calls the substitute thread `Close`."""
assert "**Ch246 Maren return:**" not in ot
ot = ot.rstrip() + "\n" + bullets.strip() + "\n"
write(op, ot)

# Chapter index
ip = "state/MANUSCRIPT_CHAPTER_INDEX.md"
idx = read(ip)
assert "# PEG-LEG GREG — CHAPTER INDEX — CH245" in idx
assert "**Current endpoint:** Chapter 245 — THE NAME-TAKER" in idx
assert "246. **THE MATCHER**" not in idx
idx = idx.replace("# PEG-LEG GREG — CHAPTER INDEX — CH245",
                  "# PEG-LEG GREG — CHAPTER INDEX — CH246", 1)
idx = idx.replace("**Current endpoint:** Chapter 245 — THE NAME-TAKER",
                  "**Current endpoint:** Chapter 246 — THE MATCHER", 1)
idx = idx.rstrip() + "\n246. **THE MATCHER**\n"
write(ip, idx)

# Workflow
wp = "state/MANUSCRIPT_WORKFLOW.md"
w = read(wp)
assert "Chapter 245 — **THE NAME-TAKER**." in w
assert "Chapter 246 edge." in w
w = w.replace("Chapter 245 — **THE NAME-TAKER**.",
              "Chapter 246 — **THE MATCHER**.", 1)
w = w.replace("Chapter 246 edge.", "Chapter 247 edge.", 1)
write(wp, w)

# Project state
pp = "state/PROJECT_STATE.md"
p = read(pp)
assert "Current recorded story endpoint is Chapter 245 — **THE NAME-TAKER**." in p
p = p.replace("Current recorded story endpoint is Chapter 245 — **THE NAME-TAKER**.",
              "Current recorded story endpoint is Chapter 246 — **THE MATCHER**.", 1)
write(pp, p)

# Dedicated work-network audit
ap = "state/LYSSA_WORK_NETWORK_AUDIT.md"
a = read(ap)
anchor = "- **Maren**, a separate spool-sign thread/garment shop in Chapter 222 where Greg can present a cloth sample for matching thread and Lyssa later says `Maren usually does.`"
assert anchor in a
assert "**Chapter 246:** the same Maren counter woman" not in a
note = "- **Chapter 246:** the same Maren counter woman remembers Greg narrowly as `Blue last time` when he returns with another sample. This graduates one small Greg/shop familiarity fact only. Her name remains unestablished; `Maren` is still not established as her personal name; no personal recognition of Lyssa by that seller is established; the shop remains a lighter supply node rather than a socially dense relationship."
a = a.replace(anchor, anchor + "\n" + note, 1)
write(ap, a)

# Fresh chapter checks
ch = read(mp).split("# CHAPTER 246", 1)[1]
words = len(re.findall(r"\b\w[\w'’-]*\b", ch))
emdashes = ch.count("—")
assert words == 2605, words
assert emdashes == 0, emdashes
print(f"CH246_WORDS={words}")
print(f"CH246_EMDASHES={emdashes}")
