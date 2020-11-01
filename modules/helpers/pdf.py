from fpdf import FPDF


class Report(FPDF):
    # Effective page width, or just epw
    epw=0
    col_width=0

    def header(self):
        """
        Header on each page
         Must contain Lot# , product and start and end time of the batch
        """
        # Logo
        self.image('uis/resources/hikma.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Helvetica', 'B', 20)
        # Move to the right
        self.cell(165)
        # Title
        self.cell(30, 10, 'Report', 0, 0, 'C')
        # Line break
        self.ln(20)

    def footer(self):
        """
        Footer on each page
        """
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def insert_table(self, data):

        # Remember to always put one of these at least once.
        self.set_font('Helvetica', 'B', 11.0)
        # Effective page width, or just epw
        self.epw = self.w - 2 * self.l_margin
        # Set column width to 1/3 of effective page width to distribute content
        # evenly across table and page
        self.col_width = self.epw / 3
        # Table topics
        self.set_draw_color(255, 255, 255)
        self.set_fill_color(200, 220, 255)
        self.cell(self.col_width, 2*self.font_size, "Timestamp", border=1, ln=0, align='C', fill=1)
        self.cell(self.col_width, 2*self.font_size, "Tray", border=1, ln=0, align='C', fill=1)
        self.cell(self.col_width, 2*self.font_size, "Vials", border=1, ln=0, align='C', fill=1)
        self.ln(2*self.font_size)
        # Data
        self.set_font('Helvetica', '', 10.0)
        self.set_draw_color(255, 255, 255)
        self.set_fill_color(245, 250, 250)
        # Here we add more padding by passing 2*th as height
        for row in data:
            for datum in row:
                # Enter data in colums
                self.cell(self.col_width, 2 * self.font_size, str(datum), border=1, align='C', fill=1)
            self.ln(2 * self.font_size)

    def fill_report(self, product_name, lot_number, data):
        self.alias_nb_pages()
        self.add_page()
        # Effective page width, or just epw
        self.epw = self.w - 2 * self.l_margin
        self.set_document_title(product_name=product_name, lot=lot_number)
        self.insert_table(data)

    def set_document_title(self, product_name, lot):
        self.set_font('Helvetica', 'B', 14.0)
        w0 = self.get_string_width('Product: ') + 3
        w1 = self.get_string_width(product_name) + 12
        w2 = self.get_string_width('Lot#: ') + 3
        w3 = self.get_string_width(lot)
        # write to pdf
        self.set_font('Helvetica', 'B', 14.0)
        self.cell(w0, 0.0, 'Product: ', align='')
        self.set_font('Helvetica', '', 14.0)
        self.cell(w1, 0.0, product_name, align='')
        self.set_font('Helvetica', 'B', 14.0)
        self.cell(w2, 0.0, 'Lot#: ', align='')
        self.set_font('Helvetica', '', 14.0)
        self.cell(w3, 0.0, lot, align='')
        self.set_font('Helvetica', '', 12.0)
        self.ln(12)


if __name__ == "__main__":

    pdf = Report()
    data = data = [ ['Jules', 'Smith', 35],
                    ['Mary', 'Ramos', 45]]

    pdf.fill_report("teste", "teste2", data=data)
    filepath = "/Users/tiagocunha/Documents/PycharmProjects/VialCounter/"
    pdf.output(filepath + "first_report.pdf")

