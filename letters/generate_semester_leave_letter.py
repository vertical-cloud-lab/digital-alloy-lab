"""Generate the FLAIME student-collaborator Letter of Collaboration template.

Creates a Word (.docx) letter on a BYU-styled letterhead that each BYU
undergraduate student collaborator populates and signs themselves,
committing to enroll in a reduced course load (with up to 6 research
credit hours) and to work the maximum hours permitted for BYU
undergraduate student employees during the funded grant period \u2014 20
hours per week during Fall/Winter semesters and up to 40 hours per week
during Spring/Summer terms (BYU Student Employment policy; see
https://hrs.byu.edu/general-information-about-student-employees and
https://finserve.byu.edu/student-work-hours). A true "semester of leave"
is not used because BYU student employees must remain enrolled to work on
campus.

The body uses the strict 2-sentence Letter of Collaboration or Access format
required by FOA DE-FOA-0003612 (Genesis Mission, Topic 3-B), so the resulting
letter can be filed in Appendix 7 of the proposal as-is.

Usage
-----
    python letters/generate_semester_leave_letter.py

Output
------
    letters/semester-leave-collaboration-letter.docx

Notes
-----
* The header embeds the BYU medallion (`letters/assets/byu-medallion.png`)
  alongside a "BRIGHAM YOUNG UNIVERSITY" wordmark in BYU Navy
  (PMS 281, hex #002E5D). The signer can swap the medallion image for an
  alternate official mark from https://brand.byu.edu/ if desired.
* The letter is pre-filled with realistic example values (date, signer
  name, contact info). Every field that the student signing the letter
  must replace is **highlighted in yellow** in the generated `.docx` so
  it is visually obvious what to overwrite. A short instructions block at
  the top of the document (printed in light gray and removed before
  signing) explains the workflow.
"""
from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

# Project metadata --- keep consistent with
# genesis-mission-proposal/flaime-genesis-proposal.tex
PROJECT_TITLE = (
    "FLAIME (Fast Learning AI for Mineral Efficiency): Autonomous Discovery "
    "and Qualification of Critical-Mineral-Lean Alloys for Clean Energy"
)
FOA_NUMBER = "DE-FOA-0003612"
PI_SALUTATION = "Dear Prof. Sterling G. Baird:"

BYU_NAVY = RGBColor(0x00, 0x2E, 0x5D)  # PMS 281

LOGO_PATH = Path(__file__).resolve().parent / "assets" / "byu-medallion.png"

# Example values pre-filled in the template. Each student signing the
# letter should overwrite these with their own information. Every field
# listed here is rendered with a yellow highlight in the generated .docx
# so it is visually obvious what to replace.
EXAMPLE_DATE = "May 1, 2026"
EXAMPLE_NAME = "Jane A. Smith"
EXAMPLE_TITLE = "Undergraduate Research Assistant"
EXAMPLE_DEPARTMENT = "Department of Mechanical Engineering"
EXAMPLE_STREET = "350 EB, Engineering Building"
EXAMPLE_EMAIL = "jane_smith@byu.edu"
EXAMPLE_PHONE = "(801) 422-0000"

# Light-gray instructions printed at the top of the .docx for the student
# signing the letter. Should be deleted before signing/sending.
FILL_IN_INSTRUCTIONS = (
    "INSTRUCTIONS (delete this paragraph before signing): This letter is "
    "filled out and signed by you, the student collaborator. Replace every "
    "yellow-highlighted field below \u2014 date, your name, your role, your "
    "department, address, email, and phone \u2014 with your own information, "
    "then print and sign the letter. Do not modify the body paragraph; the "
    "FOA requires the strict two-sentence wording shown."
)

OUTPUT_PATH = (
    Path(__file__).resolve().parent / "semester-leave-collaboration-letter.docx"
)


def _add_highlight(run, color: str = "yellow") -> None:
    """Apply a Word text-highlight color (e.g., 'yellow') to ``run``."""
    rPr = run._r.get_or_add_rPr()
    highlight = OxmlElement("w:highlight")
    highlight.set(qn("w:val"), color)
    rPr.append(highlight)


def _add_fill_in_run(paragraph, text: str):
    """Add ``text`` to ``paragraph`` as a yellow-highlighted fill-in run."""
    run = paragraph.add_run(text)
    _add_highlight(run)
    return run


