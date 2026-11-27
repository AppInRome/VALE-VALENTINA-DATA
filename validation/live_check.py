"""Explicit live smoke tests; errors never become data."""
import pathlib,sys,json
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from connectors import eurostat,worldbank
results=[]
for name,fn,args in [('Eurostat population',eurostat.query,('population','IT',2024)),('Eurostat unemployment',eurostat.query,('unemployment','IT',2024)),('World Bank population',worldbank.query,('population','ITA',2024))]:
    try:results.append({'test':name,'status':'passed','result':fn(*args)})
    except Exception as e:results.append({'test':name,'status':'failed','reason':str(e)[:300]})
print(json.dumps(results,ensure_ascii=False,indent=2));sys.exit(0 if all(x['status']=='passed' for x in results) else 1)
