from django.shortcuts import render
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from .models import EnrolmentRatio
from .models import EnrolmentRatio4_1_1
from .models import EnrolmentRatioMarksOnly4_1_2
from .models import SuccessRateStipulatedPeriod
from .models import studentspassedwithbacklogs


# ✅ HOME PAGE (No login required)
def criterion4_home(request):
    return render(request, "criterion4_home.html")


# ✅ PDF GENERATION (Table 4.1 - Enrolment Ratio)
def enrolment_ratio_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Table_4_1_Intake_Information.pdf"'

    # Set up the document in Landscape
    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()
    elements = []

    # ---------------- TITLE SECTION ----------------
    elements.append(Paragraph("<b>Criterion 4 – Students’ Performance</b>", styles['Title']))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>Table No. 4.1 : Intake Information</b>", styles['Heading2']))
    elements.append(Spacer(1, 15))

    # ---------------- DATA FETCHING ----------------
    # Fetching last 6 years
    records = list(EnrolmentRatio.objects.order_by('-academic_year')[:6])
    
    # Ensure list is exactly 6 items long to prevent index errors
    while len(records) < 6:
        records.append(None)

    # Helper function to safely get attributes
    def val(index, field):
        if records[index] and hasattr(records[index], field):
            return getattr(records[index], field)
        return "-"

    # ---------------- TABLE DATA STRUCTURE ----------------
    # Row 0 & 1 are headers (Row 1 uses \n for the line break seen in image)
    table_data = [
        ["Item", "Academic Year", "", "", "", "", ""],
        [
            "", 
            "CAY\n(2023-24)", 
            "CAY m1\n(2022-23)", 
            "CAY m2\n(2021-22)", 
            "CAY m3\n(2020-21)", 
            "CAY m4\n(2019-20)", 
            "CAY m5\n(2018-19)"
        ],
        [
            "Sanctioned intake strength of the program (N)",
            val(0, "sanctioned_intake"), val(1, "sanctioned_intake"), val(2, "sanctioned_intake"),
            val(3, "sanctioned_intake"), val(4, "sanctioned_intake"), val(5, "sanctioned_intake")
        ],
        [
            "Students admitted through state level counseling (N1)",
            val(0, "first_year_admitted"), val(1, "first_year_admitted"), val(2, "first_year_admitted"),
            val(3, "first_year_admitted"), val(4, "first_year_admitted"), val(5, "first_year_admitted")
        ],
        [
            "Students admitted through institute level quota (N2)",
            val(0, "lateral_entry"), val(1, "lateral_entry"), val(2, "lateral_entry"),
            val(3, "lateral_entry"), val(4, "lateral_entry"), val(5, "lateral_entry")
        ],
        [
            "Students admitted through lateral entry (N3)",
            val(0, "separate_division"), val(1, "separate_division"), val(2, "separate_division"),
            val(3, "separate_division"), val(4, "separate_division"), val(5, "separate_division")
        ],
        [
            "Total number of students admitted (N1 + N2 + N3)",
            val(0, "total_admitted"), val(1, "total_admitted"), val(2, "total_admitted"),
            val(3, "total_admitted"), val(4, "total_admitted"), val(5, "total_admitted")
        ],
    ]



    # ---------------- TABLE STYLING ----------------
    # Widths: Item column is wider (320), year columns are equal (75 each)
    table = Table(table_data, colWidths=[320, 75, 75, 75, 75, 75, 75])

    style = TableStyle([
        # Merge "Item" vertically
        ('SPAN', (0, 0), (0, 1)),
        # Merge "Academic Year" horizontally across 6 columns
        ('SPAN', (1, 0), (6, 0)),

        # Background Color (matching the Cyan/Light Blue from image)
        ('BACKGROUND', (0, 0), (6, 1), colors.HexColor('#CCFFFF')),
        
        # Grid and Borders
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        
        # Alignment
        ('ALIGN', (0, 0), (-1, 1), 'CENTER'),     # Center headers
        ('ALIGN', (1, 2), (-1, -1), 'CENTER'),    # Center data numbers
        ('ALIGN', (0, 2), (0, -1), 'LEFT'),       # Left align item text
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Font styling
        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 1), 10),
        ('FONTSIZE', (0, 2), (-1, -1), 9),
        
        # Padding for readability
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ])
    
    table.setStyle(style)
    elements.append(table)

    footer_text = "<b>Table No. 4.1 : Intake Information </b>"
    elements.append(Paragraph(footer_text, styles['Normal']))

# ---------------- PREVIOUS TABLE ENDS HERE ----------------
    elements.append(Spacer(1, 30)) # Space after the intake table
         
 # ---------------- BUILD PDF ----------------
    doc.build(elements)
    return response

