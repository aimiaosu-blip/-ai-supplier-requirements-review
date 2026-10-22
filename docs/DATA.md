# Data contract and metrics

All three text documents are authored fictional fixtures. Non-comment lines contain four pipe-delimited fields: `requirement_id | topic | value | unit`. Requirement values may be `<=number`, `>=number` or an exact categorical value. Supplier values must use matching units and topics; IDs must be unique within a document. No OCR or free-prose extraction is claimed.

`gold.json` stores six expected statuses per supplier and four retrieval query/source/ID targets. File hashes and line numbers are computed at load time. The fixture uses 6 requirements and 11 response lines. Retrieval Hit@3 counts an exact target source/ID among up to three positive-similarity results. Comparison accuracy counts exact categorical status agreement; status labels are not binary business acceptance.
