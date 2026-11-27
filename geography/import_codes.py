"""Import a reviewed dated geographic crosswalk; preserve codes as strings."""
import csv,io,datetime
from provenance.import_policy import reviewed_bytes
def load(path,sha256,license_id,attribution,system,as_of,approved=False):
    datetime.date.fromisoformat(as_of)
    raw=reviewed_bytes(path,sha256,license_id,attribution,approved)
    rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
    seen=set();out=[]
    for row in rows:
        code=row['code'].strip();level=row['level'].strip();name=row['name'].strip()
        if not code or not level or not name or (level,code) in seen:raise ValueError('Invalid or duplicate geography')
        seen.add((level,code));out.append({'system':system,'as_of':as_of,'code':code,'level':level,'name':name})
    return out
