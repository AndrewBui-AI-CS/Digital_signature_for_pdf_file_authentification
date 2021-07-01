from PyQt5.QtWidgets import QApplication
from genPDF import Window



if __name__ == "__main__":
    app = QApplication([])
    w = Window()
    w.show()
    app.exec_()