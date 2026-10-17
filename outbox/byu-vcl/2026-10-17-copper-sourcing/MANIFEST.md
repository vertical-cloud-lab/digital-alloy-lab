# Drop: copper sourcing for vertical-cloud-lab/byu-vcl#286

Made on 2026-10-17 in [digital-alloy-lab#123](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/123) ([run](https://github.com/vertical-cloud-lab/digital-alloy-lab/actions/runs/39005236421)), because byu-vcl was out of Claude credits.

That job couldn't write to `sgbaird/agent-staging`, because its `GH_READ_PAT_STAGING` is read-only. It couldn't write to byu-vcl either, because its app token covers digital-alloy-lab only. So the drop lives in this repo. If it's copied into the drop box, the path is `for/vertical-cloud-lab/byu-vcl/2026-10-17-copper-sourcing/`.

On 2026-10-17 the GitHub API reported this repo as private, even though its CLAUDE.md calls it public. A byu-vcl session that holds only its own token may get a 404 here. Nothing in the drop comes from a private source, so it can be posted on byu-vcl#286, which is public, as it stands.

| File | sha256 | Source | Purpose |
|---|---|---|---|
| `README.md` | `0ecdaab12c36202d6ccbfbcc5a0e1eb311bd0b7530c3a91501cfb44727c352d4` | Written in that session from McMaster (headless Chrome on the runner), vendor pages and web research, all read 2026-10-17 | The answer to byu-vcl#286, ready to post as a comment |
| `mcmaster_copper_rods.csv` | `600605bc4762a3e1e22611784c0f1a40a940f31d194f45874e7548beb7ef7e35` | McMaster category pages, read 2026-10-17 | Every 1/2" to 1" row of the 11 copper-alloy rod families checked: part number, tolerance, temper, spec, and price by length |

To fetch one file at the commit named in the digital-alloy-lab#123 comment:

```
gh api "repos/vertical-cloud-lab/digital-alloy-lab/contents/outbox/byu-vcl/2026-10-17-copper-sourcing/<file>?ref=<sha>" -H "Accept: application/vnd.github.raw" > <file>
```
