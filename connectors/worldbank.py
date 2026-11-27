"""Public World Bank API, strictly identified yearly observations."""
import json,urllib.request,datetime,math
METRICS={'population':'SP.POP.TOTL','life_expectancy':'SP.DYN.LE00.IN','gdp_current_usd':'NY.GDP.MKTP.CD'}
GEO=set('ITA FRA DEU ESP PRT BEL AUT GRC POL ROU SWE FIN DNK IRL USA CHN JPN IND GBR CAN AUS'.split())
def plan(metric,geo,year):
    if metric not in METRICS or geo not in GEO or type(year)!=int or not 2000<=year<=datetime.date.today().year:raise ValueError('Unsupported query')
    indicator=METRICS[metric];return f'https://api.worldbank.org/v2/country/{geo}/indicator/{indicator}?format=json&date={year}',(indicator,geo,year)
def parse(raw,expected):
    indicator,geo,year=expected
    if not isinstance(raw,list) or len(raw)!=2 or not isinstance(raw[1],list) or len(raw[1])!=1:raise ValueError('Expected exactly one observation')
    row=raw[1][0];v=row.get('value')
    if row.get('indicator',{}).get('id')!=indicator or row.get('countryiso3code')!=geo or row.get('date')!=str(year):raise ValueError('Unexpected dimensions')
    if type(v) not in (int,float) or not math.isfinite(v) or v<0 or indicator=='SP.POP.TOTL' and v!=int(v) or indicator=='SP.DYN.LE00.IN' and v>130:raise ValueError('Invalid/missing observation')
    return {'source':'World Bank','indicator':indicator,'geo':geo,'year':year,'value':v,'unit':{'SP.POP.TOTL':'persons','SP.DYN.LE00.IN':'years','NY.GDP.MKTP.CD':'current USD'}[indicator]}
def query(metric,geo,year):
    url,e=plan(metric,geo,year)
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'VALE-VALENTINA-DATA/1.1'}),timeout=12) as r:raw=r.read(1_000_001)
    if len(raw)>1_000_000:raise ValueError('Response too large')
    return {**parse(json.loads(raw),e),'url':url}
