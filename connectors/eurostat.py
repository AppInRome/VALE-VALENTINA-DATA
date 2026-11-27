"""Public Eurostat API. Exactly one validated observation."""
import json,math,urllib.parse,urllib.request,datetime
BASE='https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/'
GEO=set('IT FR DE ES PT BE AT EL PL RO SE FI DK IE EU27_2020'.split())
METRICS={'population':('demo_pjan','NR','TOTAL'),'unemployment':('une_rt_a','PC_ACT','Y15-74')}
def plan(metric,geo,year):
    if metric not in METRICS or geo not in GEO or type(year)!=int or not 2000<=year<=datetime.date.today().year:raise ValueError('Unsupported query')
    dataset,unit,age=METRICS[metric];dims={'freq':'A','unit':unit,'sex':'T','age':age,'geo':geo,'time':str(year)}
    return BASE+dataset+'?'+urllib.parse.urlencode({'lang':'it',**dims}),dims
def parse(raw,expected):
    if raw.get('class')!='dataset':raise ValueError('Not a dataset')
    ids=raw['id'];sizes=raw['size']
    if len(ids)!=len(expected) or set(ids)!=set(expected) or sizes!=[1]*len(ids):raise ValueError('Unexpected dimensions')
    for dim in ids:
        idx=raw['dimension'][dim]['category']['index'];key=expected[dim]
        if idx not in ({key:0},[key]):raise ValueError('Dimension mismatch '+dim)
    values=raw['value'];v=values.get('0') if isinstance(values,dict) else values[0] if len(values)==1 else None
    if type(v) not in (int,float) or not math.isfinite(v) or v<0:raise ValueError('Missing or invalid value')
    if expected['unit']=='PC_ACT' and v>100 or expected['unit']=='NR' and v!=int(v):raise ValueError('Invalid unit value')
    status=raw.get('status',{});flag=status.get('0') if isinstance(status,dict) else status[0] if isinstance(status,list) and status else None
    return {'value':v,'dimensions':expected,'flag':flag,'source':'Eurostat'}
def query(metric,geo,year):
    url,expected=plan(metric,geo,year)
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'VALE-VALENTINA-DATA/1.1'}),timeout=20) as r:raw=r.read(2_000_001)
    if len(raw)>2_000_000:raise ValueError('Response too large')
    return {**parse(json.loads(raw),expected),'url':url}
