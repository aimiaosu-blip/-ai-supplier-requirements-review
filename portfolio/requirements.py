import re, math, hashlib
from collections import Counter
from pathlib import Path
from .reused_text import cosine as cosine_similarity

def tokens(text): return re.findall(r'[a-z0-9]+',text.lower())

def parse_document(path):
    """Explicit line contract: ID | topic | value | unit. No guessed NLP extraction."""
    path=Path(path); result=[]; raw=path.read_text()
    for line_no,line in enumerate(raw.splitlines(),1):
        if not line.strip() or line.startswith('#'): continue
        parts=[p.strip() for p in line.split('|')]
        if len(parts)!=4: raise ValueError(f'{path.name}:{line_no}: expected four fields')
        rid,topic,value,unit=parts
        if any(r['id']==rid for r in result): raise ValueError('Duplicate requirement ID')
        result.append(dict(id=rid,topic=topic,value=value,unit=unit,source=path.name,line=line_no,quote=line,sha256=hashlib.sha256(raw.encode()).hexdigest()))
    return result

class Retriever:
    """TF-IDF cosine baseline adapted from the existing supplier-claim project."""
    def __init__(self,rows):
        self.rows=rows; counts=[Counter(tokens(r['quote'])) for r in rows]
        vocab=set(t for c in counts for t in c)
        self.idf={t:math.log((1+len(rows))/(1+sum(t in c for c in counts)))+1 for t in vocab}
        self.vectors=[{t:n*self.idf[t] for t,n in c.items()} for c in counts]
    def search(self,query,k=3):
        if k<1: raise ValueError('k must be positive')
        q={t:n*self.idf[t] for t,n in Counter(tokens(query)).items() if t in self.idf}
        def cosine(v): return cosine_similarity(q,v)
        scored=sorted([(cosine(v),r) for v,r in zip(self.vectors,self.rows)],key=lambda x:(-x[0],x[1]['source'],x[1]['line']))
        return [dict(r,score=round(s,6)) for s,r in scored[:k] if s>0]
    def answer(self,query):
        hits=self.search(query)
        return '\n'.join(f"[{r['source']}:{r['line']}] {r['quote']}" for r in hits) or 'Insufficient evidence: no matching source.'

def compare(requirements,responses):
    lookup={r['id']:r for r in responses}; output=[]
    for req in requirements:
        res=lookup.get(req['id']); status='missing'
        if res:
            status='unknown'
            if req['unit']!=res['unit']: status='unit_mismatch'
            elif req['topic']!=res['topic']: status='topic_mismatch'
            else:
                match=re.fullmatch(r'(<=|>=)(\d+(?:\.\d+)?)',req['value'])
                if match:
                    try:
                        number=float(res['value']); bound=float(match[2])
                        if math.isfinite(number): status='met' if (number<=bound if match[1]=='<=' else number>=bound) else 'exception'
                    except ValueError: pass
                elif res['value'].lower() in {'unknown','tbd',''}: pass
                else: status='met' if res['value'].lower()==req['value'].lower() else 'exception'
        output.append(dict(requirement=req['id'],topic=req['topic'],expected=req['value'],actual=res['value'] if res else None,status=status,source=res['source'] if res else None,line=res['line'] if res else None,quote=res['quote'] if res else None))
    return output
