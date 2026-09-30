from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Table, TableStyle


def create_report(result: dict) -> bytes:
    buffer = BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1.7 * cm, leftMargin=1.7 * cm)
    styles = getSampleStyleSheet()
    story = [Paragraph("Resume Match Report", styles["Title"]), Spacer(1, 12)]
    story.append(Paragraph(f"<b>Match score:</b> {result['match_score']} / 100", styles["Heading2"]))
    story.append(Paragraph(result["score_explanation"], styles["BodyText"]))
    story.append(Spacer(1, 10))
    for heading, key in [
        ("Candidate summary", "candidate_summary"),
        ("Matched skills", "matched_skills"),
        ("Skill gaps", "skill_gaps"),
        ("Resume improvements", "resume_improvements"),
        ("Interview questions", "interview_questions"),
        ("Missing information", "missing_information"),
    ]:
        value = result[key]
        text = value if isinstance(value, str) else "; ".join(value) or "None identified"
        story.extend([Paragraph(heading, styles["Heading2"]), Paragraph(text, styles["BodyText"]), Spacer(1, 8)])
    table = Table([["Important", "This report is an assistive comparison, not a hiring decision."]], colWidths=[3 * cm, 13 * cm])
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#e9f5ff")), ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("PADDING", (0, 0), (-1, -1), 6)]))
    story.append(table)
    document.build(story)
    return buffer.getvalue()
