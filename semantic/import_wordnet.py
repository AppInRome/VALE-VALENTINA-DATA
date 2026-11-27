"""Import local Italian OMW TSV as candidates only. Verify original licence first."""
import argparse,hashlib,json,pathlib,re,collections
SOURCE='https://github.com/omwn/omw-data/tree/main/wns/ita'
def index(raw,sha):
    if len(raw)>40_000_000 or hashlib.sha256(raw).hexdigest()!=sha.lower():raise ValueError('Size or checksum mismatch')
    synsets=collections.defaultdict(set)
    for line in raw.decode('utf8').splitlines():
        cols=line.split('\t')
        if len(cols)<3 or cols[1]!='ita:lemma' or not re.fullmatch(r'\d{8}-[nvars]',cols[0]):continue
        lemma=cols[2].strip().replace('_',' ')
        if 0<len(lemma)<=100 and all(ord(c)>=32 for c in lemma):synsets[cols[0]].add(lemma)
    return {'source':SOURCE,'sha256':sha.lower(),'synsets':{k:sorted(v) for k,v in sorted(synsets.items()) if len(v)>1},'policy':'Candidates only; review senses, attribution and licence before publishing.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('file',type=pathlib.Path);p.add_argument('--sha256',required=True);p.add_argument('--output',type=pathlib.Path,default=pathlib.Path('wordnet_candidates.local.json'));a=p.parse_args()
    if a.file.stat().st_size>40_000_000:raise SystemExit('File too large')
    result=index(a.file.read_bytes(),a.sha256)
    if not result['synsets']:raise SystemExit('No Italian synonym sets found')
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(len(result['synsets']),'candidate synsets')
