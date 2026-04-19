from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from ..core.database import get_db
from ..models.models import Registration, Student, Exam, Payment, User
from ..api.dependencies import get_current_student

router = APIRouter(prefix="/admit-card", tags=["Admit Card"])

@router.get("/{registration_id}")
def download_admit_card(
    registration_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    # Fetch registration
    registration = db.query(Registration).filter(
        Registration.registration_id == registration_id,
        Registration.student_id == current_student.student_id
    ).first()

    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    if registration.status != "confirmed":
        raise HTTPException(status_code=400, detail="Admit card only available after payment confirmation")

    exam = registration.exam
    student = current_student
    payment = registration.payment

    # Generate PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    elements = []

    # Title style
    title_style = ParagraphStyle(
        'Title', parent=styles['Normal'],
        fontSize=14, fontName='Helvetica-Bold',
        alignment=TA_CENTER, textColor=colors.HexColor('#4a4a8a'),
        spaceAfter=6, leading=18
    )
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Normal'],
        fontSize=11, fontName='Helvetica',
        alignment=TA_CENTER, textColor=colors.grey,
        spaceAfter=2
    )
    label_style = ParagraphStyle(
        'Label', parent=styles['Normal'],
        fontSize=10, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#333333')
    )
    value_style = ParagraphStyle(
        'Value', parent=styles['Normal'],
        fontSize=10, fontName='Helvetica',
        textColor=colors.HexColor('#555555')
    )

    # Header
    elements.append(Paragraph("VNR VIGNANA JYOTHI INSTITUTE OF ENGINEERING & TECHNOLOGY", title_style))
    elements.append(Spacer(1, 0.3*cm))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#4a4a8a')))
    elements.append(Spacer(1, 0.3*cm))

    admit_title = ParagraphStyle(
        'AdmitTitle', parent=styles['Normal'],
        fontSize=16, fontName='Helvetica-Bold',
        alignment=TA_CENTER, textColor=colors.HexColor('#4a4a8a'),
        spaceAfter=6
    )
    elements.append(Paragraph("ADMIT CARD", admit_title))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cccccc')))
    elements.append(Spacer(1, 0.5*cm))

    # Student Details Table
    student_data = [
        [Paragraph("<b>STUDENT DETAILS</b>", label_style), ""],
        ["Registration ID", f"REG-{registration.registration_id:04d}"],
        ["Student Name", student.name],
        ["Email", student.email],
        ["Branch", student.branch or "N/A"],
        ["Year", f"Year {student.year}" if student.year else "N/A"],
    ]

    student_table = Table(student_data, colWidths=[6*cm, 11*cm])
    student_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#4a4a8a')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 12),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f0f0f8')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
    ]))
    elements.append(student_table)
    elements.append(Spacer(1, 0.5*cm))

    # Exam Details Table
    exam_data = [
        [Paragraph("<b>EXAM DETAILS</b>", label_style), ""],
        ["Exam Name", exam.exam_name],
        ["Subject", exam.subject],
        ["Exam Date", exam.exam_date.strftime("%d %B %Y")],
        ["Duration", f"{exam.duration} minutes"],
        ["Total Marks", str(exam.total_marks)],
        ["Exam Fee", f"Rs. {float(exam.fee):.2f}"],
    ]

    exam_table = Table(exam_data, colWidths=[6*cm, 11*cm])
    exam_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#2e7d32')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 12),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f0f8f0')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
    ]))
    elements.append(exam_table)
    elements.append(Spacer(1, 0.5*cm))

    # Payment Details Table
    payment_data = [
        [Paragraph("<b>PAYMENT DETAILS</b>", label_style), ""],
        ["Payment Status", "CONFIRMED ✓"],
        ["Transaction ID", payment.transaction_id or "N/A"],
        ["Amount Paid", f"Rs. {float(payment.amount):.2f}"],
        ["Payment Date", payment.payment_date.strftime("%d %B %Y, %I:%M %p")],
    ]

    payment_table = Table(payment_data, colWidths=[6*cm, 11*cm])
    payment_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#1565c0')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 12),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f0f4ff')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TEXTCOLOR', (1, 1), (1, 1), colors.HexColor('#2e7d32')),
        ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
    ]))
    elements.append(payment_table)
    elements.append(Spacer(1, 0.8*cm))

    # Instructions
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cccccc')))
    elements.append(Spacer(1, 0.3*cm))

    instructions_title = ParagraphStyle(
        'InstTitle', parent=styles['Normal'],
        fontSize=11, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#c62828')
    )
    elements.append(Paragraph("Important Instructions:", instructions_title))
    elements.append(Spacer(1, 0.2*cm))

    instructions = [
        "1. Carry this admit card to the examination hall.",
        "2. Carry a valid photo ID proof (Aadhar / College ID).",
        "3. Report 30 minutes before the exam start time.",
        "4. Mobile phones and electronic devices are not allowed.",
        "5. This admit card is valid only for the mentioned exam.",
    ]
    inst_style = ParagraphStyle(
        'Inst', parent=styles['Normal'],
        fontSize=9, fontName='Helvetica',
        textColor=colors.HexColor('#555555'),
        spaceAfter=3
    )
    for inst in instructions:
        elements.append(Paragraph(inst, inst_style))

    elements.append(Spacer(1, 0.5*cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cccccc')))
    elements.append(Spacer(1, 0.3*cm))

    footer_style = ParagraphStyle(
        'Footer', parent=styles['Normal'],
        fontSize=8, fontName='Helvetica',
        alignment=TA_CENTER, textColor=colors.grey
    )
    elements.append(Paragraph("This is a computer-generated admit card and does not require a signature.", footer_style))

    doc.build(elements)
    buffer.seek(0)

    filename = f"AdmitCard_REG{registration.registration_id:04d}_{exam.subject.replace(' ', '_')}.pdf"

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
