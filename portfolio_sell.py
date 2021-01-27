import pandas as pd
import os 
import inspect
from datetime import datetime

module_path = inspect.getfile(inspect.currentframe())
module_dir = os.path.realpath(os.path.dirname(module_path))
os.chdir(module_dir)

portfolio = pd.read_csv('./portfolio.csv', index_col=0)

print('----------')
stock = input("Enter stock code: ")
print('----------')

status = portfolio.loc[(portfolio.Stock == int(stock)) & (portfolio.Amount_Purchased != portfolio.Amount_Sold)]
print(f"Current Record for Stock {stock}")
print(status)
print('----------')

available = int(status['Amount_Available'].sum())
print(f"Amount Available: {available}")
av_price = round(sum(status['Adjusted_Price'] * status['Amount_Purchased']) / sum(status['Amount_Purchased']), 2)
print(f"Average Purchase Price: {av_price}")
print('----------')


# index_list = list(status.index)
# print(index_list)

amount = int(input("Enter amount sold: "))
sale_price = float(input("Enter sale price: "))
while amount > available:
    print('Invalid amount entered.')
    amount = int(input("Enter amount sold: "))

# print(available - amount)
for index, row in status.iterrows():
    if row['Amount_Available'] < amount:
        amount_sold = row['Amount_Purchased']
        status.at[index, 'Amount_Available'] = 0
        status.at[index, 'Amount_Sold'] = status.at[index, 'Amount_Purchased']
        
        status.at[index, 'Sale_Price'] = row['Sale_Price'] + (amount_sold * sale_price)
        #status.loc[index]['Amount_Available'] = available - row['Amount_Available']
        amount -= row['Amount_Available']
        #print(available)
    elif row['Amount_Available'] >= amount:
        remainder = row['Amount_Available'] - amount
        amount_sold = amount 
        status.at[index, 'Amount_Available'] = remainder 
        status.at[index, 'Amount_Sold'] = row['Amount_Purchased'] - status.at[index, 'Amount_Available']

        status.at[index, 'Sale_Price'] = row['Sale_Price'] + (amount_sold * sale_price)
        break

status.Profit_Loss = [(status.Profit_Loss + status.Sale_Price - status['Purchase Value']) if status.Amount_Purchased == status.Amount_Sold else 0 for i in status.Profit_Loss]

print(status)