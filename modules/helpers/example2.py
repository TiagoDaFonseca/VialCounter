# Import FPDF class
from fpdf import FPDF

# Create instance of FPDF class
# Letter size paper, use inches as unit of measure
pdf = FPDF(format='letter', unit='in')

# Add new page. Without this you cannot create the document.
pdf.add_page()

# Remember to always put one of these at least once.
pdf.set_font('Times', '', 10.0)

# Effective page width, or just epw
epw = pdf.w - 2 * pdf.l_margin

# Set column width to 1/4 of effective page width to distribute content
# evenly across table and page
col_width = epw / 4

# Since we do not need to draw lines anymore, there is no need to separate
# headers from data matrix.

data = [['First name', 'Last name', 'Age', 'City'],
        ['Jules', 'Smith', 34, 'San Juan'],
        ['Mary', 'Ramos', 45, 'Orlando'], [
            'Carlson', 'Banks', 19, 'Los Angeles']
        ]

# Document title centered, 'B'old, 14 pt
pdf.set_font('Times', 'B', 14.0)
pdf.cell(epw, 0.0, 'Demographic data', align='C')
pdf.set_font('Times', '', 10.0)
pdf.ln(0.5)

# Text height is the same as current font size
th = pdf.font_size

for row in data:
    for datum in row:
        # Enter data in colums
        # Notice the use of the function str to coerce any input to the
        # string type. This is needed
        # since pyFPDF expects a string, not a number.
        pdf.cell(col_width, th, str(datum), border=1)
    pdf.ln(th)

# Line break equivalent to 4 lines
pdf.ln(4 * th)

pdf.set_font('Times', 'B', 14.0)
pdf.cell(epw, 0.0, 'With more padding', align='C')
pdf.set_font('Times', '', 10.0)
pdf.ln(0.5)

# Here we add more padding by passing 2*th as height
for row in data:
    for datum in row:
        # Enter data in colums
        pdf.cell(col_width, 2 * th, str(datum), border=1)

    pdf.ln(2 * th)

pdf.output('table-using-cell-borders.pdf', 'F')