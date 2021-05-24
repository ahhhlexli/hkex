import kivy
#kivy.require('1.0.6') # replace with your current kivy version !

# Must put config import before others to have it work
from kivy.config import Config
Config.set('graphics', 'resizable', 0)

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget 
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, ListProperty
from kivy.core.window import Window

import pandas as pd
from selenium import webdriver
from stocksearch import stock_input

Window.size = (1600, 900)

#Config.set('graphics', 'width', '600')
#Config.set('graphics', 'height', '300')
#Window.clearcolor = (1, 0, 1, 1)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument("--log-level=3")

DRIVER_PATH = 'C:/Program Files (x86)/chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
driver.get('http://www.etnet.com.hk/www/eng/stocks/realtime/')

#current_session = pd.DataFrame(columns=['Code', 'Name', 'Current Price', 'Change', 'Time'])

class StockCode(Screen):

    number = ObjectProperty(None)
    info = ObjectProperty(None)
    #current = ObjectProperty(None)
    current_session = ListProperty([['Code', 'Name', 'Price', 'Change', 'Time']])

    def search(self):
        print("Stock Code:", self.number.text)
        try:
            name, price, change, call_time = stock_input(self.number.text, driver)
            self.info.text = f'Stock: {name[0]} {name[1]} \nPrice: {price} \nChange: {change} \nTime: {call_time}'
            #current_session.loc[len(current_session.index)] = [name[0], name[1], price, change, call_time]
            self.current_session.append([name[0], name[1], price, change, call_time])
        except:
            #self.info.text = f'{self.number.text} is an invalid stock code!'
            content = Button(text=f'{self.number.text} is an invalid stock code!')
            popup = Popup(content=content,
                            title='Error',
                            size_hint=(None, None) ,
                            size=(300, 100))
            content.bind(on_press=popup.dismiss)
            popup.open()
        self.number.text = ""

    def history(self):
        print('something')
        #return RV()
        #content = Label(text='Close me!')

        #popup = Popup(content=show(current_session))
        #display = show(current_session)
        # self.current.text = ''
        # for row in self.current_session:
        #     for cat in row:
        #         self.current.text = self.current.text + ' ' + cat
        #     self.current.text += '\n'
        #self.current.text = (i for i in self.current_session)

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(10)]

class HistoryScreen(Screen):
    pass

class HomeApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(StockCode(name='stock'))
        sm.add_widget(HistoryScreen(name='history'))
        sm.title = 'Stock Price Checker'
        return sm


if __name__ == '__main__':
    HomeApp().run()