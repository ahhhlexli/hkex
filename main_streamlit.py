from portfolio_buy import buy
from portfolio_sell import sell 
from pyautogui import press, typewrite, hotkey
from inputter import inputter 
import pandas as pd
import streamlit as st 

st.title('Personal Stock Portfolio')

if st.button('Portfolio'):
    st.write('Hello')




# while True:
    
#     command = input("""
# What would you like to do?

# Buy: 'b'
# Sell: 's'
# Check Stock Quote: 'i'
# Check Portfolio: 'p'
# Quit Program: 'q'

# """)

#     if command == 'b':
#         buy()
#     elif command == 's':
#         sell()
#     elif command == 'q':
#         hotkey('ctrl', 'c')
#     elif command == 'i':
#         inputter()
#     elif command == 'p':
#         df = pd.read_csv('portfolio.csv')
#         print(df)
    