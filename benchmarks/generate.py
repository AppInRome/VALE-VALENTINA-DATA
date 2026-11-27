"""Generate labeled retrieval cases, not claims of numerical accuracy."""
import pathlib,sys,json
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from semantic.expand_catalog import expand
def cases():
    out=[]
    for c in expand()['concepts']:
        if c.get('kind')!='indicator':continue
        for fmt in ('Cerca indicatore {label}', 'Qual è la definizione di {label}?','Mostrami la serie storica di {label}','Quale fonte descrive {label}?'):
            out.append({'question':fmt.format(**c),'expected_id':c['id'],'suite':'generated_retrieval','numeric_verified':False})
    return out
if __name__=='__main__':print(json.dumps(cases(),ensure_ascii=False,indent=2))
