# Five-minute demonstration

1. Start the dashboard and select supplier A. Inspect six matching requirements.
2. Search `lead_time warranty`. Expand provenance to see exact text, line, hash and cosine score.
3. Search `delivery duration`. Observe the lexical limitation or abstention; this query is retained in the benchmark.
4. Select supplier B. Inspect late delivery, low recycled content, warranty unit mismatch, unknown declaration and missing traceability.
5. Attempt approval with a reason: the gate blocks it. Choose revise and describe the evidence request.
6. Download the comparison and audit. Reload to inspect persisted review state.

Optional upload accepts synthetic UTF-8 `.txt` files with `ID | topic | value | unit`. It is a strict document format, not arbitrary natural-language extraction. Never upload real supplier documents. Approval does not send anything to a supplier.
