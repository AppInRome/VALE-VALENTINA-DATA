"""Produce bounded UTF-8 Android knowledge pack; no SQL, code, user data or observations."""
import hashlib,json,re,unicodedata,pathlib,os
ROOT=pathlib.Path(__file__).resolve().parents[1]
def fold(s):return ' '.join(re.findall(r'[a-z]+',''.join(c for c in unicodedata.normalize('NFD',s.lower()) if not unicodedata.combining(c))))
def build():
    v=json.loads((ROOT/'semantic/vocabulary.json').read_text(encoding='utf8'));b=json.loads((ROOT/'catalog/bes.json').read_text(encoding='utf8'))
    rows=[];seen={}
    for rule in v['normalization_rules']:
        dest=fold(rule['canonical'])
        for raw in rule['aliases']:
            alias=fold(raw)
            if alias==dest:continue
            if alias in seen and seen[alias]!=dest:raise ValueError('Conflicting alias '+alias)
            if alias not in seen:rows.append(('A',alias,dest));seen[alias]=dest
    for c in v['concepts']:rows.append(('C',c['id'],c['module'],c['label'],' | '.join(c['aliases'])))
    for x in b['indicators']:rows.append(('I',x['id'],x['name'],x['domain']))
    if any(any('\t' in f or '\n' in f or '\r' in f or len(f)>500 for f in row) for row in rows):raise ValueError('Invalid field')
    body=''.join('\t'.join(row)+'\n' for row in rows).encode()
    if len(body)>=500_000:raise ValueError('Pack too large')
    revision=int((ROOT/'distribution/revision.txt').read_text().strip())
    if revision<1:raise ValueError('Invalid revision')
    pack=f'VALE-KNOWLEDGE-1\t{revision}\t{hashlib.sha256(body).hexdigest()}\n'.encode()+body
    dest=ROOT/'distribution/knowledge.tsv';tmp=dest.with_suffix('.tmp');tmp.write_bytes(pack);os.replace(tmp,dest)
    return len(rows)
if __name__=='__main__':print('Knowledge pack rows:',build())
