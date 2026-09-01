from pathlib import Path
import re

def one(t,a,b,n):
    c=t.count(a)
    if c!=1: raise SystemExit(f"{n}: {c}")
    return t.replace(a,b,1)

M=Path("state/manuscript/Peg_Leg_Greg_Running_Manuscript.md")
S=Path("state/MANUSCRIPT_STATE.md")
O=Path("state/OPEN_THREADS.md")
I=Path("state/MANUSCRIPT_CHAPTER_INDEX.md")
W=Path("state/MANUSCRIPT_WORKFLOW.md")
P=Path("state/PROJECT_STATE.md")
Q=Path("state/.ch236_distributor_payload.md")

ch=Q.read_text()
words=len(re.findall(r"\b[\w’'-]+\b",ch))
assert "# CHAPTER 236" in ch and "## THE DISTRIBUTOR" in ch
assert 2500<=words<=4000, words
assert "—" not in ch

m=M.read_text()
assert "# CHAPTER 236" not in m
M.write_text(m.rstrip()+"\n\n------------------------------------------------------------------------\n\n"+ch.strip()+"\n")

s=S.read_text()
s=one(s,"- Current story endpoint: Chapter 235 — **THE TAGALONG**.","- Current story endpoint: Chapter 236 — **THE DISTRIBUTOR**.","endpoint")
s=one(s,"- Chapter 235 contains no Hessa appearance or magic attempt. Counts remain 34 / 30 / 49 and all restrictions remain unchanged.","- Chapter 235 contains no Hessa appearance or magic attempt. Counts remain 34 / 30 / 49 and all restrictions remain unchanged.\n- Chapter 236 contains no Hessa appearance or magic attempt. Counts remain 34 / 30 / 49 and all restrictions remain unchanged.","magic")
s=one(s,"- Ch235 Lyssa is still home in the morning and invites Greg along on ordinary west-market household errands. She later leaves directly for north-side work and returns after dark with the beans she carried north and no bundle; no customer, garment, or work purpose is established. The narrow brown cloth remains same fold/three pins and Greg's damaged shirt remains on the shelf with three loose threads.","- Ch235 Lyssa is still home in the morning and invites Greg along on ordinary west-market household errands. She later leaves directly for north-side work and returns after dark with the beans she carried north and no bundle; no customer, garment, or work purpose is established. The narrow brown cloth remains same fold/three pins and Greg's damaged shirt remains on the shelf with three loose threads.\n- Ch236 Lyssa is gone before Greg's morning theatre call; the new bean bag is also gone. She returns after dark with no beans and no bundle, leaving their purpose unresolved. Brown cloth remains same fold/three pins; damaged shirt remains three loose threads.","lyssa")
s=one(s,"- Ch235 contains no Vale appearance, office work, payment, or debt credit. Greg and Lyssa make ordinary household/food purchases while the debt remains active and unstated.","- Ch235 contains no Vale appearance, office work, payment, or debt credit. Greg and Lyssa make ordinary household/food purchases while the debt remains active and unstated.\n- Ch236 contains no Vale appearance, office work, payment, or debt credit. Rinna pays Greg the normal one copper for theatre work; debt remains active and unstated.","economy")
s=one(s,"- Chapters 224–235 do not advance the pressure arc. In Ch228 Olin simply sends the theatre's oil with no message, question, warning, or stranger attached. Bren remains off-page. No Mason's Cut investigation and no Vale-paper clue.","- Chapters 224–235 do not advance the pressure arc after the Ch223 cart-repair report. Ch236 adds one grounded fact: a brown-coat, dark-haired, narrow-faced, quiet-voiced unknown man asks the lamp-glass seller whether she supplies the theatre, whether deliveries use the front or back, and who opens for deliveries. She gives no useful answer. Rinna classifies the description only as consistent with Olin's; identity, Bren connection, plan, organization, and intent remain unproved. No Mason's Cut investigation and no Vale connection.","pressure")
a=s.index("## Immediate next edge — Chapter 236")
b=s.index("## Chat / handoff behavior",a)
TAIL='''## Chapter 236 — THE DISTRIBUTOR
- A new theatre call arrives through an unnamed boy: Rinna asks Greg to come before midday if free. She gives him a five-stop handbill route rather than a performance role.
- Greg makes one ordinary route mistake by leaving seven bills at the tea room instead of five; a girl sweeping there catches the overcount and returns two. The Red Lane cobbler takes only three and the West Gate bread stall refuses because its notice space is full.
- The lamp-glass seller reports one new pressure fact: an unknown brown-coat, dark-haired, narrow-faced, quiet-voiced man asks whether she supplies the theatre, then asks `Do they take deliveries through the front or the back?` and who opens for deliveries. She gives no useful answer. He gives no name, buys nothing, makes no threat, offers no money, and does not ask about empty hours, money, the cart, or Bren.
- Rinna records the description only as **consistent with Olin's**, not confirmed identity. The supported pressure category now includes a question about theatre delivery/access procedure. No entry plan, robbery, ambush, Bren employment, organization, boss, Mason's Cut base, or Vale connection is established.
- Theatre remains work around the fact. Nessa separately reports the back latch still sticks; it is to be fixed because it sticks. Greg helps Jori and Davin hold/adjust a narrow door frame and receives the normal one copper for the workday.
- Nessa gives Greg a short dark-green coat and Rinna gives him **The Missing Key** pages for tomorrow. Greg is Messenger: eight lines, three entrances. Tomorrow morning rehearsal is firm; performance is conditional on Teren keeping the piece paired.
- No Hessa or magic attempt and no Vale work/credit. Magic remains **34 / 30 / 49** with all restrictions unchanged; debt remains active and unstated.
- Lyssa is gone before the morning call. The new bean bag from Ch235 is also gone and she returns after dark without it or a bundle, leaving the beans' purpose unexplained. Brown cloth remains same fold/three pins; damaged shirt remains three loose threads.

## Immediate next edge — Chapter 237
Primary recommendation: **FULFILL THE CONCRETE THEATRE OBLIGATION EARNED IN CH236. LET THE NEW PRESSURE FACT REMAIN RECORDED RATHER THAN TURNING REHEARSAL INTO AN INVESTIGATION.**

Theatre has the actual next claim: Greg has the Messenger pages for **The Missing Key**, eight lines, three entrances, Nessa's short dark-green coat, and a firm morning rehearsal. Performance happens only if Teren keeps the piece paired. Make the next chapter theatre first: rehearsal, scene partners, entrances, costume/prop/route geometry, a theatre-specific mistake or correction, and audience only if the piece genuinely performs.

Do not stack another brown-coat clue on a timer. Ch236 already moved pressure by one grounded access/logistics question and preserved the evidence ceiling. Magic should continue to breathe unless a new bounded Hessa question genuinely arrives; Hessa still has no selected experiment. Vale debt remains active but there is no current Vale obligation. The beans' purpose remains unknown, the brown cloth remains unidentified, the damaged shirt remains at three loose threads, and **Marra ≠ Maren**.

Preserve magic counts **34 / 30 / 49**, all restrictions, active unstated Vale debt, the description-match versus identity distinction, Greg's ordinary body continuity, Lyssa's independent work boundaries, and the absence of formal Marra/Jessa roles.'''
S.write_text(s[:a].rstrip()+"\n\n"+TAIL+"\n\n"+s[b:])

