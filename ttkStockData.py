import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
import datetime as dt
import sqlite3

app = ttk.Window(themename="cyborg")
colors = app.style.colors

app.geometry("1140x780") 

coldata = [
    {"text": "Ticker", "stretch": False},
    {"text": "Date", "stretch": False},
    {"text": "open", "stretch": False},
    {"text": "high", "stretch": False},
    {"text": "low", "stretch": False},
    {"text": "close", "stretch": False},
    {"text": "volume", "stretch": False},
    {"text": "adjclose", "stretch": False},
]

# Connect to the SQLite database
conn = sqlite3.connect('C:/Users/storl/stocks.db')
c = conn.cursor()

# Query the database
c.execute('SELECT * FROM stocks')

# Load query results into an array of arrays
rowdata = []
for row in c.fetchall():
     formatted_row = [
        row[0],  # Ticker 
        row[1].split(' ')[0],  # Format timestamp as date
        '${:,.2f}'.format(row[2]),  # Format open
        '${:,.2f}'.format(row[3]),  # Format high
        '${:,.2f}'.format(row[4]),  # Format low
        '${:,.2f}'.format(row[5]),  # Format close
        '{:,}'.format(int(row[6])),  # Format volume
        '${:,.2f}'.format(row[7])   # Format adjclose
    ]
     rowdata.append(formatted_row)

# Close connection
conn.close()

dt = Tableview(
    master=app,
    coldata=coldata,
    rowdata=rowdata,
    paginated=True,
    searchable=True,
    bootstyle="warnings",
    stripecolor=None,
    pagesize=50,
    height=12
    # stripecolor=(colors.light, None),
)
dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)

app.mainloop()
