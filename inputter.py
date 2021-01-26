import time
from datetime import datetime
from selenium import webdriver
import pandas as pd


DRIVER_PATH = 'C:/Program Files (x86)/chromedriver.exe'

query = None
driver = 0

current_session = pd.DataFrame(columns=['Code', 'Name', 'Current Price', 'Change'])

while query != 'q':

    query = input('Enter a valid stock code: ')

    if query.lower() == 'q':
        query == 'q'
        break

    while query.isdigit() == False:
        query = input('Enter a valid stock code: ')

    if driver == 0:
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    etnet = 'http://www.etnet.com.hk/www/eng/stocks/realtime/quote.php?code=' + query

    print(etnet)

    driver.get(etnet)
    driver.find_element_by_xpath('//*[@id="quotesearch_submit"]').click()

    time.sleep(2)

    name = driver.find_element_by_xpath('//*[@id="StkQuoteHeader"]').text
    price = driver.find_element_by_xpath('//*[@id="StkDetailMainBox"]/table/tbody/tr[1]/td[1]/span[1]').text
    change = driver.find_element_by_xpath('//*[@id="StkDetailMainBox"]/table/tbody/tr[1]/td[1]/span[2]').text

    print(name)
    print(price)
    print(change)
    print('\n')
    name = name.split(' ', 1)

    current_session.loc[len(current_session.index)] = [name[0], name[1], price, change]

driver.close()
print('\n')
print(current_session)

save = input('Save current session to csv? (y/n)')
if save == 'y':
    current_session.to_csv(str(datetime.date(datetime.now()))+'.csv')