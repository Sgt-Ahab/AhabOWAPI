# Weather API through OpenWeatherMap

# This is Base on GitHub, it takes a City, State, and Country code
# Then sends to the API
# ISO 3166 - 1 Codes Link (In English): https://www.iso.org/obp/ui/#iso:pub:PUB500001:en
# When inputting into LineEdit, it went City Name, State/ISO code ("GB = Great Britain, GB-BIR = Birmingham"; Just BIR)
# Great Britain Birmingham Example - Birmingham, BIR, GB -> Displays Results in °F/°C

# Original idea was from BroCode's YouTube Video Python Full Course, I added my own pieces.
# BroCode's YouTube - https://www.youtube.com/@BroCodez

# REMEMBER: NEVER Commit your API Keys! Use .envs if need be!

import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt


class WeatherAPI(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City, State, Country Name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather = QPushButton("Get Weather", self)
        self.temperature = QLabel(self)
        self.feelTemp = QLabel(self)
        self.emoji = QLabel(self)
        self.weather = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather API ☀ 🌥 🌦 🌩 🌤")
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather)
        vbox.addWidget(self.temperature)
        vbox.addWidget(self.feelTemp)
        vbox.addWidget(self.emoji)
        vbox.addWidget(self.weather)
        self.city_input.setPlaceholderText("Enter City, State, Country Name")
        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature.setAlignment(Qt.AlignCenter)
        self.emoji.setAlignment(Qt.AlignCenter)
        self.weather.setAlignment(Qt.AlignCenter)
        self.feelTemp.setAlignment(Qt.AlignCenter)
        self.city_input.setObjectName("city_input")
        self.city_label.setObjectName("city_label")
        self.get_weather.setObjectName("get_weather")
        self.emoji.setObjectName("emoji")
        self.weather.setObjectName("weather")
        self.temperature.setObjectName("temperature")
        self.feelTemp.setObjectName("feelTemp")
        self.setStyleSheet("""
            QLabel,QPushButton{
                font-family: Times New Roman;
            }
            QLabel#city_label{
                font-size: 32px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 28px;
            }
            QPushButton#get_weather{
                font-size: 30px;
                font-weight: bold;
                background-color: hsv(49, 63%, 66%)
            }
            QPushButton#get_weather:hover{
                background-color: hsv(49, 63%, 86%)
            }
            QLabel#temperature{
                font-size: 75px;
            }
            QLabel#emoji{
                font-size: 80px;
                font-family: Segoe UI emoji;
            }
            QLabel#weather{
                font-size: 50px;
            }
            QLabel#feelTemp{
                font-size: 50px;
            }
        """)
        self.get_weather.clicked.connect(self.getWeather)

    def getWeather(self):
        # Copy - Paste API Key here:
        API_KEY = "REPLACE_WITH_YOUR_ACTUAL_KEY" # <- Change this!
        # DO NOT COMMIT YOUR API KEY
        lineofText = self.city_input.text()
        slices = [l.strip() for l in lineofText.split(",")]
        if len(slices) != 3:
            self.display_err("API call misformatted:\nCity, State Code, Country Code")
        else:
            city = slices[0]
            state = slices[1]
            country = slices[2]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&appid={API_KEY}"
        

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_err:
            match response.status_code:
                case 400:
                    self.display_err("Bad request:\nPlease check your input")
                case 401:
                    self.display_err("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_err("Forbidden:\nAccess Denied")
                case 404:
                    self.display_err("Not Found:\nCity not found")
                case 500:
                    self.display_err("Internal Server Error:\nTry again later")
                case 502:
                    self.display_err("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_err("Service unavailable:\nServer is down")
                case 504:
                    self.display_err("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_err(f"HTTP error occured:\n Status Code - {http_err}")

        except requests.exceptions.ConnectionError:
            self.display_err("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_err("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_err("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_err:
            self.display_err(f"Request Error:\n{req_err}")

    def display_err(self, message):
        self.temperature.setStyleSheet("font-size: 30px;")
        self.feelTemp.clear()
        self.temperature.setText(message)
        self.emoji.clear()
        self.weather.clear()

    def display_weather(self, data):
        self.temperature.setStyleSheet("font-size: 75px;")
        temp_k1 = data["main"]["temp"]
        temp_k2 = data["main"]["feels_like"]
        # It defaults to Fahrenheit, however here is Celsius, uncomment this, and setText comments
        #temp_c1 = temp_k1 - 273.15
        #temp_c2 = temp_k2 - 273.15
        temp_t1 = (temp_k1 * 9 / 5) - 459.67
        temp_t2 = (temp_k2 * 9 / 5) - 459.67
        weather_id = data["weather"][0]["id"]
        weather_descrip = data["weather"][0]["description"]

        # Fahrenheit Temperature Labels
        self.temperature.setText(f"A - {temp_t1:.0f}°F")
        self.feelTemp.setText(f"F - {temp_t2:.0f}°F")
        # Celsius Temperature Labels
        #self.temperature.setText(f"A - {temp_c1:.0f}°C")
        #self.feelTemp.setText(f"F - {temp_c2:.0f}°C")
        self.emoji.setText(self.get_weather_emoji(weather_id))
        self.weather.setText(weather_descrip)

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "🌩"
        elif 300 <= weather_id <= 321:
            return "🌦"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "🌨"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id <= 804:
            return "☁"
        else:
            return ""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather = WeatherAPI()
    weather.show()
    sys.exit(app.exec_())