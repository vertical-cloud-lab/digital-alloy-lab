# Cleaning test sieves between alloys (issue #234)

The lab sieved a bronze (Cu-Sn) powder through its 63 µm and 250 µm test sieves and next wants to
sieve aluminum powder for LPBF through the same sieves. Issue #234 asked for an Edison Scientific
query on how to clean the sieves so the bronze does not contaminate the aluminum.

Two Edison jobs were submitted on 2026-11-03 with the same question (`question.txt`):

| Key | Job | Why |
|-----|-----|-----|
| `literature` | LITERATURE (`job-futurehouse-paperqa3`) | Fast answer |
| `literature_high` | LITERATURE_HIGH (`job-futurehouse-paperqa3-high`) | Deeper search to check the fast answer |

Task IDs are in `_task_ids.json`. Fetch a task with
`EdisonClient(api_key=...).get_task(task_id=..., verbose=True)`.
