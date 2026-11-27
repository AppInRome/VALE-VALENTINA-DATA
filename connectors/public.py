"""Bounded public-source clients; raw responses are candidates, not verified observations."""
import json, os, re, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from datetime import datetime, timezone
SDMX={'istat':'https://esploradati.istat.it/SDMXWS/rest','oecd':'https://sdmx.oecd.org/public/rest'}
def token(value):
    if not isinstance(value,str) or not re.fullmatch(r'[A-Za-z0-9_.+,@-]{1,200}',value): raise ValueError('Invalid identifier')
    return value
def get(url, accept='application/json', body=None, headers=None):
    request=urllib.request.Request(url,data=body,headers={'Accept':accept,'User-Agent':'VALE-VALENTINA-DATA/2',**(headers or {})})
    with urllib.request.urlopen(request,timeout=25) as response:
        raw=response.read(16_000_001)
    if len(raw)>16_000_000: raise ValueError('Response exceeds bound')
    return raw
def flows(source, agency='all'):
    url=SDMX[source]+'/dataflow/'+token(agency)+'?detail=allstubs'
    root=ET.fromstring(get(url,'application/vnd.sdmx.structure+xml;version=2.1'))
    return [{'id':e.get('id'),'agency':e.get('agencyID'),'version':e.get('version'),'names':{n.get('{http://www.w3.org/XML/1998/namespace}lang','und'):n.text for n in e if n.tag.endswith('}Name')}} for e in root.iter() if e.tag.endswith('}Dataflow') and e.get('id')]
def sdmx_data(source, flow, key, start, end):
    if not (type(start)==type(end)==int and 1900<=start<=end<=2100 and end-start<=20): raise ValueError('Invalid period')
    url=SDMX[source]+'/data/'+token(flow)+'/'+token(key)+'?'+urllib.parse.urlencode({'startPeriod':start,'endPeriod':end})
    return get(url,'application/vnd.sdmx.genericdata+xml;version=2.1')
def who(indicator, country, year):
    if not re.fullmatch('[A-Z]{3}',country) or type(year)!=int or not 1900<=year<=2100: raise ValueError('Invalid filters')
    url='https://ghoapi.azureedge.net/api/'+token(indicator)+'?'+urllib.parse.urlencode({'$filter':"SpatialDim eq '"+country+"' and TimeDim eq "+str(year),'$top':100})
    data=json.loads(get(url))
    if not isinstance(data.get('value'),list) or data.get('@odata.nextLink'): raise ValueError('Incomplete result')
    if any(r.get('SpatialDim')!=country or r.get('TimeDim')!=year for r in data['value']): raise ValueError('Unexpected dimensions')
    return {'source':'who','url':url,'rows':data['value'],'status':'candidate_requires_stratum_validation'}
def un_population(indicator,location,start,end):
    if not all(type(x)==int for x in (indicator,location,start,end)) or min(indicator,location)<1 or not 1950<=start<=end<=2100: raise ValueError('Invalid filters')
    url=f'https://population.un.org/dataportalapi/api/v1/data/indicators/{indicator}/locations/{location}?'+urllib.parse.urlencode({'startYear':start,'endYear':end})
    return {'source':'un_population','url':url,'response':json.loads(get(url)),'status':'candidate_requires_variant_validation'}
def undata_sdg(series,area):
    if type(area)!=int or area<1: raise ValueError('Invalid area')
    url='https://unstats.un.org/SDGAPI/v1/sdg/Series/Data?'+urllib.parse.urlencode({'seriesCode':token(series),'areaCode':area,'pageSize':100})
    return {'source':'unsd_sdg','url':url,'response':json.loads(get(url)),'status':'candidate_requires_pagination_and_dimensions'}
def datacommons(entity,variable,date):
    if os.getenv('VALE_ENABLE_DATACOMMONS')!='true': raise RuntimeError('Explicit opt-in required')
    key=os.environ.get('DATACOMMONS_API_KEY')
    if not key: raise RuntimeError('API key required')
    url='https://api.datacommons.org/v2/observation'
    body=json.dumps({'date':token(date),'entity':{'dcids':[token(entity)]},'variable':{'dcids':[token(variable)]},'select':['date','entity','variable','value','facet']}).encode()
    return {'source':'datacommons','response':json.loads(get(url,body=body,headers={'X-API-Key':key,'Content-Type':'application/json'})),'status':'candidate_requires_facet_validation'}