#4.1.1 PDF GENERATION
def enrolment_ratio_pdf_4_1(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="Table_4_1_1_4_1_2.pdf"'

    # PDF Document Setup
    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()
    elements = []

    # ---------------- TITLE SECTION ----------------
    elements.append(Paragraph("<b>Criterion 4 – Students’ Performance</b>", styles["Title"]))
    elements.append(Spacer(1, 10))

    # ---------------- FORMULA SECTION ----------------
    elements.append(Paragraph("<b>Enrolment Ratio Formula:</b>", styles["Heading3"]))
    elements.append(Spacer(1, 8))

    fraction_table = Table([
        ["Enrolment Ratio =", "(N1 + N2)"],
        ["", ""],
        ["", "N"],
    ], colWidths=[140, 80])

    fraction_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('LINEABOVE', (1, 2), (1, 2), 1, colors.black),
        ('SPAN', (0, 0), (0, 2)),
    ]))

    elements.append(fraction_table)
    elements.append(Spacer(1, 15))

    # ---------------- TABLE 4.1.1 TITLE ----------------
    elements.append(Paragraph("<b>Following Table No. 4.1 shows Average Enrolment Ratio</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    # ---------------- FETCH DATA ----------------
    record = EnrolmentRatio4_1_1.objects.last()

    # ---------------- CALCULATIONS ----------------
    if record:
        total_cay = record.N1 + record.N2
        total_m1 = record.N1_m1 + record.N2_m1
        total_m2 = record.N1_m2 + record.N2_m2

        ratio_cay = round((total_cay / record.N) * 100, 2) if record.N != 0 else 0
        ratio_m1 = round((total_m1 / record.N_m1) * 100, 2) if record.N_m1 != 0 else 0
        ratio_m2 = round((total_m2 / record.N_m2) * 100, 2) if record.N_m2 != 0 else 0

        average_enrolment = round((ratio_cay + ratio_m1 + ratio_m2) / 3, 2)
    else:
        total_cay = total_m1 = total_m2 = "-"
        ratio_cay = ratio_m1 = ratio_m2 = "-"
        average_enrolment = "-"

    # ---------------- TABLE 4.1.1 DATA ----------------
    table_data_4_1_1 = [
        ["Item", "No. of students", "", ""],
        [
            "(Students enrolled at the First Year Level\non average basis during the previous three academic\nyears including the current academic year)",
            "CAY\n(2023-24)",
            "CAY m1\n(2022-23)",
            "CAY m2\n(2021-22)",
        ],
        ["N1", record.N1 if record else "-", record.N1_m1 if record else "-", record.N1_m2 if record else "-"],
        ["N2", record.N2 if record else "-", record.N2_m1 if record else "-", record.N2_m2 if record else "-"],
        ["N",  record.N  if record else "-", record.N_m1  if record else "-", record.N_m2  if record else "-"],
        ["Total (N1+N2)", total_cay, total_m1, total_m2],
        ["Enrolment Ratio  [((N1+N2)/N)*100]", ratio_cay, ratio_m1, ratio_m2],
        ["Average Enrolment", average_enrolment, "", ""],
    ]

    table_4_1_1 = Table(table_data_4_1_1, colWidths=[320, 110, 110, 110])

    style_4_1_1 = TableStyle([
        ('SPAN', (1, 0), (3, 0)),  # Merge "No. of students"

        ('BACKGROUND', (0, 0), (3, 1), colors.HexColor("#CCFFFF")),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        ('ALIGN', (0, 0), (-1, 1), 'CENTER'),
        ('ALIGN', (1, 2), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 2), (0, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 1), 10),
        ('FONTSIZE', (0, 2), (-1, -1), 9),

        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ])

    table_4_1_1.setStyle(style_4_1_1)
    elements.append(table_4_1_1)

    elements.append(Spacer(1, 8))
    elements.append(Paragraph("<b>Table No. 4.1.1 : Average Enrolment Ratio</b>", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # ---------------- TABLE 4.1.2 TITLE ----------------
    elements.append(Paragraph("<b>Following Table No. 4.1.2 shows Enrolment Ratio.</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    # ---------------- TABLE 4.1.2 DATA FROM ADMIN (ONLY MARKS) ----------------
    marks_obj = EnrolmentRatioMarksOnly4_1_2.objects.last()

    table_4_1_2_data = [
        ["Item\n(Students enrolled at the First Year Level on average basis during the\nprevious three academic years including the current academic year)", "Marks"],
        [">=90% Students", str(marks_obj.marks_90 if marks_obj else 20)],
        [">=80% Students", str(marks_obj.marks_80 if marks_obj else 18)],
        [">=70% Students", str(marks_obj.marks_70 if marks_obj else 16)],
        [">=60% Students", str(marks_obj.marks_60 if marks_obj else 12)],
        [">=50% Students", str(marks_obj.marks_50 if marks_obj else 8)],
        ["<50% Students", str(marks_obj.marks_below_50 if marks_obj else 0)],
    ]

    table_4_1_2 = Table(table_4_1_2_data, colWidths=[520, 120])

    style_4_1_2 = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#CCFFFF")),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('FONTSIZE', (0, 0), (-1, -1), 10),

        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ])

    table_4_1_2.setStyle(style_4_1_2)
    elements.append(table_4_1_2)

    elements.append(Spacer(1, 8))
    elements.append(Paragraph("<b>Table No. 4.1.2 : Enrolment Ratio</b>", styles["Normal"]))

    # ---------------- BUILD PDF ----------------
    doc.build(elements)
    return response

# ✅ PDF GENERATION (Table 4.2 - Success Rate Without Backlogs)
def success_rate_nobacklog_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Table_4_2_No_Backlog.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20,
    )

    styles = getSampleStyleSheet()
    elements = []

    # ---------------- TITLE ----------------
    elements.append(Paragraph("<b>4.2. Success Rate in the stipulated period of the program</b>", styles["Title"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        "<b>Following Table No. 4.2 Number of students passed without backlogs in stipulated year of study</b>",
        styles["Heading2"]
    ))
    elements.append(Spacer(1, 10))

    # ---------------- FETCH DATA (LAST 6 YEARS) ----------------
    records = list(SuccessRateStipulatedPeriod.objects.all().order_by("-id")[:6])
    records.reverse()  # old to new

    # ---------------- TABLE HEADER ----------------
    table_data = [
        [
            "Year of entry",
            "N1 + N2 + N3\n(As defined above)",
            "Number of students who have successfully\npassed without backlogs in any year of study",
            "",
            ""
        ],
        ["", "", "I Year", "II Year", "III Year"]
    ]

    # ---------------- TABLE ROWS ----------------
    for r in records:
        table_data.append([
            r.year_of_entry,
            r.n1_n2_n3_total,
            r.passed_year_1 if r.passed_year_1 is not None else "-",
            r.passed_year_2 if r.passed_year_2 is not None else "-",
            r.passed_year_3 if r.passed_year_3 is not None else "-",
        ])

    # ---------------- CREATE TABLE ----------------
    table = Table(table_data, colWidths=[170, 120, 150, 150, 150])

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("BACKGROUND", (0, 0), (-1, 1), colors.lightblue),
        ("FONTNAME", (0, 0), (-1, 1), "Helvetica-Bold"),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        # Merge header cells
        ("SPAN", (0, 0), (0, 1)),
        ("SPAN", (1, 0), (1, 1)),
        ("SPAN", (2, 0), (4, 0)),
    ]))

    elements.append(table)

    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "<b>Table No. 4.2 : Number of students passed without backlogs in stipulated year of study</b>",
        styles["Heading3"]
    ))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("LYG : Last Year Graduate", styles["Normal"]))
    elements.append(Paragraph("LYG 1 : Last Year Graduate minus 1", styles["Normal"]))
    elements.append(Paragraph("LYG 2 : Last Year Graduate minus 2", styles["Normal"]))

    doc.build(elements)
    return response

