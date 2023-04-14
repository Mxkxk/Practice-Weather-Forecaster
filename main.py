import sys
import PySide6.QtWidgets as QW
import PySide6.QtGui as QG
import PySide6.QtCore as QC
import requests
import urllib.parse as pr
import pandas as pd
import json as js
import re

from datetime import date
import options as CustomOptions
from widgets import About, History, Weather, Message


class MainWindow(QW.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(CustomOptions.MAIN_NAME)
        self.setWindowIcon(QG.QPixmap(CustomOptions.ICON))
        #set main layout for app

        self.generateLayout()      
        self.setLayout(self.layout)
        
        self.setMenu()
        self.setStyle()

        self.data = {}
        self.data["Index"] = ""
        self.data["City"] = ""
        self.data["Location"] = ""
        self.data["Weather"] = []
        
    def setStyle(self):
        theme_file = None
        try:
            theme_file = open(CustomOptions.MAIN_THEME)
        except(Exception()):
            print("Failed to open theme file...")
        finally:
            self.setStyleSheet(theme_file.read())
            theme_file.close()

    def generateLayout(self):
        self.layout = QW.QVBoxLayout(self)

        #set main layout for info output
        self.info_layout = QW.QStackedLayout()
        self.layout.addLayout(self.info_layout)

        self.weather = Weather()
        self.weather.generateLayout(CustomOptions.EMPTY_DATA)

        self.history = History()
        self.history.choose_button.clicked.connect(self.history_load)

        self.about = About()
        
        self.info_layout.addWidget(self.weather)
        self.info_layout.addWidget(self.history)
        self.info_layout.addWidget(self.about)

    def setMenu(self):
        self.menuBar = QW.QHBoxLayout()
        self.menus = {}

        for menu in CustomOptions.MENU:
            self.menus[menu] = QW.QPushButton(menu)
            self.menuBar.addWidget(self.menus[menu])
        
        self.menus[CustomOptions.MENU[0]].clicked.connect(self.weather_menu)
        self.menus[CustomOptions.MENU[1]].clicked.connect(self.history_menu)
        self.menus[CustomOptions.MENU[2]].clicked.connect(self.about_menu)
        self.menus[CustomOptions.MENU[3]].clicked.connect(self.close_menu)
        
        self.layout.addLayout(self.menuBar)        

    def getGeocode(self):
        #Computing lat and lon of city
        osm_df = pd.read_csv(CustomOptions.LOCATION, sep='\t')
        osm_df = osm_df[(osm_df["state"] == self.data["Oblast"]) | osm_df["state"].isnull()]
        try:
            self.data["Location"] = osm_df[osm_df["name"].str.contains(self.data["City"], na=False)]
            if len(self.data["Location"]["lon"]) < 1:
                raise                       
        except:
            self.data["Location"] = osm_df[osm_df["alternative_names"].str.contains(self.data["City"], na=False)] 
        if len(self.data["Location"]["lon"]) > 0:
            lon = sum(self.data["Location"]["lon"])/len(self.data["Location"]["lon"])
            lat = sum(self.data["Location"]["lat"])/len(self.data["Location"]["lat"] )
            self.data["Location"] = {"Lat": lat, "Lon": lon}            
        else:
            Message(CustomOptions.MESSAGE_ERROR, "Місто не знайдено за індексом")

    def getWeather(self, type):
        if type == "index" or type == "city":                       
            url = "https:" + pr.quote(CustomOptions.SINOPTIK + self.data["City"].lower())
            answer = re.findall(r'id="bd[1-9]">.*?&nbsp;</div>', ''.join(requests.get(url).text.split("\r\n")))            
            if len(answer) > 1:
                self.data["Weather"] = []
                for a in answer:
                    data = {}
                    data["Date"] = re.findall(r"([0-9]{4})-([0-9]{2})-([0-9]{2})", a)[0]
                    data["Conditions"] = re.findall(r'[А-Яа-яҐЄЇІґєїі ,.]{2,}',re.findall(r'weatherIco .*? title=".*?"', a)[0])[0]
                    data["Min"] = re.findall(r'((\+|-)[0-9]+)', re.findall(r'span>.*?</span', a)[0])[0][0]
                    data["Max"] = re.findall(r'((\+|-)[0-9]+)', re.findall(r'span>.*?</span', a)[1])[0][0]
                    self.data["Weather"].append(data)

                self.data["Weather"].insert(0, str(date.today()))

            else:
                Message(CustomOptions.MESSAGE_ERROR, "Місто не знайдено", self.styleSheet())
            

        if type == "location":
            self.getGeocode()   

    @QC.Slot()
    def weather_menu(self):
        self.info_layout.setCurrentIndex(0)
        self.weather.inputForm()        
        self.weather.button_index.clicked.connect(self.check_index)
        self.setWindowTitle(CustomOptions.MAIN_NAME + ": " + CustomOptions.WEATHER_NAME)

    @QC.Slot()
    def history_menu(self):
        self.info_layout.setCurrentIndex(1)
        self.setWindowTitle(CustomOptions.MAIN_NAME + ": " + CustomOptions.HISTORY_NAME)

    @QC.Slot()
    def history_load(self):
        if self.history.list.currentRow() == -1 and self.history.list.count() > 0:
            Message(CustomOptions.MESSAGE_ERROR, "Ви нічого не вибрали(")
        if self.history.list.currentRow() >= 0:
            self.info_layout.setCurrentIndex(0)
            self.weather.generateLayout(self.history.load_data[self.history.list.currentRow()]["Weather"])
            date = ".".join(self.history.load_data[self.history.list.currentRow()]["Weather"][0].split('-')[::-1])
            self.setWindowTitle(f'{CustomOptions.MAIN_NAME} : {CustomOptions.WEATHER_NAME} - {self.history.load_data[self.history.list.currentRow()]["City"]} ({date})')
        

    @QC.Slot()
    def about_menu(self):
        self.info_layout.setCurrentIndex(2)
        self.setWindowTitle(CustomOptions.MAIN_NAME + ": " + CustomOptions.ABOUT_NAME)

    @QC.Slot()
    def close_menu(self):
        QW.QApplication.exit()  

    @QC.Slot()
    def check_index(self):
        #Checking index
        df = pd.read_csv(CustomOptions.HOUSES)
        if self.weather.radio_type == "index":
            self.data["Index"] = self.weather.edit_index.text()
            try:
                self.data["City"] = df.query(f'Index == {self.weather.edit_index.text()}')
            except:
                Message(CustomOptions.MESSAGE_ERROR, "Невірно уведені дані", self.styleSheet())
            if len(self.data["City"]) > 0:
                del self.weather.form
                self.data["Oblast_UA"] = self.data["City"]["Oblast"].values[0] + " Область"
                self.data["Oblast"] = CustomOptions.DICTIONARY[self.data["City"]["Oblast"].values[0]] + " Oblast"
                self.data["City"] = '-'.join(self.data["City"]["City"].values[0].split(' ')[1:])
                print(f'{self.data["Oblast"]} {self.data["City"].lower()}')
                self.getWeather(self.weather.radio_type)                
            else:
                Message(CustomOptions.MESSAGE_ERROR, "Індекс не знайдено", self.styleSheet())

        #Seeking city
        if self.weather.radio_type == "city":
            self.data["City"] = '-'.join(self.weather.edit_index.text().split(' '))
            del self.weather.form
            print(f'{self.data["City"].lower()}')
            if len(self.data["City"]) > 0:    
                self.getWeather(self.weather.radio_type)            
            
        try:
            self.data["Index"] = str(int(self.data["Index"]))
        except:
            self.data["Index"] = ""

        if len(self.data["Weather"]) > 0:
            self.history.saveHistory(self.data)
            self.weather.generateLayout(self.data["Weather"])
            self.setWindowTitle(CustomOptions.MAIN_NAME + ": " + CustomOptions.WEATHER_NAME + " - " + self.data["City"])

        print(self.data)
            
        


if __name__ == "__main__":
    app = QW.QApplication()

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())