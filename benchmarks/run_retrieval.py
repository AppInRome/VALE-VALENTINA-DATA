"""Measure generated BES retrieval separately from numerical accuracy."""
import sys,pathlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from semantic.expand_catalog import expand
from semantic.fts import build,search
from benchmarks.generate import cases
def run():
    docs=[(c['id'],c['label'],c.get('domain','')) for c in expand()['concepts'] if c.get('kind')=='indicator']
    db=build(docs);results=[]
    for c in cases():
        ids=[x[0] for x in search(db,c['question'])]
        results.append({'question':c['question'],'expected':c['expected_id'],'top1':bool(ids and ids[0]==c['expected_id']),'top5':c['expected_id'] in ids})
    return {'suite':'generated_exact_label_retrieval','cases':len(results),'top1_correct':sum(x['top1'] for x in results),'top5_correct':sum(x['top5'] for x in results),'numeric_accuracy':None,'failures':[x for x in results if not x['top1']]}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
