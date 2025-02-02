import os
import pandas as pd
import matplotlib.pyplot as plt
import json
from glob import glob

transaction_file_path = r"C:\Content\Crypto\CoinTracker_Transactions"
# file_name = "SHIB_transactions.csv"
# transaction_file = os.path.join(transaction_file_path,file_name)
ouput_json = os.path.join(transaction_file_path,'all_coins_cost_basis.json')
files = glob(os.path.join(transaction_file_path,"*_transactions.csv"))

def transactions(file):
    coin_dict = {"cost_basis": 0,
                 "avg_cost": 0,
                 "num_shares":0,
                 "realized_return":0}
    coiney = os.path.basename(file).split("_")[0]
    df = pd.read_csv(file)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date', ascending=True)
    cost_basis_value = 0
    cost_basis_values = []
    num_shares = 0
    num_shares_values = []
    avg_cost = 0
    realized_return = 0
    realized_returns = []
    avg_costs = []
    dates = []
    # if coiney in ["Bitcoin", "CRO"]:
    for index, row in df.iterrows():
        if row["Type"] == "BUY":
            transaction_price = float(row["Sent Quantity"])/float(row["Received Quantity"])
            cost_basis_value += float(row["Sent Quantity"])
            num_shares += float(row["Received Quantity"])
            print(f"cost basis: {cost_basis_value}")
            steve=1
        if row["Type"] == "SELL":
            transaction_price = float(row["Received Quantity"])/float(row["Sent Quantity"])
            sell_value = float(row["Received Quantity"])
            cost = float(row["Sent Quantity"]) * avg_cost
            profit = sell_value-cost
            realized_return+=profit
            cost_basis_value -= cost
            num_shares -= float(row["Sent Quantity"])
            # realized_return += float(row["Realized Return (USD)"])
            print(f"cost basis: {cost_basis_value}")
            steve=1
        if row["Type"] == "SEND":
            num_shares -= float(row["Sent Quantity"])
            cost_basis_value -= float(row["Sent Quantity"]) * avg_cost
        cost_basis_values.append(cost_basis_value)
        num_shares_values.append(num_shares)
        realized_returns.append(realized_return)
        dates.append(row['Date'])
        if num_shares > 0:
            avg_cost = cost_basis_value/num_shares
        else:
            avg_cost = 0
        if cost_basis_value < 0:
            cost_basis_value = 0
        print(f"avg cost: {avg_cost}")
        avg_costs.append(avg_cost)
    # else:
    #     for index,row in df.iterrows():
    #         if row["Type"] == "BUY":
    #             cost_basis_value += float(row["Received Cost Basis (USD)"])
    #             num_shares += float(row["Received Quantity"])
    #         if row["Type"] == "SELL":
    #             cost_basis_value -= float(row["Sent Cost Basis (USD)"])
    #             num_shares -= float(row["Sent Quantity"])
    #             realized_return += float(row["Realized Return (USD)"])
    #         else:
    #             continue
    #         cost_basis_values.append(cost_basis_value)
    #         num_shares_values.append(num_shares)
    #         realized_returns.append(realized_return)
    #         dates.append(row['Date'])
    #         avg_cost = cost_basis_value/num_shares
    #         avg_costs.append(avg_cost)
    coin_dict['cost_basis'] = cost_basis_value
    coin_dict['avg_cost'] = '{:.10f}'.format(avg_cost)
    coin_dict['num_shares'] = num_shares
    coin_dict['realized_return'] = realized_return

    # fig, axs = plt.subplots(2)
    # axs[0].plot(dates, cost_basis_values)
    # axs[1].plot(dates, num_shares_values)
    # fig.show()
    # steve = 1

    return coin_dict

if __name__ == "__main__":
    data_dict = {}
    for transaction_file in files:
        coin = os.path.basename(transaction_file).split("_")[0]
        data_dict[coin] = transactions(transaction_file)
    with open(ouput_json,'w') as fout:
        json.dump(data_dict,fout, indent = 2)