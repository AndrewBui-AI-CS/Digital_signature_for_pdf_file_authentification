from PyQt5.QtWidgets import QPushButton, QLineEdit, QApplication, QFormLayout, QWidget, QTextEdit, QMessageBox, QSpinBox
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot

from reportlab.pdfgen.canvas import Canvas
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.barcode.qr import QrCodeWidget 
from reportlab.graphics import renderPDF
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont  

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

    def gen(self):
        try:
            p = Canvas(self.data['fileName'])
            p.setPageSize((400, 400))

            content= self.data['content']
            #content sau nay phai ghep voi chu ky RSA
            #sk, pk = generateKey()
            sk=self.data['sk']
            pk=self.data['pk']
            signature_bytes = sign_msg(bytes(content, 'utf-8'), sk)
            signature = binascii.hexlify(signature_bytes).decode('utf-8')
            qr_data = content+'#'+signature
            # Generate qr code
            print(qr_data)
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
            #canvas.drawString(20, 800, self.data['customer'])


            ystart = 750

            # Program Language

            content = self.data['content'].split('\n')
            print(content)
            ystart = 780
            for line in content:
                if line:
                    lines = textwrap.wrap(line, width=88) # 45
                    for n, l in enumerate(lines, 0):
                        ystart = ystart - 28
                        canvas.drawString(75, ystart, l)
                ystart = ystart -28
            canvas.save()

        except Exception as e:
            self.signals.error.emit(str(e))
            print(str(e))
            return

        self.signals.file_saved_as.emit(self.data['fileName'])
        print('ok2')