import sys
import PySide6.QtWidgets as QW
import PySide6.QtGui as QG
import PySide6.QtCore as QC

import options as CustomOptions


class About(QW.QWidget):
    def __init__(self):
        super().__init__()        
        self.setStyle()

        self.layout = QW.QVBoxLayout()
        
        self.text_about = QW.QTextEdit(CustomOptions.MAIN_NAME)
        self.text_about.setObjectName('text_about')
        self.text_about.setEnabled(False)
        self.text_about.setAlignment(QC.Qt.AlignmentFlag.AlignRight)
        about_add_text = lambda s: self.text_about.setText(self.text_about.toPlainText()+s)
        about_add_text("\n\tQT:"+str(QC.qVersion()))
        

        self.layout.addWidget(self.text_about)

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
        self.form.setWindowTitle(CustomOptions.INDEX_LABEL)
        self.form.setMinimumHeight(200)
        self.form.setWindowIcon(QG.QPixmap(CustomOptions.ICON))

        self.form_layout = QW.QVBoxLayout()

        self.edit_index = QW.QLineEdit()
        self.edit_index.setValidator(QG.QIntValidator(0, CustomOptions.INDEX_MAX_VALUE))
        self.edit_index.setPlaceholderText(CustomOptions.INDEX_LABEL)
        self.edit_index.setAlignment(QC.Qt.AlignmentFlag.AlignCenter)

        self.box_index = QW.QGroupBox(title=CustomOptions.INDEX_RADIO_TITLE)        
        self.radio_day = QW.QRadioButton(text=CustomOptions.INDEX_RADIO_DAY)
        self.radio_day.setChecked(True)
        self.radio_week = QW.QRadioButton(text=CustomOptions.INDEX_RADIO_WEEK)

        box_index_layout = QW.QVBoxLayout(self.box_index)
        box_index_layout.addStretch(0)
        box_index_layout.addWidget(self.radio_day)
        box_index_layout.addWidget(self.radio_week)

        self.button_index = QW.QPushButton(text=CustomOptions.INDEX_PUSHBUTTON)
        

        self.form_layout.addWidget(self.edit_index)
        self.form_layout.addWidget(self.box_index)
        self.form_layout.addWidget(self.button_index)

        self.form.setLayout(self.form_layout)
        self.form.setVisible(True)
        self.form.setStyleSheet(self.styleSheet())

    


    def setStyle(self):
        theme_file = None
        try:
            theme_file = open(CustomOptions.MAIN_THEME)
        except(Exception()):
            print("Failed to open theme file...")
        finally:
            self.setStyleSheet(theme_file.read())
            theme_file.close()

class Message():
    def __init__(self, title, text, styleSheet = None):
        box = QW.QMessageBox()
        box.setWindowTitle(title)
        box.setText(text)
        box.setWindowIcon(QG.QPixmap(CustomOptions.ICON))
        box.setStyleSheet(styleSheet)
        box.resize(QC.QSize(300, 150))
        box.exec()