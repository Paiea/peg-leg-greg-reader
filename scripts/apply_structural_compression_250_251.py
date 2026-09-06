#!/usr/bin/env python3
from __future__ import annotations

import argparse, html, json, re
from pathlib import Path

PATHS = {
    250: [Path("chapters/250.html"), Path("light/250.html")],
    251: [Path("chapters/251.html"), Path("light/251.html")],
}
ARTICLE_RE = re.compile(r'(<article class="prose(?: light-prose)?">)(.*?)(</article>)', re.I | re.S)
P_RE = re.compile(r'<p(?:\s[^>]*)?>(.*?)</p>', re.I | re.S)
TAG_RE = re.compile(r'<[^>]+>')


def norm(s): return re.sub(r'\s+', ' ', html.unescape(TAG_RE.sub('', re.sub(r'<br\s*/?>',' ',s,flags=re.I)))).strip()
def wc(ps): return sum(len(re.findall(r"\b\w+[’'-]?\w*\b",p)) for p in ps)

def idx(ps,cue):
    m=[i for i,p in enumerate(ps) if cue in p]
    if len(m)!=1: raise ValueError(f"cue {cue!r}: {len(m)} matches")
    return m[0]

def repl(ps,a,b,new):
    i,j=idx(ps,a),idx(ps,b)
    if j<=i: raise ValueError(f"bad range {a} -> {b}")
    return ps[:i]+new+ps[j:]

CH250_HOME=[
    "Lyssa was already dressed. The reddish-brown sample had disappeared from the table; the darker spool had moved into use. The groceries had survived breakfast, including the cheese I had called acceptable yesterday.",
    "Lyssa caught me eating it. “Good?”",
    "“Improving.”",
    "“You said acceptable.”",
    "“It has had time to develop.”",
    "“Since yesterday?”",
    "“Important period for cheese.”",
    "She took a piece. That ended the review.",
]
CH250_ROUTE=[
    "Marek waited for me on the stairs badly, meaning he kept moving slowly and called it waiting. Outside, the haircut remained a strategic error in the cold. He noticed, approved of the haircut, then ruined the compliment with, “More head.”",
    "We took the wider route toward the theatre. Marek knew it now without asking. Somewhere along the way, accommodation had become route.",
    "I was still carrying Nessa's damaged hat because Marek had transferred responsibility to me the instant he reached my house. He called this successful delivery. I called it a succession crisis.",
]
CH251_LINES=[
    "The remaining lines did not yield evenly. One came back as soon as Lyssa supplied Hara's cue. Another had fused itself to Pell's habitual pause. The last stubborn one sat between a joke I knew and Hara's answer I also knew, leaving a clean blank where my own words belonged.",
    "Lyssa took the pages and cued me from the other parts. She read every character as Lyssa. The young wife sounded like Lyssa. The brother sounded like Lyssa. The servant sounded like Lyssa with less patience.",
    "“You are ruining the company,” I said.",
    "“Line.”",
    "We worked backward two lines whenever I missed. That was more useful than repeating the blank itself. By the end, the last three lines were present at the table, which was not the same thing as having them in a scene.",
    "Forty-three lines. Probably.",
]
CH251_ARRIVAL=[
    "The walk to the theatre proved the distinction immediately. Lines I had owned at the table vanished while I moved uphill on crutches, returned out of order, then disappeared again when I tried to count them.",
    "At the theatre, Pell was still sick but improving. The stage was half lit, Jori was tightening the dinner table, and Nessa told me Teren wanted the whole piece after warm-up. Pages would be available, not forbidden.",
    "My widened chalk mark from yesterday was still there. Marek arrived without the hat because Nessa had already recovered it from the prop shelf after he lost it during cleanup. Different kind of learning.",
]
CH251_TIMING=[
    "We ran the whole piece. Once the words stopped being the main emergency, timing became one. I started stepping on the ends of other people's lines because I already knew what came next.",
    "Teren stopped me. “Then stop proving it.”",
    "I waited longer. Too long. Marek looked toward the wing.",
    "“Not that long,” Teren said.",
    "Useful range. We found it.",
]

