# Cleaning test sieves between alloys (issue #234)

The lab sieved a bronze (Cu-Sn) powder through its 63 µm and 250 µm test sieves and next wants to
sieve aluminum powder for LPBF through the same sieves. Issue #234 asked for an Edison Scientific
query on how to clean the sieves so the bronze does not contaminate the aluminum.

Two Edison jobs were submitted on 2026-11-03 with the same question (`question.txt`):

| Key | Job | Why |
|-----|-----|-----|
| `literature` | LITERATURE (`job-futurehouse-paperqa3`) | Fast answer |
| `literature_high` | LITERATURE_HIGH (`job-futurehouse-paperqa3-high`) | Deeper search to check the fast answer |

Both finished with status `success`: LITERATURE_HIGH at about 21:47 UTC (87 evidence contexts) and
LITERATURE by 22:04 UTC (107 evidence contexts). Task IDs are in `_task_ids.json`. Fetch a task with
`EdisonClient(api_key=...).get_task(task_id=..., verbose=True)`.

| File | Contents |
|------|----------|
| `question.txt` | The question sent to both jobs |
| `literature-high.md`, `literature.md` | Each job's answer with its reference list |
| `literature-high.artifacts.md` | Tables the LITERATURE_HIGH agent built (the LITERATURE job made none) |
| `literature-high.verbose.json`, `literature.verbose.json` | Full trajectories |

Before commit, the trajectory JSON had account fields (`user`, `build_owner`, `permitted_accessors`),
query cost, and the raw page text returned by Edison's `read_text` tool removed, since this repo is
public. Summaries of each evidence passage, the agent's messages and tool calls, and the source metadata
(titles, authors, DOIs) are kept.

Two statements in the LITERATURE_HIGH answer are wrong and should not be reused: the Al–Sn system has no
intermetallic compounds (it is a simple eutectic at about 228 °C), and Cu-bearing particles in aluminum
have a large X-ray CT contrast (8.96 vs 2.70 g/cm³), not a small one.
