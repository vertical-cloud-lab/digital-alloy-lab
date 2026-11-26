# `metal-am-contacts.csv` — schema and intended use

> **Public copy.** Named staff at partner organizations (Valimet, Thermo-Calc, AMAZEMET) are listed by role only, with their direct emails removed (`redacted-contact`). The `linkedin_path` column, which recorded the PI's own LinkedIn network, was dropped. Coverage counts below describe the original list.

**Source of truth** for FLAIME validation-print outreach. Designed to be exported to a shared Google Sheet (`File > Import > Upload > Replace current sheet`).

## Columns

| Column | Description |
|---|---|
| `organization` | Institution / company / lab name. Multiple rows per org are expected (one per named contact + one per role-based inbox). |
| `country` | ISO-style country code or short name. |
| `category` | High-level bucket: `Academic`, `National lab`, `LPBF OEM`, `Binder jet OEM`, `Atomizer OEM`, `Powder supplier`, `Service bureau`, `Industry (auto/aero)`, `Corporate R&D + alloy IP`, `Standards body`, `Funding agency`, `Software/ML`. |
| `name` | Named individual (blank for role-based inboxes like `info@…`). |
| `title` | Position / signing-authority hint. |
| `email` | Best email currently known. **Empty if not verified** — do not guess. |
| `email_verification` | One of: `verified-public` (institution contact page), `verified-publication` (peer-reviewed paper / NTRS / OSTI / Zenodo / arXiv / Scholar verified-email), `verified-corpus` (already cited in `metal-am-contacts-worldwide.md` with source), `verified-PR60` (carried over from PR #60), `fallback-general-inbox` (no public personal email found; populated with the verified general/role-based inbox of the same organization so the contact is still actionable — `name` field tells the reader who to attention-line), `NOT-FOUND-public` (no personal email found in any primary source AND no usable general inbox at the same org — route via LinkedIn / web form / colleague), `UNVERIFIED-NEEDS-CHECK` (working email exists but final click-through verification still pending), `UNVERIFIED` (no email known yet), `UNVERIFIED-from-SOSSEC-listing` (third-party defense-AM consortium roster — check before sending), `UNVERIFIED-likely-public` (looks like a generic info@ but not click-confirmed in this session), `UNVERIFIED-third-party` (only third-party aggregator pattern — not used for sending per "don't guess" policy), `redacted-contact` (public copy: a named contact removed; the role stays, and the organization's general inbox where one was listed). |
| `phone` | Optional; only role/HQ numbers — no direct mobile lines. |
| `source_url` | Where the contact / claim is sourced from (institution page, paper PDF, press release). |
| `google_scholar` | Direct Scholar profile URL where known, otherwise a search-string hint. Useful for finding corresponding-author emails on PDFs. |
| `al_am_relevance` | Why this contact matters for FLAIME validation printing. |
| `notes` | Anything else — e.g. "senior signing authority", "verify email before outreach", "pair with senior co-signer". |

## Verification policy (per sgbaird, comment 4338780652)

> *"Once you identify a few people from the company, you can likely find an email if they are more research-oriented and have a google scholar profile. Be thorough. Don't get lazy. … verify that the emails are accurate (if not publicly listed on an institution page, look for articles they published and see if their contact info is listed there) and don't make guesses on emails."*

- An email **with a `verified-*` status** has been confirmed against the listed `source_url` and is safe to use.
- An email **with an `UNVERIFIED-*` status** is a working hypothesis (corresponding-author convention, public consortium roster, or domain pattern) and **must be confirmed before outreach** — typically by:
  1. Visiting the institution faculty / staff directory (Cranfield, MPIE, UC Berkeley, etc.).
  2. Opening a recent first/last-author publication PDF and reading the corresponding-author email at the foot of the title page.
  3. Checking the lab's official Contact / People page.
  4. (Last resort) sending the role-based `info@` / `sales@` with `ATTN: <name>`.
- A **blank email cell** means no candidate has been found yet.

## Coverage status (as of v13)

- **130 rows** total.
- **100 verified personal or role-based emails** (verified-public 52 + verified-PR60 33 + verified-publication 9 + verified-corpus 6).
- **18 fallback-general-inbox** rows — named individual where no public personal email was found, populated with the verified general/role-based inbox of the same organization (e.g., HRL/Hunter Martin → `additive@hrl.com`, Sintavia/Brian Neff → `info@sintavia.com`, Constellium CRV/Shahani → `aheadd@constellium.com`, EOS/Grinkevich → `info@eos.info`). Use `ATTN: <name>` in the message.
- **5 NOT-FOUND-public** rows — no personal email and no usable org inbox; route via LinkedIn DM, personal web form, or a verified colleague at the same institution (e.g., NASA MSFC/O'Connor → `ajpo.space` contact form; NASA MSFC/Jones → reach via Paul Gradl; UTEP Keck/Wicker → reach via Francisco Medina; NVIDIA/Ong + IBM/Pitera → LinkedIn DM only).
- **7 remaining UNVERIFIED-* rows** — see status field for type; check before any outreach.

## Companion docs

- `metal-am-contacts-worldwide.md` — the master narrative directory (665+ lines). All names in the CSV are sourced from this file unless `source_url` says otherwise.
- `metal-am-outreach-priority-top75.md` — Top-75 outreach prioritization and FOA-compliant Letter-of-Collaboration framing.
- §10g of `metal-am-contacts-worldwide.md` — export-control / international-shipping considerations (per Moataz feedback). Read before sending any letter to a non-US target.
