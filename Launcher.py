import sys
from PyQt5.QtWidgets import QApplication
from ExtractorWindow import ExtractorWindow



if __name__ =="__main__":
    app=QApplication(sys.argv)
    extractorWindow=ExtractorWindow()
    extractorWindow.show()
    sys.exit(app.exec())