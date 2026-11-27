"""Build candidate pack in a separate path. Legacy TSV untouched."""
import pathlib,json,hashlib,os,tempfile,shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
INPUTS=['semantic/vocabulary.json','catalog/archives.json','catalog/bes.json','knowledge/graph.json','geography/registry.json','provenance/resources.json','methods/statistics.md','documentation/modules.json']
def build(dest):
    dest=pathlib.Path(dest)
    if dest.exists(): raise ValueError('Destination must not exist')
    dest.parent.mkdir(parents=True,exist_ok=True)
    tmp=pathlib.Path(tempfile.mkdtemp(dir=dest.parent))
    try:
        entries=[]
        for name in INPUTS:
            raw=(ROOT/name).read_bytes()
            if len(raw)>2_000_000: raise ValueError('Oversized resource')
            if name.endswith('.json'):json.loads(raw)
            target=tmp/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
            entries.append({'path':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
        manifest={'schema':2,'status':'candidate_unsigned','min_android_reader':2,'files':entries}
        (tmp/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        os.rename(tmp,dest)
    finally:
        if tmp.exists():shutil.rmtree(tmp)
    return manifest
if __name__=='__main__':
    import sys
    print(json.dumps(build(sys.argv[1]),indent=2))
