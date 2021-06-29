from PyQt5.QtWidgets import QPushButton, QLineEdit, QApplication, QFormLayout, QWidget, QTextEdit, QMessageBox, QSpinBox
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot

from reportlab.pdfgen.canvas import Canvas
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.barcode.qr import QrCodeWidget 
from reportlab.graphics import renderPDF
import os

import textwrap
from datetime import datetime

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from sign import *


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """
    error = pyqtSignal(str)
    file_saved_as = pyqtSignal(str)


class Generator(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handle worker thread setup, signals
    and wrap-up.

    :param data: The data to add to the PDF for generating.
    """

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            p = Canvas(self.data['fileName'])
            p.setPageSize((400, 400))

            content= self.data['content'].replace('\n', ' ')
            #content sau nay phai ghep voi chu ky RSA
            user=User(self.data['customer'])
            qr_data = content+'#'+self.data['customer']+'#'+user.sign(content)

            # Generate qr code
            qrw = QrCodeWidget(qr_data) 

            d = Drawing(10,10) 
            d.add(qrw)

            renderPDF.draw(d, p, 0, 0)
            p.showPage()
            p.save()

            # mo 1 cai pdf co san ra
            template = PdfReader(self.data['fileName'], decompress=False).pages[0]
            template_obj = pagexobj(template)

            canvas = Canvas(self.data['fileName'])

            xobj_name = makerl(canvas, template_obj)
            canvas.doForm(xobj_name)

            # Date: Todays date
            today = datetime.today()
            canvas.drawString(500, 15, today.strftime('%F'))


            # Customer
            canvas.drawString(20, 800, self.data['customer'])


            ystart = 750

            # Program Language

            comments = self.data['content'].replace('\n', ' ')
            if comments:
                lines = textwrap.wrap(comments, width=65) # 45
                first_line = lines[0]
                remainder = ' '.join(lines[1:])

                lines = textwrap.wrap(remainder, 75) # 55
                lines = lines[:4]  # max lines, not including the first.

                canvas.drawString(155, ystart, first_line)
                for n, l in enumerate(lines, 1):
                    canvas.drawString(80, ystart - (n*28), l)

            canvas.save()

        except Exception as e:
            self.signals.error.emit(str(e))
            return

        self.signals.file_saved_as.emit(self.data['fileName'])


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.threadpool = QThreadPool()

        self.name = QLineEdit()
        self.fileName = QLineEdit()
        self.customer = QLineEdit()
        self.comments = QTextEdit()

        self.generate_btn = QPushButton("Generate PDF")
        self.generate_btn.pressed.connect(self.generate)

        layout = QFormLayout()
        layout.addRow("Customer", self.customer)
        layout.addRow("Content", self.comments)
        layout.addRow("File Name", self.fileName)
        layout.addRow(self.generate_btn)

        self.setLayout(layout)

    def generate(self):
        self.generate_btn.setDisabled(True)
        data = {
            'fileName': self.fileName.text(),
            'customer': self.customer.text(),
            'content': self.comments.toPlainText()
        }
        g = Generator(data)
        g.signals.file_saved_as.connect(self.generated)
        g.signals.error.connect(print)  # Print errors to console.
        self.threadpool.start(g)

    def generated(self, outfile):
        self.generate_btn.setDisabled(False)
        try:
            os.startfile(outfile)
        except Exception:
            # If startfile not available, show dialog.
            QMessageBox.information(self, "Finished", "PDF has been generated")


app = QApplication([])
w = Window()
w.show()
app.exec_()