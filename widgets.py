import sys
import PySide6.QtWidgets as QW
import PySide6.QtGui as QG
import PySide6.QtCore as QC
import json
import options as CustomOptions


class About(QW.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyle()

        self.layout = QW.QVBoxLayout()
        
        self.text_about = QW.QTextEdit()
        self.text_about.setObjectName('text_about')
        self.text_about.setReadOnly(True)
        #self.text_about.setAlignment(QC.Qt.AlignmentFlag.AlignHCenter)
        #print(f"About alignment {self.text_about.alignment()}")
        about_text_doc = QG.QTextDocument()
        about_text_doc.setDefaultStyleSheet(self.styleSheet())
        about_text_add = lambda s: about_text_doc.setHtml(about_text_doc.toHtml()+s)
        about_text_add(f"<h1>{CustomOptions.MAIN_NAME}</h1>")
        about_text_add(f"<p>{CustomOptions.ABOUT_TEXT}</p>")
        about_text_add(f"<p>Версія QT: {str(QC.qVersion())}</p>")
        about_text_add(f"<p>Дані локацій: {CustomOptions.ABOUT_OSM}</p>")
        about_text_add(f"<p>Погодні дані: {CustomOptions.ABOUT_WEATHER}</p>")
        about_text_add(f"<p>Автор: {CustomOptions.ABOUT_AUTHOR_NAME}</p>")
        about_text_add(f"<p>Контакти: {CustomOptions.ABOUT_AUTHOR_MAIL}</p>")
        self.text_about.setDocument(about_text_doc)
        print(self.text_about.toHtml())

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
        
        self.choose_button = QW.QPushButton(CustomOptions.HISTORY_CHOOSE)
        self.delete_button = QW.QPushButton(CustomOptions.HISTORY_DELETE)

        self.list = QW.QListWidget()

        self.layout.addWidget(self.choose_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.list)
        

        '''
        Data is stored in list of dictionaries
        Index: str of index digits
        City: str of city name
        Location: str of float latitude and longitude        
        Weather: list of weather and date:
            [0]: date of weather data query
            [1::]: dictionaries of weather data:
                Date: list of day date (YYYY, MM, DD)
                Conditions: str of weather conditions
                Min: str of minimal temperature 
                Max: str of maximal temperature        
        '''
        self.load_data = []
        self.setLayout(self.layout)

        self.readHistory()
        self.generaleList()

    def read_file(self, name):
            try:
                with open(name, 'r') as f:
                    return f.read()
            except:
                return None
            
    def errase_file(self, name):
        try:
            with open(name, 'w') as f:
                f.write('')
        except: pass
    
    def rewrite_file(self, name, text):
        try:
            with open(name, 'w') as f:
                f.write(text)
        except: pass

    def write_file(self, name, text):
        with open(name, 'a+') as f:
            f.write(text)

    def saveHistory(self, weather_data = None): 
        if self.read_file(CustomOptions.HISTORY) is None:
            self.write_file(CustomOptions.HISTORY, '[]')
        data = json.loads(self.read_file(CustomOptions.HISTORY))
        if weather_data is not None:
            data.append(weather_data)
        else:
            data = self.load_data
        self.rewrite_file(CustomOptions.HISTORY, json.dumps(data))

    def readHistory(self):  
        if self.read_file(CustomOptions.HISTORY) is None:
            self.write_file(CustomOptions.HISTORY, '[]')
        self.load_data = json.loads(self.read_file(CustomOptions.HISTORY))
        #print(self.load_data)

    def generaleList(self):
        if self.list.count() > 0:
            self.list.clear()
        for data in self.load_data[::-1]:
            date = ".".join(data["Weather"][0].split('-')[::-1])
            self.list.addItem(f'{data["City"]}:{date}')

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
        self.setWindowTitle(CustomOptions.MAIN_NAME + ": " + CustomOptions.WEATHER_NAME)
        self.setStyle()
        self.radio_type = ""
        self.weather_widgets = []
        self.layout = QW.QStackedLayout()
        self.setLayout(self.layout)

    def inputForm(self):

        self.form = QW.QWidget()
        self.form.setWindowTitle(CustomOptions.INDEX_LABEL)
        self.form.setMinimumHeight(250)
        self.form.setWindowIcon(QG.QPixmap(CustomOptions.ICON))

        self.form_layout = QW.QVBoxLayout()

        self.edit_index = QW.QLineEdit()
        self.edit_index.setPlaceholderText(CustomOptions.INDEX_LABEL)
        self.edit_index.setAlignment(QC.Qt.AlignmentFlag.AlignCenter)

        self.box_index = QW.QGroupBox(title=CustomOptions.INDEX_RADIO_TITLE)
        self.radio = {}
        self.radio["index"] = QW.QRadioButton(text=CustomOptions.INDEX_RADIO_INDEX)
        self.radio["index"].setChecked(True)
        self.radio["city"] = QW.QRadioButton(text=CustomOptions.INDEX_RADIO_CITY)
        self.radio["location"] = QW.QRadioButton(text=CustomOptions.INDEX_RADIO_LOC)

        box_index_layout = QW.QVBoxLayout(self.box_index)
        box_index_layout.setAlignment(QC.Qt.AlignmentFlag.AlignBottom)
        box_index_layout.addSpacerItem(QW.QSpacerItem(1, 50))
        for k in self.radio.keys():
            self.radio[k].clicked.connect(self.check_radios)
            box_index_layout.addWidget(self.radio[k])
        
        self.check_radios()

        self.button_index = QW.QPushButton(text=CustomOptions.INDEX_PUSHBUTTON)
        
        self.form_layout.addWidget(self.edit_index)
        self.form_layout.addWidget(self.box_index)
        self.form_layout.addWidget(self.button_index)

        self.form.setLayout(self.form_layout)
        self.form.setVisible(True)
        self.form.setStyleSheet(self.styleSheet())

    def generateLayout(self, data):
        self.weather_widgets_layout = QW.QHBoxLayout()

        if data[0] == "empty":
            for i in range(7):
                self.weather_widgets_layout.addWidget(self.getWeatherWidget(data[1]))
        else:
            for d in data[1::]:
                self.weather_widgets_layout.addWidget(self.getWeatherWidget(d))
            w = QW.QWidget()
            w.setLayout(self.weather_widgets_layout)
            self.layout.addWidget(w)
            self.layout.setCurrentIndex(self.layout.count()-1)
           
            

    def getWeatherWidget(self, data):        
        widget = QW.QWidget()
        layout = QW.QVBoxLayout()

        labels = []
        labels.append(QW.QLabel(text='.'.join(data["Date"][::-1])))
        labels.append(QW.QLabel(text=data["Conditions"]))
        labels.append(QW.QLabel(text=data["Max"]))
        labels.append(QW.QLabel(text=data["Min"]))
        
        #QW.QLabel().setObjectName('forecast')

        for l in labels:
            l.setAlignment(QC.Qt.AlignmentFlag.AlignCenter)
            l.setWordWrap(True)
            l.setObjectName('forecast')
            layout.addWidget(l)

        widget.setLayout(layout)
        return widget

    @QC.Slot()
    def check_radios(self):
        for k in self.radio.keys():
            if self.radio[k].isChecked():
                self.radio_type = k
                break

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
        box.setObjectName("message")
        box.setStyleSheet(styleSheet)
        box.resize(QC.QSize(300, 150))
        box.exec()