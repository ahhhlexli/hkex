def sell():
    import pandas as pd
    import os 
    import inspect
    from datetime import datetime

    module_path = inspect.getfile(inspect.currentframe())
    module_dir = os.path.realpath(os.path.dirname(module_path))
    os.chdir(module_dir)
    date = datetime.today().strftime("%Y-%m-%d")


    portfolio = pd.read_csv('./portfolio.csv', index_col=0)
    portfolio.Stock = portfolio.Stock.astype(dtype='int32')

    print('----------')
    stock = input("Enter stock code: ")
    print('----------')

    status = portfolio.loc[(portfolio.Stock == int(stock)) & (portfolio.Amount_Purchased != portfolio.Amount_Sold)]
    print(f"Current Record for Stock {stock}")
    print(status)
    print('----------')

    available = int(status['Amount_Available'].sum())
    print(f"Amount Available: {available}")

    #STORE AV PRICE AS A DIFFERENT FEATURE IN MAIN
    # av_price = round(sum(status['Adjusted_Price'] * status['Amount_Purchased']) / sum(status['Amount_Purchased']), 2)
    # print(f"Average Purchase Price: {av_price}")
    print('----------')

    amount = int(input("Enter amount sold: "))
    while amount > available:
        print('Invalid amount entered.')
        amount = int(input("Enter amount sold: "))
    sale_price = float(input("Enter sale price: "))

    # print(available - amount)
    for index, row in status.iterrows():
        if row['Amount_Available'] < amount:
            amount_sold = row['Amount_Purchased'] - row['Amount_Sold'] #row['Amount_Purchased']
            status.at[index, 'Amount_Available'] = 0
            status.at[index, 'Amount_Sold'] = status.at[index, 'Amount_Purchased']
            status.at[index, 'Date_Sold'] = date
            status.at[index, 'Sale_Price'] = row['Sale_Price'] + (amount_sold * sale_price)
            #status.loc[index]['Amount_Available'] = available - row['Amount_Available']
            amount -= row['Amount_Available']
            #print(available)
        elif row['Amount_Available'] >= amount:
            remainder = row['Amount_Available'] - amount
            amount_sold = amount 
            status.at[index, 'Amount_Available'] = remainder 
            status.at[index, 'Amount_Sold'] = row['Amount_Purchased'] - status.at[index, 'Amount_Available']
            status.at[index, 'Date_Sold'] = date
            status.at[index, 'Sale_Price'] = row['Sale_Price'] + (amount_sold * sale_price)
            break

    for i in range(len(status)):
        if status.Amount_Purchased.iloc[i] == status.Amount_Sold.iloc[i]:
            status.Profit_Loss.iloc[i] = status.Sale_Price.iloc[i] - status.Adjusted_Purchase_Total.iloc[i]

    print(f"Overview of This Sale - {stock}")
    print('-----')
    print(status)
    print('-----')
    print('Portfolio Overview')
    print('-----')
    portfolio.update(status)
    portfolio.Stock = portfolio.Stock.astype(dtype='int32')
    print(portfolio)
    portfolio.to_csv('./portfolio.csv')