o=O.read_text()
o=one(o,"- **Current endpoint:** Chapter 235 — **THE TAGALONG**.","- **Current endpoint:** Chapter 236 — **THE DISTRIBUTOR**.","open endpoint")
o=one(o,"- **Threat restraint:** Chapters 224–235 contain no new warning, demand, appearance, violence, sabotage, or investigation. Ch228 Olin simply sends ordinary oil with no message or warning attached.","- **Threat restraint through Ch235:** Chapters 224–235 contain no new warning, demand, appearance, violence, sabotage, or investigation after the Ch223 report.\n- **Ch236 lamp-glass fact:** an unknown brown-coat, dark-haired, narrow-faced, quiet-voiced man asks whether the seller supplies the theatre, `Do they take deliveries through the front or the back?`, and who opens for deliveries. She gives no useful answer. Rinna records the description only as consistent with Olin's. This adds a delivery/access-procedure question, not a confirmed identity, entry plan, robbery plan, Bren employment, organization, or Vale connection.","open threat")
old="- **Ch235 magic/Vale/theatre/pressure:** no Hessa or magic attempt, no Vale work/credit, no theatre work/call, and no Bren/brown-coat movement. Magic remains 34 / 30 / 49.\n- **Next engine rotation:** Ch235 supplies a full ordinary Greg/Lyssa/Carrow day after the Ch234 Hessa session. Follow the next actual obligation or social pressure; theatre, Vale, threat, friendship, or continued ordinary life are all available only if the day earns them. Magic should not reopen on a timer."
new="- **Ch235 magic/Vale/theatre/pressure:** no Hessa or magic attempt, no Vale work/credit, no theatre work/call, and no Bren/brown-coat movement. Magic remains 34 / 30 / 49.\n- **Ch236 theatre/work:** a new Rinna call produces a five-stop handbill route, one ordinary overcount corrected by a tea-room girl, later door-frame work with Jori/Davin, and normal one-copper pay.\n- **Ch236 next obligation:** Greg has **The Missing Key** Messenger pages, eight lines, three entrances, and Nessa's short dark-green coat. Tomorrow morning rehearsal is firm; performance remains conditional on Teren keeping the piece paired.\n- **Ch236 household/body/magic/Vale:** ordinary route/work fatigue only, no injury. Beans disappear off-page with purpose unresolved; brown cloth stays same fold/three pins; damaged shirt stays three loose threads. No Hessa/magic or Vale work/credit. Magic remains 34 / 30 / 49.\n- **Next engine rotation:** Chapter 237 has a concrete theatre obligation already earned by prose. Let the Ch236 pressure fact remain recorded rather than stacking another clue on a timer."
o=one(o,old,new,"open ch236")
O.write_text(o)

i=I.read_text().rstrip()
assert i.endswith("235. **THE TAGALONG**")
I.write_text(i+"\n236. **THE DISTRIBUTOR**\n")

w=W.read_text()
w=one(w,"Chapter 235 — **THE TAGALONG**.\n\nSee `state/MANUSCRIPT_STATE.md` for current canon and the Chapter 236 edge.","Chapter 236 — **THE DISTRIBUTOR**.\n\nSee `state/MANUSCRIPT_STATE.md` for current canon and the Chapter 237 edge.","workflow")
W.write_text(w)

p=P.read_text()
P.write_text(one(p,"Current recorded story endpoint is Chapter 235 — **THE TAGALONG**.","Current recorded story endpoint is Chapter 236 — **THE DISTRIBUTOR**.","project"))

print("chapter_words",words)
print("em_dashes",ch.count("—"))
