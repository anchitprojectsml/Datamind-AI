from io import BytesIO
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)


def generate_pdf_report(
    profile: dict,
    health: dict,
    summary_result: dict,
    dataset_name: str
):
    if not profile:
        return None

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    # 1. Document Title
    story.append(
        Paragraph("<b>DataMind AI</b>", styles["Title"])
    )
    story.append(
        Paragraph("Dataset Analysis Report", styles["Heading2"])
    )
    story.append(Spacer(1, 20))

    # 2. Dataset Metadata
    story.append(
        Paragraph(f"<b>Dataset :</b> {dataset_name}", styles["BodyText"])
    )
    story.append(
        Paragraph(f"<b>Generated :</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}", styles["BodyText"])
    )
    story.append(Spacer(1, 15))

    # 3. Dataset Profile Section
    story.append(
        Paragraph("<b>Dataset Profile</b>", styles["Heading2"])
    )
    story.append(
        Paragraph(f"Rows : {profile.get('rows', 0)}", styles["BodyText"])
    )
    story.append(
        Paragraph(f"Columns : {profile.get('columns', 0)}", styles["BodyText"])
    )
    story.append(
        Paragraph(f"Missing Values : {profile.get('total_missing_values', 0)}", styles["BodyText"])
    )
    story.append(
        Paragraph(f"Duplicate Rows : {profile.get('total_duplicate_rows', 0)}", styles["BodyText"])
    )
    story.append(Spacer(1, 15))

    # 4. Dataset Health Section
    if health:
        story.append(
            Paragraph("<b>Dataset Health</b>", styles["Heading2"])
        )
        story.append(
            Paragraph(f"Health Score : {health.get('score', 0)}/100", styles["BodyText"])
        )
        story.append(
            Paragraph(f"Grade : {health.get('grade', 'N/A')}", styles["BodyText"])
        )
        story.append(Spacer(1, 15))

    # 5. AI Consultant Summary Section
    if summary_result and summary_result.get("success"):
        story.append(
            Paragraph("<b>AI Consultant Summary</b>", styles["Heading2"])
        )
        for item in summary_result.get("summary", []):
            story.append(
                Paragraph(item, styles["BodyText"])
            )
        story.append(Spacer(1, 10))

        # 6. Recommendations
        story.append(
            Paragraph("<b>Recommendations</b>", styles["Heading2"])
        )
        for index, item in enumerate(summary_result.get("recommendations", []), start=1):
            story.append(
                Paragraph(f"{index}. {item}", styles["BodyText"])
            )
        story.append(Spacer(1, 20))

    # 7. Footer Tagline
    story.append(
        Paragraph("Generated automatically by DataMind AI.", styles["Italic"])
    )

    # Build PDF and Return Bytes Buffer
    doc.build(story)
    buffer.seek(0)
    return buffer