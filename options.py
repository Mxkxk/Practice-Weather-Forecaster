#File with custom values
MAIN_NAME = "Weather Forecaster"
MAIN_THEME = "theme.css"
ABOUT_NAME = "Про програму"
HISTORY_NAME = "Історія"
WEATHER_NAME = "Прогноз погоди"
MENU = ["Погода", "Історія", "Про програму", "Вийти"]
#Weather data
WEATHER_API_KEY = "5efcc8b5b685d99dbcf01585a90702ef"
WEATHER_API = "https://api.openweathermap.org/data/2.5/weather?lat=$lat&lon=$lon&appid=$key&units=metric"
SINOPTIK = "//ua.sinoptik.ua/погода-"
ICON = "resources/icon.png"
HOUSES = "resources/houses.csv"
LOCATION = "resources/ukraine.csv"
HISTORY = "resources/history.json"
EMPTY_DATA = ['empty', {'Date': ('', '', ''), 'Conditions': '', 'Min': '', 'Max': ''}]
#Input index form
INDEX_LABEL = "Введіть дані"
INDEX_PUSHBUTTON = "Підтвердити" 
INDEX_RADIO_TITLE = "Виберіть тип даних"
INDEX_RADIO_INDEX = "Поштовий індекс"
INDEX_RADIO_CITY = "Назва міста"
INDEX_RADIO_LOC = "Координати"
INDEX_MAX_VALUE = 99999
#Message codes
MESSAGE_ERROR = "Виникла помилка"
#Transliter
DICTIONARY = {"Київ":"Kyiv", "Київська":"Kyiv", "Житомирська":"Zhytomyr", "Чернігівська":"Chernihiv", "Черкаська":"Cherkasy", "Вінницька":"Vinnytsia",
 "Кіровоградська":"Kirovohrad", "Хмельницька":"Khmelnytskyi", "Рівненська":"Rivne", "Полтавська":"Poltava", "Сумська":"Sumy",
 "Волинська":"Volyn", "Тернопільська":"Ternopil", "Дніпропетровська":"Dnipropetrovsk", "Миколаївська":"Mykolaiv",
 "Чернівецька":"Chernivtsi", "Харківська":"Kharkiv", "Одеська":"Odesa", "Запорізька":"Zaporizhia", "Херсонська":"Kherson",
 "Івано-Франківська":"Ivano-Frankivsk", "Львівська":"Lviv", "Донецька":"Donetsk", "Закарпатська":"Zakarpattia", "Луганська":"Luhansk"}
#
ABOUT_TEXT = "Дана програма дозволяє користувачу отримати прогноз погоди на тиждень та мати доступ до історії пошуку, ґрунтуючись на поштовому індексі"
ABOUT_OSM = "OpenStreetMap data of 2022-11-25"