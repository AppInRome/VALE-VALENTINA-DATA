"""Validate public metadata, curated routing and bounded pack; no network."""
import sys,json,pathlib,re,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from semantic.search import load,search,search_bes
from semantic.import_wordnet import index
from connectors.eurostat import plan,parse
from connectors.worldbank import plan as wbplan,parse as wbparse
from validation.build_pack import build
v=load('semantic/vocabulary.json');ids=[x['id'] for x in v['concepts']]
assert len(ids)==25 and len(set(ids))==len(ids)
assert all(x['module'] in ['POPULIV','PROXIMA','PRAEVOL','PULSE'] for x in v['concepts'])
for a,cs in v['ambiguous'].items():assert set(cs)<=set(ids)
g=load('knowledge/graph.json');assert set(g['nodes'])==set(ids)
for e in g['edges']:assert e['from'] in ids and e['to'] in ids
files=load('catalog/archives.json')['files']
assert len(files)==77 and len(files)==len({(f['module'],f['file']) for f in files})
assert sum(len(f.get('tables',{})) for f in files)==44
bes=load('catalog/bes.json')['indicators'];assert len(bes)==141 and len(bes)==len({x['id'] for x in bes})
cases=load('tests/reference.json')['cases']
for c in cases:
    r=search(c['question'])
    assert (r['status']==c['status'] if 'status' in c else r['status']=='suggestions' and r['matches'][0]['id']==c['id']),(c,r)
for c in v['concepts']:
    for a in c['aliases']:assert c['id'] in {x['id'] for x in search(a)['matches']},(c['id'],a)
assert search_bes('speranza di vita alla nascita')[0]['id']=='01SAL001'
url,d=plan('population','IT',2024)
fixture={'class':'dataset','id':list(d),'size':[1]*len(d),'dimension':{k:{'category':{'index':{x:0}}} for k,x in d.items()},'value':{'0':123}}
assert parse(fixture,d)['value']==123
def reject(fn):
    try:fn()
    except (ValueError,KeyError,TypeError,IndexError):return
    raise AssertionError('Invalid observation accepted')
for invalid in [-1,True,1.2,None]:reject(lambda:parse({**fixture,'value':{'0':invalid}},d))
reject(lambda:parse({**fixture,'size':[2]+fixture['size'][1:]},d))
_,e=wbplan('population','ITA',2024);row={'indicator':{'id':e[0]},'countryiso3code':'ITA','date':'2024','value':123}
assert wbparse([{},[row]],e)['value']==123
for edit in [{'value':None},{'value':True},{'value':-1},{'value':1.5},{'countryiso3code':'FRA'},{'date':'2023'},{'indicator':{'id':'wrong'}}]:
    reject(lambda:wbparse([{},[{**row,**edit}]],e))
reject(lambda:wbparse([{},[row,row]],e))
raw=b'00000001-n\tita:lemma\tnosocomio\n00000001-n\tita:lemma\tospedale\n'
assert index(raw,hashlib.sha256(raw).hexdigest())['synsets']=={'00000001-n':['nosocomio','ospedale']}
reject(lambda:index(raw,'0'*64))
pack=ROOT/'distribution/knowledge.tsv';original=pack.read_bytes()
try:
    n=build();assert pack.read_bytes()==original,'Pack does not match catalog; increment revision and regenerate intentionally'
finally:
    if pack.read_bytes()!=original:pack.write_bytes(original)
header,body=original.split(b'\n',1);assert header.split(b'\t')[-1].decode()==hashlib.sha256(body).hexdigest()
print(json.dumps({'status':'passed','archives':len(files),'tables':44,'bes':len(bes),'concepts':len(ids),'normalization_rules':len(v['normalization_rules']),'aliases_tested':sum(len(c['aliases']) for c in v['concepts']),'reference_cases':len(cases),'relations':len(g['edges']),'pack_rows':n,'live_api_tested':False},indent=2))
