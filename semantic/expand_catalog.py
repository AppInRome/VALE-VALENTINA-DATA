"""Derive distinct indicator concepts from the existing BES catalog, preserving provenance."""
import json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def expand():
    v=json.loads((ROOT/'semantic/vocabulary.json').read_text())
    b=json.loads((ROOT/'catalog/bes.json').read_text())
    g=json.loads((ROOT/'knowledge/graph.json').read_text())
    concepts=[{**c,'origin':'curated'} for c in v['concepts']]
    edges=list(g['edges'])
    domains=sorted({i['domain'] for i in b['indicators']})
    for n,d in enumerate(domains):
        concepts.append({'id':f'bes_domain_{n}','label':d,'kind':'domain','origin':b['source']})
    for i in b['indicators']:
        cid='bes_'+i['id']
        concepts.append({'id':cid,'label':i['name'],'kind':'indicator','origin':b['source'],'domain':i['domain'],'queryable':False})
        edges.append({'from':cid,'to':f"bes_domain_{domains.index(i['domain'])}",'relation':'classified_in','source':b['source']})
    assert len({c['id'] for c in concepts})==len(concepts)
    return {'concepts':concepts,'edges':edges,'note':'Catalog identifiers are not proof of executable queries; lexical overlap is not equivalence.'}
if __name__=='__main__':print(json.dumps(expand(),ensure_ascii=False,indent=2))
