import requests
import json
# import csv
import argparse
import sqlite3
import datetime as dt_module


"""
_summary_
   This code calls Yahoo Finance API to get stock data for a given ticker, data interval
   and date range. Valid inputs are:
   
ticker: stock ticker symbol
   
Interval:
   For the interval parameter in the Yahoo Finance API url, you can specify 
   different time intervals for the data:
    1m - 1 minute
    2m - 2 minutes
    5m - 5 minutes
    15m - 15 minutes
    30m - 30 minutes
    60m - 60 minutes (1 hour)
    90m - 90 minutes
    1h - 1 hour
    1d - 1 day
    5d - 5 days
    1wk - 1 week
    1mo - 1 month
    3mo - 3 months

date_range:
    For the date_range parameter expects a string representing the range of dates to get data for.
    Some examples of valid values:
    "1d" - 1 day
    "5d" - 5 days
    "1mo" - 1 month
    "3mo" - 3 months
    "6mo" - 6 months
    "1y" - 1 year
    "2y" - 2 years
    "5y" - 5 years
    "10y" - 10 years
    "ytd" - Year to date
    "max" - Max range

calling syntax:
python "C:/Users/storl/miniconda3/envs/torenv/GetStockdataFromYahoo.py" --symbol PLTR --date_range 3mo --interval 1d --output_file PLTR_2023-10-18.csv   
python "C:/Users/storl/miniconda3/envs/torenv/GetStockdataFromYahoo.py" --symbol PLTR --date_range 3mo --interval 1d --db_file stocks.db

Returns:
    _type_: json object
"""


# Create argument parser
parser = argparse.ArgumentParser(description='Retrieve stock data from Yahoo Finance and write it to a CSV file.')

# Add arguments
parser.add_argument('--symbol', type=str, help='Stock symbol to retrieve data for (e.g. ABBV)')
parser.add_argument('--date_range', type=str, default='1d', help='Date range to retrieve data for (e.g. 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)')
# Add arguments
parser.add_argument('--interval', type=str, default='1d', help='interval range to retrieve data for (e.g. 1m, 2m,5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)')
parser.add_argument('--db_file', type=str, help='Name of sqllite3 database file')
# parser.add_argument('--output_file', type=str, help='Name of output CSV file')

# Parse arguments
args = parser.parse_args()

# Create User-Agent header
# Note: Open Google Chrome and type in 
# "my user agent" to get your user agent string
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

        
def get_data_from_web_api(ticker, interval, date_range):
    base_url = "https://query1.finance.yahoo.com/v8/finance/chart/"
    query_url = f"{ticker}?region=US&lang=en-US&includePrePost=false&interval={interval}&range={date_range}&corsDomain=finance.yahoo.com&.tsrc=finance"
    url = base_url + query_url
    print(url)
    response = requests.get(url, headers=headers)
    print("response status code:", response.status_code)
    return response.text
 
def convert_timestamps(timestamps):
    # dates = []   
    for ts in timestamps:
         return [dt_module.datetime.fromtimestamp(ts) for ts in timestamps]
        
def parse_stock_data(json_data, output_file, ticker):
    data = json.loads(json_data)    
    meta = data['chart']['result'][0]['meta']
    indicators = data['chart']['result'][0]['indicators']
    timestamps = convert_timestamps(data['chart']['result'][0]['timestamp'])
    
    stock_data = {
        'timestamps': timestamps,
        'open': indicators['quote'][0]['open'],
        'high': indicators['quote'][0]['high'],
        'low': indicators['quote'][0]['low'],
        'close': indicators['quote'][0]['close'],
        'volume': indicators['quote'][0]['volume'],
        'adjclose': indicators['adjclose'][0]['adjclose']
    }

    try:
    # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        # Create table if it doesn't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS stocks (
                ticker TEXT,
                timestamp TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                adjclose REAL
            )
        ''')

        # Insert data into the table
        for i in range(len(stock_data['timestamps'])):
            c.execute('''
                INSERT INTO stocks VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                ticker,
                str(stock_data['timestamps'][i]),
                stock_data['open'][i],
                stock_data['high'][i],
                stock_data['low'][i],
                stock_data['close'][i],
                stock_data['volume'][i],
                stock_data['adjclose'][i]
            ))

        # Commit changes and close connection
        conn.commit()
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")
    finally:
        conn.close()
    
    # print(stock_data)
    
    # Open the CSV file in write mode
    # with open('' + output_file, 'w', newline='') as file:
    #     writer = csv.writer(file)
        
    #     # Write the header
    #     writer.writerow(stock_data.keys())
        
    #        # Write the data
    #     data_rows = [[stock_data[key][i] for key in stock_data.keys()] for i in range(len(stock_data['timestamps']))]
    #     writer.writerows(data_rows)


    return stock_data

ticker = args.symbol
interval= args.interval
date_range = args.date_range
db_file = args.db_file

# output_file = args.output_file

print('ticker:' + ticker, 'int:' + interval, 'dt:' + date_range, 'outf:' + db_file)

json_data = get_data_from_web_api(ticker, interval, date_range)


# Pass json_data to parse function
stock_data = parse_stock_data(json_data, db_file, ticker)
# stock_data = parse_stock_data(json_data, output_file)
# print(stock_data)

