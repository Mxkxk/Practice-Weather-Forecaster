import sys
import PySide6.QtWidgets as QW
from PySide6.QtGui import QScreen
import PySide6.QtCore as QC

import options as CustomOptions

class MainWindow(QW.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(CustomOptions.MAIN_NAME)

        self.button = QW.QPushButton("Click me!")
        self.button.setFlat(True)
        self.text = QW.QLabel("Hello World", alignment = QC.Qt.AlignCenter)

        layout = QW.QVBoxLayout(self)
        layout.addWidget(self.text)
        layout.addWidget(self.button)

        self.setLayout(layout)
        
        self.setStyle()

        
    def setStyle(self):
        theme_file = None
        try:
            theme_file = open(CustomOptions.MAIN_THEME)
        except(Exception()):
            print("Failed to open theme file...")
        finally:
            self.setStyleSheet(theme_file.read())
            theme_file.close()





if __name__ == "__main__":
    app = QW.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())