TITLE='Enterprise AI Assistant & Supplier Requirements Review'

import json
from pathlib import Path
import streamlit as st
import pandas as pd
from portfolio.governance import ReviewStore, digest
ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title=TITLE,layout='wide')
st.title(TITLE)
st.warning('Synthetic portfolio demonstration. No real company data or validated business outcomes. Independent project; no company affiliation.')
def load(name): return json.loads((ROOT/'data'/name).read_text())
def review(artifact,blocked=False):
    st.subheader('Human review')
    st.caption('Self-declared demo reviewer. A decision applies only to this exact artifact version. Local SQLite audit; not enterprise authentication.')
    with st.form('review'):
        reviewer=st.text_input('Reviewer alias',value='demo-reviewer')
        decision=st.selectbox('Decision',['revise','approve','reject'])
        reason=st.text_area('Reason')
        submit=st.form_submit_button('Record human decision')
    store=ReviewStore(ROOT/'runtime'/'audit.sqlite')
    if submit:
        try:store.decide(digest(artifact),decision,reviewer,reason,blocked);st.success('Decision recorded')
        except ValueError as exc:st.error(str(exc))
    st.caption('Audit hash chain valid: '+str(store.verify()))
    st.dataframe(store.rows())
    st.download_button('Download audit JSON',json.dumps(store.rows(),indent=2),'audit.json')
    store.db.close()

from portfolio.requirements import parse_document, Retriever, compare
requirements=parse_document(ROOT/'data/requirements.txt')
supplier=st.selectbox('Supplier',['supplier_a','supplier_b'])
responses=parse_document(ROOT/'data'/f'{supplier}.txt')
upload=st.file_uploader('Optional synthetic response document (.txt)',type=['txt'])
if upload:
    import tempfile
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/'uploaded_synthetic.txt';path.write_bytes(upload.getvalue())
        try:responses=parse_document(path)
        except (ValueError,UnicodeError) as exc:st.error(str(exc));st.stop()
results=compare(requirements,responses)
st.subheader('Requirement comparison')
st.dataframe(results,use_container_width=True)
st.bar_chart(pd.Series([r['status'] for r in results]).value_counts())
st.subheader('Evidence assistant — lexical RAG with extractive generation')
query=st.text_input('Evidence question',value='lead_time warranty')
index=Retriever(responses)
st.text(index.answer(query))
with st.expander('Source provenance and retrieval scores'):st.json(index.search(query))
st.download_button('Download comparison',json.dumps(results,indent=2),'comparison.json')
review({'requirements':requirements,'responses':responses,'comparison':results},any(r['status']!='met' for r in results))
