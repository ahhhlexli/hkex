def inputter():

    import time
    import os
    import inspect
    from pyautogui import press, typewrite, hotkey
    from datetime import datetime
    from selenium import webdriver
    import pandas as pd
    from selenium.webdriver.support.ui import WebDriverWait

    module_path = inspect.getfile(inspect.currentframe())
    module_dir = os.path.realpath(os.path.dirname(module_path))
    os.chdir(module_dir)
    #`print(os.getcwd())


    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--log-level=3")

    DRIVER_PATH = 'C:/Program Files (x86)/chromedriver.exe'

    query = None
    driver = 0

    current_session = pd.DataFrame(columns=['Code', 'Name', 'Current Price', 'Change', 'Time'])

    while query != 'q':

        query = input('''
Enter a valid stock code: 
Enter 'q' to quit.''')

        if query.lower() == 'q':
            query == 'q'
            break

        while query.isdigit() == False:
            query = input('Enter a valid stock code: ')

        if driver == 0:
            driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=chrome_options)
            driver.set_window_size(1440, 900) 
            #driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        etnet = 'http://www.etnet.com.hk/www/eng/stocks/realtime/quote.php?code=' + query

        print(etnet)

        driver.get(etnet)
        driver.find_element_by_xpath('//*[@id="quotesearch_submit"]').click()

        time.sleep(2)

        name = driver.find_element_by_xpath('//*[@id="StkQuoteHeader"]').text
        price = driver.find_element_by_xpath('//*[@id="StkDetailMainBox"]/table/tbody/tr[1]/td[1]/span[1]').text
        change = driver.find_element_by_xpath('//*[@id="StkDetailMainBox"]/table/tbody/tr[1]/td[1]/span[2]').text
        current_time = datetime.now()
        call_time = current_time.strftime("%Y-%m-%d %H:%M")

        print(name)
        print(price)
        print(change)
        print(call_time)
        print('\n')
        name = name.split(' ', 1)

        current_session.loc[len(current_session.index)] = [name[0], name[1], price, change, call_time]

    try:
        driver.close()
    except:
        pass
    print('\n')
    print(current_session)

    save = input('Save current session to csv? (y/n)  ')
    if save == 'y':
        current_time = current_time.strftime("%Y-%m-%d %H%M")
        current_session.to_csv('./' + current_time + '.csv')

    # print('\n')

