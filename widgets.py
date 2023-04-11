import sys
import PySide6.QtWidgets as QW
import PySide6.QtCore as QC

import pandas as pd

import options as CustomOptions


class About(QW.QWidget):
    def __init__(self):
        super().__init__()        
        self.setStyle()

        self.layout = QW.QVBoxLayout()
        
        self.name_label = QW.QLabel(CustomOptions.MAIN_NAME)
        self.name_label.setAlignment(QC.Qt.AlignmentFlag.AlignTop and QC.Qt.AlignmentFlag.AlignHCenter)
        self.name_label.setObjectName('name_label')

        self.qt_label = QW.QLabel(str(QC.qVersion()))

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.qt_label)

        self.setLayout(self.layout)

    def setStyle(self):
        theme_file = None
        try:
            theme_file = open(CustomOptions.MAIN_THEME)
        except(Exception()):
            print("Failed to open theme file...")
        finally:
            self.setStyleSheet(theme_file.read())
            theme_file.close()

class History(QW.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(CustomOptions.MAIN_NAME + ": " + CustomOptions.HISTORY_NAME)
        self.setStyle()

        self.layout = QW.QVBoxLayout()
        
        self.list = QW.QListView()
        self.layout.addWidget(self.list)

        self.setLayout(self.layout)


    def setStyle(self):
        theme_file = None
        try:
            theme_file = open(CustomOptions.MAIN_THEME)
        except(Exception()):
            print("Failed to open theme file...")
        finally:
            self.setStyleSheet(theme_file.read())
            theme_file.close()

class Weather(QW.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(CustomOptions.MAIN_NAME + ": " + CustomOptions.ABOUT_NAME)
        self.setStyle()

        
        
    def inputForm(self):

        self.form = QW.QWidget()
        self.form_layout = 

    def setStyle(self):
        theme_file = None
        try:
            theme_file = open(CustomOptions.MAIN_THEME)
        except(Exception()):
            print("Failed to open theme file...")
        finally:
            self.setStyleSheet(theme_file.read())
            theme_file.close()