def _add_letterhead(doc: Document) -> None:
    """Add a BYU letterhead (medallion + wordmark) at the top of the document."""
    # Two-column borderless table: medallion on the left, wordmark on the right.
    table = doc.add_table(rows=1, cols=2)
    table.autofit = False
    table.columns[0].width = Inches(1.1)
    table.columns[1].width = Inches(5.4)

    logo_cell, text_cell = table.rows[0].cells
    logo_cell.width = Inches(1.1)
    text_cell.width = Inches(5.4)
    logo_cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    text_cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    if LOGO_PATH.exists():
        logo_para = logo_cell.paragraphs[0]
        logo_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        logo_para.add_run().add_picture(str(LOGO_PATH), width=Inches(0.95))
    else:
        # Fall back to a "Y" glyph if the medallion asset is missing.
        logo_para = logo_cell.paragraphs[0]
        logo_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = logo_para.add_run("Y")
        run.bold = True
        run.font.size = Pt(40)
        run.font.color.rgb = BYU_NAVY

    wordmark_para = text_cell.paragraphs[0]
    wordmark_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = wordmark_para.add_run("BRIGHAM YOUNG UNIVERSITY")
    run.bold = True
    run.font.size = Pt(20)
    run.font.color.rgb = BYU_NAVY

    tagline_para = text_cell.add_paragraph()
    tagline_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = tagline_para.add_run(
        f"{EXAMPLE_DEPARTMENT}  \u2022  Provo, Utah  84602"
    )
    run.font.size = Pt(10)
    run.font.color.rgb = BYU_NAVY
    _add_highlight(run)

    # Horizontal rule (a bottom border on an empty paragraph) below the table.
    rule = doc.add_paragraph()
    p_pr = rule._p.get_or_add_pPr()
    p_bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "8")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "002E5D")
    p_bdr.append(bottom)
    p_pr.append(p_bdr)


def _add_signature_block(doc: Document) -> None:
    doc.add_paragraph("Sincerely,")
    doc.add_paragraph()  # space for handwritten signature
    doc.add_paragraph()
    for line in (
        EXAMPLE_NAME,
        EXAMPLE_TITLE,
        f"{EXAMPLE_DEPARTMENT}, Brigham Young University",
        EXAMPLE_STREET,
        "Provo, UT 84602",
        EXAMPLE_EMAIL,
        EXAMPLE_PHONE,
    ):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        _add_fill_in_run(p, line)


def build_letter(output_path: Path = OUTPUT_PATH) -> Path:
    doc = Document()

    # 1-inch margins all around
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Default body font: 11pt Times New Roman
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(11)

    _add_letterhead(doc)

    # Instructions block (light gray, italic) — to be deleted before sending.
    doc.add_paragraph()
    instr = doc.add_paragraph()
    instr_run = instr.add_run(FILL_IN_INSTRUCTIONS)
    instr_run.italic = True
    instr_run.font.size = Pt(9)
    instr_run.font.color.rgb = RGBColor(0x80, 0x80, 0x80)

    # Date
    doc.add_paragraph()
    date_para = doc.add_paragraph()
    _add_fill_in_run(date_para, EXAMPLE_DATE)

    # Salutation
    doc.add_paragraph()
    doc.add_paragraph(PI_SALUTATION)

    # Body --- strict 2-sentence Letter of Collaboration or Access format
    body = doc.add_paragraph()
    body.add_run(
        f'If your application entitled, "{PROJECT_TITLE}," is selected for '
        f"funding under {FOA_NUMBER}, it is my intent to collaborate in this "
        "research by enrolling in a reduced course load (including up to 6 "
        "research credit hours) during Fall and Winter semesters of the "
        "funded grant period and working the maximum hours permitted for BYU "
        "undergraduate student employees \u2014 20 hours per week during Fall "
        "and Winter semesters and up to 40 hours per week during Spring and "
        "Summer terms \u2014 toward the development of novel, high-performing "
        "Aluminum alloys. "
    )
    body.add_run("Thank you for the opportunity to participate.")

    doc.add_paragraph()
    _add_signature_block(doc)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    return output_path


if __name__ == "__main__":
    path = build_letter()
    print(f"Wrote {path}")
