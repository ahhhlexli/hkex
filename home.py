import kivy
#kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget 
from kivy.properties import ObjectProperty  
from kivy.core.window import Window


from selenium import webdriver
from stocksearch import stock_input

Window.size = (600, 300)
#Window.clearcolor = (1, 0, 1, 1)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument("--log-level=3")

DRIVER_PATH = 'C:/Program Files (x86)/chromedriver.exe'

query = None
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
driver.get('http://www.etnet.com.hk/www/eng/stocks/realtime/')


class StockCode(Widget):

    number = ObjectProperty(None)
    info = ObjectProperty(None)

    def btn(self):
        print("Stock Code:", self.number.text)
        name, price, change, call_time = stock_input(self.number.text, driver)
        self.number.text = ""
        self.info.text = f'Stock: {name} \nPrice: {price} \nChange: {change} \nTime: {call_time}'

class HomeApp(App):

    def build(self):
        self.title = 'Stock Price Checker'
        return StockCode()


if __name__ == '__main__':
    HomeApp().run()