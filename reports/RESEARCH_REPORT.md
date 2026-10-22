# Research report: traceable supplier requirements review

## Executive finding

The prototype produces a source-linked comparison, identifies known exceptions and prevents approval when mandatory evidence remains unresolved. It correctly classifies all **12 authored requirement-response fixtures**. Retrieval finds the expected item in the top three for **3 of 4 queries (75%)**. These are actual program outputs on a tiny synthetic fixture, not evidence of effectiveness at Scania, Derome or another company.

## Research question and method

Can requirement-level evidence retrieval improve review completeness without transferring decision authority to AI? The artifact separates extraction, comparison, retrieval and human disposition so each stage can be examined. Six requirements cover lead time, recycled content, warranty, environmental documentation, traceability and defects. Two fictional responses contain positive evidence, numeric violations, missing evidence, an unknown answer and a unit mismatch.

The structured parser retains the original line, filename, line number and SHA-256 document hash. Numeric comparison accepts explicit <= or >= thresholds. Unit conversion is deliberately not guessed: two years against 24 months is marked for review, even though a human may establish equivalence. The assistant uses sparse TF-IDF cosine similarity to retrieve response lines and composes an extractive answer with exact citations. Retrieval does not determine compliance; the comparison engine evaluates all requirements independently.

## Evaluation

`python -m portfolio.demo` writes `results/comparison.json`, `retrieval.json`, `metrics.json` and `overview.svg`. Gold statuses and target retrieval IDs are explicitly stored in `data/gold.json`. Fixture status accuracy is the number of exact status matches divided by 12. Hit@3 is the proportion of the four authored queries with their expected source and requirement among the returned hits. Gold labels were authored alongside the fixture; there is no held-out generalization claim.

Supplier A meets six of six specified criteria. Supplier B meets one, violates two, has one unit mismatch, one unknown and one missing response. Query `delivery duration` fails to match `lead_time`, making the baseline's vocabulary dependence visible. A perfect fixture classifier is expected for explicit structured rules and should not be described as 100% AI accuracy.

## Governance and business interpretation

A reviewer can revise or reject an exception-bearing package but cannot approve it. Reviewers supply an alias and rationale. Decisions bind to the artifact hash, including source provenance. The database records chained events and rejects a second disposition for an unchanged artifact. The result is an inspectable demonstration of accountability, not compliance-grade identity or immutable storage.

The business value hypothesis is fewer overlooked requirements and less evidence-search effort. Neither time savings nor improved supplier quality has been measured. The MVP can support a thesis interview: ask reviewers whether a unit mismatch should block approval, what source authority they need, and which exceptions require engineering review.

## Proposed thesis validation

First collect permitted, redacted documents and have two domain reviewers independently label requirements and evidence spans. Resolve disagreements before evaluation. Split at document and supplier level so near-duplicate language does not leak across development and evaluation. Compare manual search, lexical retrieval and an approved semantic model on the same cases. Measure per-status precision/recall, critical false acceptances, citation correctness, evidence coverage and abstention. Run a counterbalanced reviewer study measuring active review time, error severity and workload. Predefine acceptable critical-error rates with the organization; do not optimize only mean accuracy.

## Limitations and next work

The current format is pipe-delimited text, not general PDF or prose extraction. It does not perform semantic entailment, document version negotiation, unit conversion, OCR or authenticated supplier segregation. Hashes establish identity, not truth. Prompt-like content in uploaded text is treated as evidence text and never executed. Future work requires schema-aware ingestion, multilingual paraphrase retrieval, independent annotation and production access controls.

## Reproduction and evidence

Run `python -m portfolio.demo` from the repository root. Inputs are in `data/`; row-level or aggregate outputs are in `results/`. Run `python -m pytest -q` for the tested behavioral boundaries. All original synthetic materials are MIT-licensed.
