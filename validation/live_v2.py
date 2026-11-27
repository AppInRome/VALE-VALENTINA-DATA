"""Explicit live diagnostics; never publish raw candidates as observations."""
import sys,pathlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from connectors import public,eurostat,worldbank
checks=[('ISTAT flows',lambda:public.flows('istat')),('OECD flows',lambda:public.flows('oecd')),('WHO',lambda:public.who('WHOSIS_000001','ITA',2020)),('Eurostat',lambda:eurostat.query('population','IT',2024)),('World Bank',lambda:worldbank.query('population','ITA',2024))]
results=[]
for name,fn in checks:
    try:
        result=fn()
        if not result:raise ValueError('Empty response')
        results.append({'name':name,'status':'response_received','type':type(result).__name__})
    except Exception as e:results.append({'name':name,'status':'failed','error':str(e)[:250]})
print(json.dumps(results,indent=2))
sys.exit(any(r['status']=='failed' for r in results))
