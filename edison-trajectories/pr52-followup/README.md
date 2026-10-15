# PR #52 Edison follow-up queries

Kicked off 2026-04-18 from agent session addressing PR #52 reviews
4134915150 and 4135166017.  The PI asked for these queries to be fired
without waiting for completion and fetched in the next session.

See `edison-tasks.json` for task IDs.  Fetch results with
`client.get_task(task_id=tid)`.

| Key | Job | Purpose | Addresses comment |
|-----|-----|---------|-------------------|
| `apex_peer_review` | LITERATURE | Verify whether APEX (Conn 2025) is peer-reviewed and whether it has been publicly demonstrated without human monitoring; assess how sparse the available report is. | 3105662153, 3105676143 |
| `birdshot_broader` | LITERATURE_HIGH | Enumerate BIRDSHOT / Arroyave related 2022--2026 publications beyond Paramore 2025 (`literature/1-s2.0-S1359645425001120-main.pdf`) with search-space size, automation extent, and mechanical testing scope. | 3105681551 |
| `rsos_tom_analysis` | ANALYSIS (PDFs attached: `rsos.250646.pdf`, `tom-self-driving.pdf`) | Verify the "DED-based active-learning platforms discover bulk alloys at >100/week but use purchased feedstocks without LPBF or tensile qualification" claim (line 501 of proposal) against the two uploaded PDFs; if unsupported, suggest citations. | 3105689425 |
| `lpbf_atomization_precedent` | PRECEDENT | Has anyone closed-the-loop ML-driven LPBF that includes atomization? Includes AMAZEMET / ATO Lab. | 3105714330 |
| `lpbf_atomization_literature` | LITERATURE_HIGH | Parallel literature search for same question, broader. | 3105714330 |

Next session: fetch each task, compare against draft claims, update
proposal citations, and mark corresponding comments resolved.
