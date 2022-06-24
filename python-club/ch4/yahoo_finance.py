import csv
import time

import numpy as np
import yfinance as yf

# test commit. test commit2

# settings
fn = "ticker.txt"
csv_fn = "data.csv"

# number of tickers in a request
limit = 10

# number of tickers
noi = 0
tickers = []

with open(fn) as f:
    for ticker in f:
        noi += 1
        ticker = ticker.rstrip()
        tickers.append(ticker)
        # print(ticker)

print(noi)

# number of repeats
nor = noi // limit + np.sign(noi % limit)

# data
rows = {}

stop = 0

for i in range(nor):
    if stop == 1:
        break

    ticker1 = tickers[i * limit:(i + 1) * limit]
    ticker2 = "".join(ticker1)
    print(ticker1)
    # print(ticker2)
    # continue
    tsd1 = yf.Tickers(ticker2)

    for j in range(len(ticker1)):
        if stop == 1:
            break

        try:
            # debug
            # print(j, tsd1.tickers[ticker1[j]].info)

            # yf data
            tsd = tsd1.tickers[ticker1[j]]

            # data
            row = ["",  "", 0, 0, 0, 0, 0, 0]

            ticker = ticker1[j]
            row[0] = ticker

            if "shortName" in tsd.info.keys():
                row[1] = tsd.info['shortName']
            else:
                print(f"skip. {ticker} is invalid.")

            if "regularMarketPrice" in tsd.info.keys():
                row[2] = tsd.info['regularMarketPrice']
            
            if "trailingAnnualDividendRate" in tsd.info.keys():
                row[3] = tsd.info['trailingAnnualDividendRate']
    
            if "trailingAnnualDividendYield" in tsd.info.keys():
                row[4] = tsd.info['trailingAnnualDividendYield']
    
            if "marketCap" in tsd.info.keys():
                row[5] = tsd.info['marketCap']
    
            if "forwardEps" in tsd.info.keys():
                row[6] = tsd.info['forwardEps']
    
            if "trailingEps" in tsd.info.keys():
                row[7] = tsd.info['trailingEps']

            print(i, j, i * limit + j, row)
            rows[ticker] = row
        except KeyboardInterrupt:
            stop = 1
        except:
            pass

    time.sleep(1.0)
        
# output
# csv
csv_f = open(csv_fn, 'w', newline = '')
csvw = csv.writer(csv_f, delimiter = '\t')

for symbol in sorted(rows.keys()):
    csvw.writerow(rows[symbol])

csv_f.close()