# ✅ PDF GENERATION (Table 4.3 - students passed with backlogs )
def students_passed_with_backlogs_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Table_4_2_No_Backlog.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20,
    )

    styles = getSampleStyleSheet()
    elements = []

    # ---------------- TITLE ----------------

    elements.append(Paragraph(
        "<b>Following Table No. 4.3 shows number of students passed with backlogs in stipulated year of study.</b>",
        styles["Heading2"]
    ))
    elements.append(Spacer(1, 10))

    # ---------------- FETCH DATA (LAST 6 YEARS) ----------------
    records = list(studentspassedwithbacklogs.objects.all().order_by("-id")[:6])
    records.reverse()  # old to new

    # ---------------- TABLE HEADER ----------------
    table_data = [
        [
            "Year of entry",
            "N1 + N2 + N3\n(As defined above)",
            "Number of students who have successfully passed\n(Students with backlog in stipulated period of study)",
            "",
            ""
        ],
        ["", "", "I Year", "II Year", "III Year"]
    ]

    # ---------------- TABLE ROWS ----------------
    for r in records:
        table_data.append([
            r.year_of_entry,
            r.n1_n2_n3_total,
            r.passed_year_1 if r.passed_year_1 is not None else "-",
            r.passed_year_2 if r.passed_year_2 is not None else "-",
            r.passed_year_3 if r.passed_year_3 is not None else "-",
        ])

    # ---------------- CREATE TABLE ----------------
    table = Table(table_data, colWidths=[170, 120, 150, 150, 150])

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("BACKGROUND", (0, 0), (-1, 1), colors.lightblue),
        ("FONTNAME", (0, 0), (-1, 1), "Helvetica-Bold"),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        # Merge header cells
        ("SPAN", (0, 0), (0, 1)),
        ("SPAN", (1, 0), (1, 1)),
        ("SPAN", (2, 0), (4, 0)),
    ]))

    elements.append(table)

    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "<b>Table No. 4.3 : Number of students passed with backlogs in stipulated year of study</b>",
        styles["Heading3"]
    ))

    doc.build(elements)
    return response