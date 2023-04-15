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
        self.history.delete_button.clicked.connect(self.history_delete)

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

    def getWeather(self, type):
        if type == "location":
            self.getGeocode()
        else:
            self.data["City"] = ['', self.data["City"]]
        for i, city in enumerate(self.data["City"]):
            url = "https:" + pr.quote(CustomOptions.SINOPTIK + city.lower())
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
                self.data["City"] = city
                return True
                    
        Message(CustomOptions.MESSAGE_ERROR, "Місто не знайдено", self.styleSheet())
        return False

    def getGeocode(self):
        #Computing lat and lon of city
        osm_df = pd.read_csv(CustomOptions.LOCATION, sep='\t')
        #osm_df = osm_df[(osm_df["state"] == self.data["Oblast"]) | osm_df["state"].isnull()]
        if self.data["Location"]["lat"] < CustomOptions.GEO_DATA["north"] and self.data["Location"]["lat"] > CustomOptions.GEO_DATA["south"] and self.data["Location"]["lon"] < CustomOptions.GEO_DATA["east"] and self.data["Location"]["lon"] > CustomOptions.GEO_DATA["west"]:      
            try:
                osm_df = osm_df.query(f'lat >= {self.data["Location"]["lat"]-CustomOptions.GEO_APPROX} and lat <= {self.data["Location"]["lat"]+CustomOptions.GEO_APPROX}')
                osm_df = osm_df.query(f'lon >= {self.data["Location"]["lon"]-CustomOptions.GEO_APPROX} and lon <= {self.data["Location"]["lon"]+CustomOptions.GEO_APPROX}')
                lat, lon = self.data["Location"]["lat"], self.data["Location"]["lon"]
                locations = [(frame.lon-lon)**2+(frame.lat-lat)**2 for frame in osm_df.itertuples()]                
                min_i = locations.index(min(locations))
                city_list = re.findall(r"([А-ЩЮЯҐЄЇІ]*[а-щюяяґєїьі']+-)*([А-ЩЮЯҐЄЇІ][а-щюяяґєїьі'-]+,)", ",".join([str(v) for v in osm_df.values[min_i]]+[""]))
                city_list = [("".join(city)).replace(',', '') for city in city_list]
                print(city_list)
                self.data["City"] = city_list
            except:
                Message(CustomOptions.MESSAGE_ERROR, "Вашу локацію не знайдено в межах України(поблизу вказаних кординат відсутні населені пунтки)", self.styleSheet())
        else: 
            Message(CustomOptions.MESSAGE_ERROR, "Ваша локація знаходиться за межами України)", self.styleSheet())

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
            Message(CustomOptions.MESSAGE_ERROR, "Ви нічого не вибрали(", self.styleSheet())
        if self.history.list.currentRow() >= 0:
            self.info_layout.setCurrentIndex(0)
            current_row = lambda: len(self.history.load_data) - self.history.list.currentRow() - 1
            self.weather.generateLayout(self.history.load_data[current_row()]["Weather"])
            date = ".".join(self.history.load_data[current_row()]["Weather"][0].split('-')[::-1])
            self.setWindowTitle(f'{CustomOptions.MAIN_NAME} : {CustomOptions.WEATHER_NAME} - {self.history.load_data[current_row()]["City"]} ({date})')
        
    @QC.Slot()
    def history_delete(self):
        if self.history.list.currentRow() == -1 and self.history.list.count() > 0:
            Message(CustomOptions.MESSAGE_ERROR, "Ви нічого не вибрали(", self.styleSheet())
        if self.history.list.currentRow() >= 0:
            current_row = lambda: len(self.history.load_data) - self.history.list.currentRow() - 1
            del self.history.load_data[current_row()]
            self.history.saveHistory()
            self.history.readHistory()
            self.history.generaleList()

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
                self.data["City"] = '-'.join(self.data["City"]["City"].values[0].split(' ')[1:])
                if self.getWeather(self.weather.radio_type):
                    del self.weather.form
            else:
                self.data["Index"] = ""
                Message(CustomOptions.MESSAGE_ERROR, "Індекс не знайдено", self.styleSheet())

        #Seeking city
        if self.weather.radio_type == "city":
            self.data["City"] = '-'.join(self.weather.edit_index.text().split(' '))
            if len(self.data["City"]) > 0:
                if self.getWeather(self.weather.radio_type):
                    del self.weather.form
                else:
                    self.data["City"] = ""
            
        #Seeking location
        if self.weather.radio_type == "location":
            self.data["Location"] = self.weather.edit_index.text().replace(" ", "").split(",")
            try:
                if len(self.data["Location"]) == 2:
                    self.data["Location"] = {"lat":float(self.data["Location"][0]), "lon":float(self.data["Location"][1])}
                    print(self.data["Location"])
                    if self.getWeather(self.weather.radio_type):
                        del self.weather.form
                else: raise
            except:
                self.data["Location"] = ""
                Message(CustomOptions.MESSAGE_ERROR, "Введіть 2 значення через кому в десятковому форматі, використовуючи крапку в якості роздільника", self.styleSheet())

        if len(self.data["Weather"]) > 0:
            self.history.saveHistory(self.data)
            self.history.readHistory()
            self.history.generaleList()
            self.weather.generateLayout(self.data["Weather"])
            self.setWindowTitle(CustomOptions.MAIN_NAME + ": " + CustomOptions.WEATHER_NAME + " - " + self.data["City"])

        print(self.data)



if __name__ == "__main__":
    app = QW.QApplication()

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())