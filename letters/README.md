# FLAIME — Letter Templates

Sendable Word (.docx) letter templates for the FLAIME Genesis Mission
proposal (FOA `DE-FOA-0003612`, Topic 3-B).

## Available templates

| File | Purpose |
| --- | --- |
| `semester-leave-collaboration-letter.docx` | Letter of Collaboration in which a BYU **undergraduate student collaborator** commits to a **reduced course load (including up to 6 research credit hours)** and to working the **maximum hours allowed for BYU student employees** (20 hr/wk Fall/Winter, up to 40 hr/wk Spring/Summer) on FLAIME during the funded grant period. Each student fills out and signs their own copy. |

> **Note on naming.** An earlier draft used a "semester of leave" framing.
> BYU policy does not permit a student employee to take a leave of absence
> from coursework while continuing to work on campus, so the body wording
> now reflects a reduced-course-load + maximum-allowed-hours commitment
> instead. The filename is kept for continuity. See
> [BYU Student Work Hours](https://finserve.byu.edu/student-work-hours)
> and [Requirements for Student Employees](https://hrs.byu.edu/general-information-about-student-employees).

## Regenerating

The `.docx` files are produced by Python scripts in this directory using
[`python-docx`](https://python-docx.readthedocs.io/). To rebuild after
editing project metadata (title, FOA number, salutation):

```bash
pip install python-docx
python letters/generate_semester_leave_letter.py
```

## BYU letterhead

The generated letters use the official BYU medallion
(`letters/assets/byu-medallion.png`) alongside a "BRIGHAM YOUNG UNIVERSITY"
wordmark in BYU navy (PMS 281, `#002E5D`). The medallion is sourced from
[Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Brigham_Young_University_medallion.svg)
and may be replaced with an alternate official mark from
<https://brand.byu.edu/> if the signing department prefers.

## Example data and fill-in workflow

Each student collaborator fills out and signs their own copy of this
letter, so the template is designed to be obvious to fill out:

* The body paragraph is **fixed** — it must match the FOA's strict
  two-sentence Letter of Collaboration or Access wording and should not be
  edited.
* Every field that needs to be replaced (date, signer name, role,
  department, address, email, phone) is **highlighted in yellow** in the
  generated `.docx` and pre-populated with realistic example values
  (`May 1, 2026`, `Jane A. Smith`, `Undergraduate Research Assistant`, BYU
  Mechanical Engineering address, `jane_smith@byu.edu`, `(801) 422-0000`).
* A short light-gray instructions block at the top of the document
  summarizes the workflow and is meant to be deleted before signing.

Edit the `EXAMPLE_*` constants at the top of
`letters/generate_semester_leave_letter.py` and re-run the script if you
prefer different defaults baked into the template.

## FOA compliance notes

* All letters here follow the **strict 2-sentence Letter of Collaboration
  or Access** format required by the FOA (see
  `genesis-mission-proposal/flaime-genesis-proposal.tex`, "Quick-Reference:
  Letter Types"). They must not read as recommendations or endorsements.
* Letters of *commitment* (from funded team-member institutions) are a
  different document type and live in the proposal LaTeX source.
* All signed letters belong in **Appendix 7 (Other Attachments)** of the
  Field-8 submission.

## BYU student-employment policy notes (PI checklist)

When budgeting student effort backed by these letters, confirm with BYU
Human Resources / Student Employment:

* **Hour caps.** Undergraduate student employees are limited to 20 hr/wk
  during Fall/Winter and may work up to 40 hr/wk during Spring/Summer
  terms; the rolling annual average must stay at or below 28 hr/wk for
  ACA compliance.
* **Enrollment requirement.** A student employee must remain enrolled
  (≥ 6 credit hours for U.S. undergrads in Fall/Winter); a true semester
  of leave is incompatible with continued on-campus employment.
* **Wage cap.** The annual BYU Student Employee Hourly Pay Scale sets a
  ceiling on undergraduate hourly rates; rates above the published cap
  require an HR-approved exception. Verify the proposed rate against the
  current pay scale before finalizing the budget.
* **Tuition support.** Paying student tuition out of grant funds is rare
  and may require additional approvals; confirm with the College and
  Office of Research before relying on it.
