import csv
import json
import requests

"""
get tickers of stocks
"""

# settings

# lower limit of market capacity
lower_limit = 2000000000

#csv
csv_fn = "ticker_stock.txt"

#output
rows = {}

# url
url_stock =  "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"

# it's needed
headers = {'user-agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
f = requests.get(url_stock, headers = headers)
data = f.json()

# print(data["data"]["headers"])

for i, d in enumerate(data["data"]["rows"]):
    row = []

    # symbol
    symbol = d["symbol"]
    symbol = symbol.replace("/", "-")
    symbol = symbol.replace("^", "-")
    row.append(symbol)

    # name
    name = d["name"]
    row.append(name)

    # sector
    sector = d["sector"]
    row.append(sector)

    # industry
    industry = d["industry"]
    row.append(industry)
    
    # market cap
    marketCap = d["marketCap"]
    try:
        mc = float(marketCap)
        if mc > lower_limit:
            rows[symbol] = row
    except:
        # BRK-B, RDS-B, BF-B, JW-A
        if symbol in ["BRK-B", "RDS-B", "BF-B", "JW-A"]:
            rows[symbol] = row
        pass

    print(i, row)

# output
# csv
csv_f = open(csv_fn, 'w', newline = '')
csvw = csv.writer(csv_f, delimiter = '\t')

for symbol in sorted(rows.keys()):
    csvw.writerow(rows[symbol])

csv_f.close()
