"""Import Italian SKOS RDF/XML from a reviewed local snapshot."""
import pathlib,hashlib,xml.etree.ElementTree as ET
def load(path,sha256):
    raw=pathlib.Path(path).read_bytes()
    if len(raw)>100_000_000 or hashlib.sha256(raw).hexdigest()!=sha256: raise ValueError('Invalid snapshot')
    root=ET.fromstring(raw)
    rdf='{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'
    skos='{http://www.w3.org/2004/02/skos/core#}'
    lang='{http://www.w3.org/XML/1998/namespace}lang'
    out=[]
    for el in root.iter():
        uri=el.get(rdf+'about')
        if not uri:continue
        labels=[x.text.strip() for x in el if x.tag in (skos+'prefLabel',skos+'altLabel') and x.get(lang)=='it' and x.text and x.text.strip()]
        if labels:out.append({'uri':uri,'labels':sorted(set(labels))})
    return out
