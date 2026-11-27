"""Opt-in snapshot, never overwrite a previous good snapshot on error."""
import datetime,json,pathlib,sys,os
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from connectors.eurostat import query
out=ROOT/'catalog'/'external_snapshot.json'
year=datetime.date.today().year-2
observations=[query(metric,'IT',year) for metric in ('population','unemployment')]
result={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'observations':observations}
tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');os.replace(tmp,out)
print('Two public observations saved; no AI API calls.')
