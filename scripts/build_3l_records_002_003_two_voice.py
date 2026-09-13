#!/usr/bin/env python3
from __future__ import annotations

import hashlib, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sh(*args):
    subprocess.run(list(args), check=True)


def probe(path: Path) -> float:
    out = subprocess.check_output([
        'ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(path)
    ], text=True)
    return float(out.strip())


def silences(path: Path):
    p = subprocess.run([
        'ffmpeg','-hide_banner','-nostats','-i',str(path),'-af','silencedetect=noise=-42dB:d=0.06','-f','null','-'
    ], capture_output=True, text=True)
    events = re.findall(r'silence_(start|end):\s*([0-9.]+)', p.stderr)
    out=[]; start=None
    for kind,val in events:
        if kind=='start': start=float(val)
        elif start is not None:
            out.append((start,float(val))); start=None
    return out


def manuscript_body(record: str) -> str:
    text=(ROOT/'3l'/'manuscript'/f'record-{record}.md').read_text(encoding='utf-8')
    parts=text.split('\n\n',2)
    if len(parts)!=3: raise ValueError('unexpected manuscript header')
    return parts[2].strip()


def dialogue_paragraph_roles(record: str, text: str):
    paragraphs=[]; cursor=0
    for m in re.finditer(r'[^\n]+(?:\n(?!\n)[^\n]+)*', text):
        p=m.group(0); q=list(re.finditer(r'“.*?”',p,flags=re.S))
        if q: paragraphs.append((m.start(),m.end(),p,q))
    roles=[]
    if record=='002':
        speaker='dragon'
        for item in paragraphs:
            roles.append((item,speaker)); speaker='greg' if speaker=='dragon' else 'dragon'
    elif record=='003':
        # Opening repeated phrase and Greg's first question are both Greg; conversation alternates after that.
        for i,item in enumerate(paragraphs):
            if i<2: speaker='greg'
            else: speaker='dragon' if i%2==0 else 'greg'
            roles.append((item,speaker))
    else: raise ValueError(record)
    return roles


def role_spans(record: str, text: str):
    marks=['greg']*len(text)
    for ((pstart,pend,p,quotes),speaker) in dialogue_paragraph_roles(record,text):
        if speaker!='dragon': continue
        for q in quotes:
            for i in range(pstart+q.start(),pstart+q.end()): marks[i]='dragon'
    spans=[]
    for i,role in enumerate(marks):
        if not spans or spans[-1]['role']!=role:
            spans.append({'start':i,'end':i+1,'role':role})
        else: spans[-1]['end']=i+1
    return spans


def spoken_fraction(text: str, pos: int):
    total=sum(not c.isspace() for c in text)
    return 0 if not total else sum(not c.isspace() for c in text[:pos])/total


def nearest_ordered(targets, candidates):
    if len(candidates)<len(targets): return targets
    # monotone greedy is sufficient because transitions are already ordered and silence density is high.
    out=[]; lo=0
    for t in targets:
        choices=[(abs(c-t),j,c) for j,c in enumerate(candidates[lo:],start=lo)]
        if not choices: return targets
        _,j,c=min(choices); out.append(c); lo=j+1
    return out


def timed_spans(text: str, spans, audio: Path):
    dur=probe(audio)
    mids=sorted((a+b)/2 for a,b in silences(audio) if 0<(a+b)/2<dur)
    targets=[dur*spoken_fraction(text,s['start']) for s in spans[1:]]
    times=nearest_ordered(targets,mids)
    if len(times)!=len(targets): raise ValueError('transition mapping failed')
    bounds=[0.0]+times+[dur]
    return [dict(s,start_seconds=bounds[i],end_seconds=bounds[i+1]) for i,s in enumerate(spans)]


def render(record: str, manifest: dict):
    text=manuscript_body(record)
    spans=role_spans(record,text)
    dragon_count=sum(1 for s in spans if s['role']=='dragon')
    if dragon_count<10: raise ValueError(f'{record}: suspiciously few dragon spans: {dragon_count}')

    work=ROOT/'.tmp-3l-audio'; work.mkdir(exist_ok=True)
    deep=work/f'{record}-deep.mp3'; normal=work/f'{record}-normal.mp3'
    for key,path in [('greg_full_audio_url',deep),('dragon_full_audio_url',normal)]:
        sh('curl','-L','--fail','--retry','3','-o',str(path),manifest[record][key])
        sh('ffmpeg','-v','error','-i',str(path),'-f','null','-')

    td=timed_spans(text,spans,deep); tn=timed_spans(text,spans,normal)
    if len(td)!=len(tn): raise ValueError('source maps differ')

    filters=[]; inputs=['-i',str(deep),'-i',str(normal)]; labels=[]
    for i,(a,b) in enumerate(zip(td,tn)):
        src=0 if a['role']=='greg' else 1
        chosen=a if a['role']=='greg' else b
        st=float(chosen['start_seconds']); en=float(chosen['end_seconds'])
        if en<=st: raise ValueError('non-positive span')
        filters.append(f'[{src}:a]atrim=start={st:.6f}:end={en:.6f},asetpts=PTS-STARTPTS[p{i}]')
        labels.append(f'[p{i}]')
    filters.append(''.join(labels)+f'concat=n={len(labels)}:v=0:a=1,apad=pad_dur=2[out]')
    out=ROOT/'3l'/'assets'/'audio'/f'record-{record}.mp3'; out.parent.mkdir(parents=True,exist_ok=True)
    sh('ffmpeg','-loglevel','error','-y',*inputs,'-filter_complex',';'.join(filters),'-map','[out]','-c:a','libmp3lame','-b:a','192k',str(out))
    sh('ffmpeg','-v','error','-i',str(out),'-f','null','-')

    receipt={
      'record':record,'status':'verified','greg_voice':'deep','dragon_voice':'normal','dragon_tempo':1.0,
      'semantic_dragon_spans':dragon_count,'total_role_spans':len(spans),'duration_seconds':probe(out),
      'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
      'greg_source_context_id':manifest[record]['greg_context_id'],'dragon_source_context_id':manifest[record]['dragon_context_id'],
      'assembly':'dual-full-render semantic splice; role transitions silence-snapped independently per voice; 2s settling tail'
    }
    vdir=ROOT/'3l'/'audio'/'verification'; vdir.mkdir(parents=True,exist_ok=True)
    (vdir/f'record-{record}-two-voice.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))


def main():
    manifest=json.loads((ROOT/'3l'/'audio'/'records-002-003-source-renders.json').read_text())
    for r in ('002','003'): render(r,manifest)

if __name__=='__main__': main()
