"""Import reviewed WPP CSV with explicit column mapping; never merge variants."""
import csv,io,decimal
from provenance.import_policy import reviewed_bytes
def load(path,sha256,license_id,attribution,columns,approved=False):
    fields={'location','year','variant','indicator','value','unit'}
    if set(columns)!=fields:raise ValueError('Explicit WPP column mapping required')
    raw=reviewed_bytes(path,sha256,license_id,attribution,approved,max_bytes=500_000_000)
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))
    if not set(columns.values())<=set(reader.fieldnames or []):raise ValueError('Missing columns')
    seen=set()
    for row in reader:
        item={k:row[v] for k,v in columns.items()}
        item['year']=int(item['year'])
        value=decimal.Decimal(item['value'])
        if not value.is_finite() or not 1950<=item['year']<=2100 or any(not item[k].strip() for k in ('location','variant','indicator','unit')):raise ValueError('Invalid WPP row')
        key=tuple(item[k] for k in ('location','year','variant','indicator','unit'))
        if key in seen:raise ValueError('Duplicate observation')
        seen.add(key)
        yield {**item,'source':'UN WPP','value':str(value),'snapshot_sha256':sha256}
