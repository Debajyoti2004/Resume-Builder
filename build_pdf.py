from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

def convert_to_pdf(output_file: str, content: dict):
    doc = SimpleDocTemplate(output_file, pagesize=A4, rightMargin=inch, leftMargin=inch, topMargin=inch, bottomMargin=inch)
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = ParagraphStyle('Heading1', parent=styles['Heading1'], spaceAfter=6)
    subheading_style = ParagraphStyle('Heading2', parent=styles['Heading2'], spaceAfter=4)
    body_style = styles['BodyText']
    
    elements = []

    elements.append(Paragraph(content['name'], title_style))
    elements.append(Paragraph(f"Email: {content['email']} | Phone: {content['phone']}", body_style))
    elements.append(HRFlowable(width="100%", thickness=1, color="black"))

    elements.append(Paragraph("Objective", heading_style))
    elements.append(Paragraph(content['objective'], body_style))
    elements.append(HRFlowable(width="100%", thickness=1, color="black"))

    elements.append(Paragraph("Experience", heading_style))
    for exp in content['experience']:
        elements.append(Paragraph(f"{exp['job_title']} at {exp['company_name']} ({exp['years']})", body_style))
        for project in exp['projects']:
            for key, value in project.items():
                if key.startswith('project'):
                    elements.append(Paragraph(f"{value} ({project['timeline']})", subheading_style))
                elif key == 'description':
                    elements.append(Paragraph(value, body_style))
        elements.append(HRFlowable(width="100%", thickness=1, color="black"))

    elements.append(Paragraph("Skills", heading_style))
    elements.append(Paragraph(", ".join(content['skills']), body_style))
    elements.append(HRFlowable(width="100%", thickness=1, color="black"))

    elements.append(Paragraph("Education", heading_style))
    for edu in content['education']:
        elements.append(Paragraph(f"{edu['degree']} from {edu['university']} ({edu['year']})", body_style))
    elements.append(HRFlowable(width="100%", thickness=1, color="black"))
    
    doc.build(elements)
