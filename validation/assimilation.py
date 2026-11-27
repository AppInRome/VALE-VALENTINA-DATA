"""Online diagnostics, no paid API, no promotion of unverified observations."""
import sys,pathlib,json,urllib.request,hashlib,datetime
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from connectors import public,eurostat,worldbank
def e5_config():
    url='https://huggingface.co/api/models/intfloat/multilingual-e5-small'
    with urllib.request.urlopen(url,timeout=25) as r: model=json.loads(r.read(2_000_000))
    sha=model['sha']
    if len(sha)!=40 or any(c not in '0123456789abcdef' for c in sha):raise ValueError('Invalid model revision')
    with urllib.request.urlopen('https://huggingface.co/intfloat/multilingual-e5-small/resolve/'+sha+'/config.json',timeout=25) as r: raw=r.read(100_000)
    config=json.loads(raw)
    return {'revision':sha,'config_sha256':hashlib.sha256(raw).hexdigest(),'hidden_size':config['hidden_size'],'weights_verified':False}
def check(name,fn):
    try:
        value=fn()
        if not value:raise ValueError('Empty result')
        return {'name':name,'status':'response_received','detail':value if name=='E5 metadata' else {'type':type(value).__name__,'count':len(value)}}
    except Exception as e:return {'name':name,'status':'failed','error':str(e)[:300]}
checks=[('ISTAT',lambda:public.flows('istat')),('OECD',lambda:public.flows('oecd')),('Eurostat',lambda:eurostat.query('population','IT',2024)),('World Bank',lambda:worldbank.query('population','ITA',2024)),('WHO',lambda:public.who('WHOSIS_000001','ITA',2020)),('E5 metadata',e5_config)]
report={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':[check(n,f) for n,f in checks]}
pathlib.Path('assimilation-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
sys.exit(any(r['status']=='failed' for r in report['results']))
