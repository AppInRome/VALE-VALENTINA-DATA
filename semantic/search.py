"""Offline concept and BES retrieval. Suggestions only, not executable SQL."""
import json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))
def fold(text): return ' '.join(re.findall(r'[a-z0-9]+',''.join(c for c in unicodedata.normalize('NFD',text.lower()) if not unicodedata.combining(c))))
def contains(text,phrase): return ' '+fold(phrase)+' ' in ' '+text+' '
def search(query):
    q=fold(query); v=load('semantic/vocabulary.json')
    if not q or len(q)>500:return {'status':'unsupported','matches':[]}
    hits=[]
    for c in v['concepts']:
        h=[fold(a) for a in [c['label'],*c['aliases']] if contains(q,a)]
        if h:hits.append((max(len(a.split()) for a in h),c))
    if hits:
        matches=[x[1] for x in hits if x[0]==max(y[0] for y in hits)]
        return {'status':'suggestions' if len(matches)==1 else 'ambiguous','matches':matches}
    for alias,ids in v['ambiguous'].items():
        if contains(q,alias):return {'status':'ambiguous','matches':[c for c in v['concepts'] if c['id'] in ids]}
    return {'status':'not_found','matches':[]}
def search_bes(query,limit=5):
    stop=set('di del della da in a il la le per e quale qual quanto nel l'.split())
    q=set(fold(query).split())-stop; rows=[]
    for x in load('catalog/bes.json')['indicators']:
        w=set(fold(x['name']).split())-stop
        if q&w: rows.append((len(q&w)/max(1,len(q|w)),x['id'],x))
    return [x[2] for x in sorted(rows,key=lambda x:(-x[0],x[1]))[:max(0,min(limit,20))]]
if __name__=='__main__':
    import sys
    q=' '.join(sys.argv[1:])
    print(json.dumps({'concepts':search(q),'bes':search_bes(q)},ensure_ascii=False,indent=2))
