from pathlib import Path
p=Path('state/OPEN_THREADS.md')
s=p.read_text(encoding='utf-8')
old='- **Next engine rotation:** let Ch242\'s maintenance / no-work money day breathe. Do not convert the repaired grip, Vale\'s conditional `Tomorrow, maybe`, or Attempt 52 into an automatic next step; follow the next actual claim.'
new='- **Next engine rotation:** let Ch243\'s market-social day breathe. Do not convert the onion stall into a job, resurrect Ch242\'s expired `Tomorrow, maybe`, or turn Attempt 52 into an automatic next step; follow the next actual claim.'
assert old in s
p.write_text(s.replace(old,new,1),encoding='utf-8')
print('UPDATED_NEXT_ENGINE_ROTATION')
