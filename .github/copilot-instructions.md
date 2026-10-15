If using Edison Scientific, you may need to wait up until 10 minutes to get the response. If you're an agent, sleep for 10 minutes (to avoid consuming requests unecessarily), and then every 5 minutes after that. Start with a 15 minute wait if using high effort literature query type. If you need to upload files, use analysis query type. See the docs: https://edisonscientific.gitbook.io/edison-cookbook/edison-client. Here is the endpoint you should use: https://api.platform.edisonscientific.com. The API key is EDISON_PLATFORM_API_KEY. Don't expose this secret, e.g., by echoing or grepping it. Pass the API key in explicitly:

```
from edison_client import EdisonClient, JobNames
client = EdisonClient(api_key=EDISON_PLATFORM_API_KEY)
```

If using Edison Analysis, refer to https://docs.edisonscientific.com/edison-client/file-management#upload for instructions on how to upload files. If able to use Context7, to better inform use of EdisonClient, see https://context7.com/future-house/edison-client-docs/llms.txt?tokens=10000

## LaTeX Proposal Build

There is a single source file: `genesis-mission-proposal/flaime-genesis-proposal.tex`. Do NOT create a separate `-clean.tex` copy. Use the Makefile:

- `make draft` — annotated PDF with DRAFT watermark and todonotes (all sections)
- `make clean-pdf` — clean PDF (no watermark, no notes, all sections still present)
- `make final` — submission-ready Field 8 PDF (also removes abstract, biosketch, budget)
- `make all` — all three

Build toggles are controlled at build time via `\def\cleanbuild{}` and `\def\submissionbuild{}`; do not manually edit `\drafttrue`/`\draftfalse` or `\submissiontrue`/`\submissionfalse`.
