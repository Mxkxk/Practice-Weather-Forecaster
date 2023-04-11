import sys
import PySide6.QtWidgets as QW
import PySide6.QtCore as QC

import options as CustomOptions
from widgets import About, History, Weather


class MainWindow(QW.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(CustomOptions.MAIN_NAME)
        
        self.button = QW.QPushButton("Click me!")
        self.button.setFlat(True)
        self.text = QW.QLabel("Hello World", alignment = QC.Qt.AlignCenter)


        #set main layout for app
        self.layout = QW.QVBoxLayout(self)

        #set main layout for info output
        self.info_layout = QW.QStackedLayout()
        self.layout.addLayout(self.info_layout)

        self.weather = Weather()
        self.history = History()
        self.about = About()
        
        self.info_layout.addWidget(self.weather)
        self.info_layout.addWidget(self.history)
        self.info_layout.addWidget(self.about)
        
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
        self.menuBar = QW.QHBoxLayout()
        self.menus = {}

        for menu in CustomOptions.MENU:
            self.menus[menu] = QW.QPushButton(menu)
            self.menuBar.addWidget(self.__menus[menu])
        
        self.menus[CustomOptions.MENU[0]].clicked.connect(self.weather_menu)
        self.menus[CustomOptions.MENU[1]].clicked.connect(self.history_menu)
        self.menus[CustomOptions.MENU[2]].clicked.connect(self.about_menu)
        self.menus[CustomOptions.MENU[3]].clicked.connect(self.close_menu)
        
        self.layout.addLayout(self.menuBar)

    @QC.Slot()
    def weather_menu(self):
        self.info_layout.setCurrentIndex(0)
        self.setWindowTitle(CustomOptions.MAIN_NAME + ": " + CustomOptions.WEATHER_NAME)

    @QC.Slot()
    def history_menu(self):
        self.info_layout.setCurrentIndex(1)
        self.setWindowTitle(CustomOptions.MAIN_NAME + ": " + CustomOptions.HISTORY_NAME)

    @QC.Slot()
    def about_menu(self):
        self.info_layout.setCurrentIndex(2)
        self.setWindowTitle(CustomOptions.MAIN_NAME + ": " + CustomOptions.ABOUT_NAME)

    @QC.Slot()
    def close_menu(self):
        QW.QApplication.exit()

if __name__ == "__main__":
    app = QW.QApplication()

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())