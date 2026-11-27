"""Optional PC embedding retrieval. Offline; no network or paid APIs."""
import os,pathlib,json,argparse
os.environ['HF_HUB_OFFLINE']='1';os.environ['TRANSFORMERS_OFFLINE']='1';os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
ROOT=pathlib.Path(__file__).resolve().parents[1]
def rank(model,question):
    import numpy as np
    from sentence_transformers import SentenceTransformer
    model=pathlib.Path(model).resolve(strict=True)
    if not model.is_dir():raise ValueError('Local model directory required')
    v=json.loads((ROOT/'semantic/vocabulary.json').read_text(encoding='utf8'));b=json.loads((ROOT/'catalog/bes.json').read_text(encoding='utf8'))
    docs=[(x['id'],x['label']+'; '+', '.join(x['aliases'])+'; '+x['module']) for x in v['concepts']]+[(x['id'],x['name']+'; '+x['domain']) for x in b['indicators']]
    encoder=SentenceTransformer(str(model),device='cpu',local_files_only=True,trust_remote_code=False)
    encoder.max_seq_length=128
    vectors=encoder.encode(['passage: '+x[1] for x in docs],normalize_embeddings=True,show_progress_bar=False)
    q=encoder.encode(['query: '+question],normalize_embeddings=True,show_progress_bar=False)[0]
    scores=vectors@q
    if not np.isfinite(scores).all():raise ValueError('Non-finite embedding')
    return [{'id':docs[i][0],'label':docs[i][1],'score':float(scores[i])} for i in np.argsort(-scores)[:5]]
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('model');p.add_argument('question');a=p.parse_args()
    print(json.dumps({'suggestions':rank(a.model,a.question),'note':'Candidate retrieval only, not verified statistical values.'},ensure_ascii=False,indent=2))
