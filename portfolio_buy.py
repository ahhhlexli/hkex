import pandas as pd
import os 
import inspect
from datetime import datetime

module_path = inspect.getfile(inspect.currentframe())
module_dir = os.path.realpath(os.path.dirname(module_path))
os.chdir(module_dir)

isFile = os.path.isfile('./portfolio.csv') 
print(f"File Exists = {isFile}")
print(os.getcwd())
if isFile == False:
    portfolio = pd.DataFrame(columns=['Stock', 'Purchase_Price','Adjusted_Price',
                                        'Amount_Purchased', 'Amount_Sold', 'Amount_Available',
                                        'Adjusted_Purchase_Total', 'Sale_Price',
                                        'Profit_Loss', 'Date_Purchased', 'Date_Sold'])
    #print(portfolio.columns)
    portfolio.to_csv('./portfolio.csv')

portfolio = pd.read_csv('./portfolio.csv', index_col=0)
#print(portfolio)

print('----------')
stock = input("Enter stock code: ")
print('----------')
price = float(input("Enter purchase price: "))
print('----------')
amount = int(input("Number of shares purchased: "))
print('----------')
adj_price = round(price * 1.0075, 3)
adj_purchase_tot= adj_price * amount

date = datetime.today()
date = date.strftime("%Y-%m-%d")
#print(adj_price)
portfolio.loc[len(portfolio.index)] = [stock, price, adj_price, 
                                        amount, 0, amount,
                                        adj_purchase_tot, 0, 
                                        0, date, 'Not Sold']
portfolio.to_csv('./portfolio.csv')
