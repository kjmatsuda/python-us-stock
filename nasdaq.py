import csv
import datetime
import json
import time

import numpy as np
import requests

# settings
# csv
csv_fn = 'data_nasdaq.csv'

# output
rows = {}

### 1. stock
url =  "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"
headers = {'user-agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
response = requests.get(url, headers = headers)
data = json.loads(response.text)

# print(data)

for i, item in enumerate(data["data"]["rows"]):
    row = ["", "", 0, 0]

    # symbol
    symbol = item["symbol"]
    symbol = symbol.replace("/", "-")
    symbol = symbol.replace("^", "-")
    row[0] = symbol

    # name
    row[1] = item["name"]

    # price
    lastsale = item["lastsale"]
    lastsale = lastsale.replace("$", "")
    if lastsale == "":
        lastsale = 0
    row[2] = lastsale

    # market cap
    marketCap = item["marketCap"]
    if marketCap == "":
        marketCap = 0
    row[3] = marketCap

    print(i, row)
    rows[symbol] = row

### 2. ETF
### nasdaq data, separately
### stable, fow data are lost.

# number of items
# noi = 2150
url =  "https://api.nasdaq.com/api/screener/etf?tableonly=true&order=asc&limit=10&offset=0"
headers = {'user-agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
response = requests.get(url, headers = headers)
data = json.loads(response.text)

noi = data["data"]["records"]["totalrecords"]
print(noi)

# limit of visible records
limit = 50
# number of repeats
nor = noi // limit + np.sign(noi % limit)

stop = 0

for i in range((noi * 5) // limit):
    if stop == 1:
        break

    url =  f"https://api.nasdaq.com/api/screener/etf?tableonly=true&order=asc&limit={limit}&offset={(i*limit)%noi}"
    print(url)
    headers = {'user-agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    response = requests.get(url, headers = headers)
    data = json.loads(response.text)

    for j, item in enumerate(data["data"]["records"]["data"]["rows"]):
        try:
            row = ["", "", 0, 0]

            # symbol
            symbol = item["symbol"]
            symbol = symbol.replace("/", "-")
            symbol = symbol.replace("^", "-")
            row[0] = symbol

            # name
            row[1] = item["companyName"]

            # price
            lastsale = item["lastSalePrice"]
            lastsale = lastsale.replace("$", "")
            if lastsale == "":
                lastsale = 0
            row[2] = lastsale

            # market cap
            row[3] = 0

            print(i * limit + j, row)
            rows[symbol] = row
        except KeyboardInterrupt:
            stop = 1
        except:
            pass

    time.sleep(1.1)


# csv
csv_f = open(csv_fn, 'w', newline = '')
csvw = csv.writer(csv_f, delimiter = '\t')
for symbol in sorted(rows.keys()):
    csvw.writerow(rows[symbol])
csv_f.close()
