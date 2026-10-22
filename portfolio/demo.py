import json
from pathlib import Path
from portfolio.charts import bars
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
def load(name): return json.loads((ROOT/'data'/name).read_text())
def write(name,value): (OUT/name).write_text(json.dumps(value,indent=2)+'\n')

from portfolio.requirements import *
requirements=parse_document(ROOT/'data/requirements.txt');gold=load('gold.json');results={};correct=0;total=0
allrows=[]
for supplier in ['supplier_a','supplier_b']:
    rows=parse_document(ROOT/'data'/f'{supplier}.txt');allrows.extend(rows)
    results[supplier]=compare(requirements,rows)
    for actual,expected in zip(results[supplier],gold[supplier]):
        correct+=actual['status']==expected;total+=1
index=Retriever(allrows);retrieval=[]
for case in gold['retrieval']:
    hits=index.search(case['query']);hit=any(r['source']==case['source'] and r['id']==case['id'] for r in hits)
    retrieval.append(dict(case,hit_at_3=hit,retrieved=[r['source']+':'+r['id'] for r in hits]))
metrics={'fixture_status_accuracy':correct/total,'evaluated_requirements':total,'retrieval_hit_at_3':sum(r['hit_at_3'] for r in retrieval)/len(retrieval),'retrieval_queries':len(retrieval)}
write('comparison.json',results);write('retrieval.json',retrieval);write('metrics.json',metrics)
bars({k:sum(r['status']=='met' for r in v)/len(v) for k,v in results.items()},OUT/'overview.svg','Synthetic requirement coverage (not supplier validation)')

print('Rebuilt synthetic outputs in',OUT)
