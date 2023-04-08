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

        self.layout = QW.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        
        self.setLayout(self.layout)
        
        self.setMenu()
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


    def setMenu(self):
        self.__menuBar = QW.QHBoxLayout()

        self.__menus = {}

        for menu in CustomOptions.MENU:
            self.__menus[menu] = QW.QPushButton(menu)
            self.__menuBar.addWidget(self.__menus[menu])
            
        self.layout.addLayout(self.__menuBar)

        #for k in self.__menus.keys():
        #    print(f"{k} : {self.__menus[k]}")

if __name__ == "__main__":
    app = QW.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())