# Drop: Navy copper alloys, rod and filler wire, for vertical-cloud-lab/byu-vcl#286

Made on 2026-10-17 in [digital-alloy-lab#123](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/123) ([run](https://github.com/vertical-cloud-lab/digital-alloy-lab/actions/runs/39058390371)). It follows the first drop, `../2026-10-17-copper-sourcing/`, which is on branch `claude/issue-123-20261017-0509`, and it also feeds the ONR YIP copper-nickel draft (#117). If it's copied into the `sgbaird/agent-staging` drop box, the path is `for/vertical-cloud-lab/byu-vcl/2026-10-17-navy-copper-alloys/`.

Everything here comes from public vendor pages and search results. Nothing comes from a private source.

| File | sha256 | Source | Purpose |
|---|---|---|---|
| `README.md` | `5cd84f341a7122ad4be41ea6a54097df9f913424657cb05915017be7d6eb7507` | Written in that session from vendor pages, McMaster category tables (headless Chrome on the runner) and web search, all read 2026-10-17 | Summary of the best rod and filler-wire option per alloy, plus melting notes, ready to post |
| `navy_copper_alloys.csv` | `570ee462a2452e13bd170173d8f689d69c387823b27b1cfe81a97ca786b759f9` | The same reads, 141 listings | One row per listing, size and package: vendor, part number, link, diameter and tolerance, length or weight, price, computed $/ft or $/lb, stock or lead time, cert, quote-only flag, specs, and how each was read |

To fetch one file at the commit named in the digital-alloy-lab#123 comment:

```
gh api "repos/vertical-cloud-lab/digital-alloy-lab/contents/outbox/byu-vcl/2026-10-17-navy-copper-alloys/<file>?ref=<sha>" -H "Accept: application/vnd.github.raw" > <file>
```