def transform_paragraphs(n, ps):
    out=list(ps)
    if n==250:
        if any('OLD_HOUSEHOLD_INVENTORY_LOOP' in p for p in out): out=repl(out,'Lyssa was already dressed.','Instead someone knocked.',CH250_HOME)
        elif not any('Important period for cheese.' in p for p in out): out=repl(out,'Lyssa was already dressed.','Instead someone knocked.',CH250_HOME)
        if any('OLD_WALK_TO_THEATRE_LOOP' in p for p in out): out=repl(out,'The theatre side door was already open.','Teren held out pages.', ['The theatre side door was already open.']+CH250_ROUTE)
        elif not any('accommodation had become route' in p for p in out): out=repl(out,'He had already reached the bottom landing.','The theatre side door was already open.',CH250_ROUTE)
    elif n==251:
        if any('OLD_LINE_BY_LINE_MEMORIZATION_LOOP' in p for p in out): out=repl(out,'The first missing line was in scene one','Forty-three lines. Probably.',CH251_LINES)
        elif not any('The remaining lines did not yield evenly.' in p for p in out): out=repl(out,'The first missing line was in scene one','Lyssa gave the pages back.',CH251_LINES+['Lyssa gave the pages back.'])
        if any('OLD_THEATRE_ARRIVAL_LOOP' in p for p in out): out=repl(out,'The walk gave me twenty minutes','Teren arrived before I could answer.',CH251_ARRIVAL)
        elif not any('Lines I had owned at the table vanished' in p for p in out): out=repl(out,'The walk gave me twenty minutes','Teren arrived before I could answer.',CH251_ARRIVAL)
        if any('OLD_TIMING_REHEARSAL_LOOP' in p for p in out): out=repl(out,'We ran the whole piece.','By midday, I could get through the play without pages.',CH251_TIMING)
        elif not any('timing became one' in p for p in out): out=repl(out,'We ran the whole piece.','By midday, I could get through the play without pages.',CH251_TIMING)
    else: raise ValueError(n)
    return out

def transform_html(text,n):
    m=ARTICLE_RE.search(text)
    if not m: raise ValueError('article missing')
    body=m.group(2); figs=re.findall(r'<figure\b.*?</figure>',body,re.I|re.S)
    ps=[norm(x.group(1)) for x in P_RE.finditer(body)]
    out=transform_paragraphs(n,ps)
    if out==ps: return text,ps,out
    new=''.join(f'<p>{html.escape(p,quote=False)}</p>' for p in out)
    # Art is advisory/held. Preserve assets without letting them define cuts.
    new+=''.join(figs)
    return text[:m.start(2)]+new+text[m.end(2):],ps,out

def verify(root):
    protected={250:['Pell is sick','Knowing a man’s cup','Knowing a man\'s cup','narrow side stool'],251:['Knowing and playing were apparently separate industries.','Because stopping is worse.','One belonged to Pell.']}
    for n, paths in PATHS.items():
        texts=[]
        for rel in paths:
            t=(root/rel).read_text(encoding='utf-8'); texts.append('\n'.join([norm(x.group(1)) for x in P_RE.finditer(ARTICLE_RE.search(t).group(2))]))
        for cue in protected[n]:
            if n==250 and cue=='Knowing a man’s cup': continue
            if not all(cue in t for t in texts): raise AssertionError(f'{n} missing {cue}')
        if texts[0]!=texts[1]: raise AssertionError(f'{n} illustrated/text prose diverged')
    print('250-251 illustrated/text prose agree and protected beats survive')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=Path('.')); ap.add_argument('--write',action='store_true'); ap.add_argument('--verify',action='store_true'); ap.add_argument('--manifest',type=Path); a=ap.parse_args(); root=a.root.resolve()
    if a.verify: verify(root); return
    stats={}
    for n,paths in PATHS.items():
        for rel in paths:
            p=root/rel; new,before,after=transform_html(p.read_text(encoding='utf-8'),n); stats[str(rel)]={'before_words':wc(before),'after_words':wc(after),'delta_words':wc(after)-wc(before)}
            if new!=p.read_text(encoding='utf-8'): p.write_text(new,encoding='utf-8')
    verify(root)
    man={'schema_version':1,'batch':'250-251','status':'applied','strength':'aggressive-on-repetition-preserve-distinct-role-progression','source_authority':'reader chapter prose with synchronized text-reader projection','stable_id_actions':{'plg-ch-000250':{'status':'active','action':'tightened_emergency_substitution'},'plg-ch-000251':{'status':'active','action':'tightened_understudy_to_performance'}},'illustration_policy':'advisory hold; art does not protect redundant prose or boundaries','stats':stats,'protected':{'250':['Pell sickness trigger','Greg moved from Steward to Uncle','Marek inherits Steward','crutch/stool staging adaptation'],'251':['Lyssa cue practice','table memory vs embodied performance','wrong-line recovery','stopping is worse','Greg stops copying Pell']}}
    if a.manifest:
        q=a.manifest if a.manifest.is_absolute() else root/a.manifest; q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps(man,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(man,indent=2))
if __name__=='__main__': main()
