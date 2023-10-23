import ttkbootstrap as tb
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
import numpy as np
import numpy_financial as npf


# Create a window
root = tb.Window(themename="darkly") # cyborg, superhero, darkly, solar
root.title("Mortgage Calculator")
#root.logo(logo)

#If Autofit on datagrid is Not set - Use this
root.geometry("1140x780")  # width and height

#If Autofit on datagrid is set - Use this
#my_w.geometry("600x880")  # width and height

# Add functions here:
# =========================

# Define data rows
principalAmount = []

# Define your columns and headings.
columns = ("number", "payment",  "interest pmt", "principal pmt", "balance")

# Create the Tableview widget
dv = tb.tableview.Tableview(
    master=root,
    paginated=True,
    coldata=columns,
    rowdata=principalAmount,
    searchable=False,
    bootstyle="primary",  # primary, secondary, success, info, warning, danger, light, dark, link
    pagesize=12,
    height=12
)

# Grid the tableview widget
dv.grid(row=2, column=0, padx=10)    
    
def calculate():   
   # rate = ((sliderRates.get())/100)/12
 #  value1 = int(meter1['amountused'])

    # Get the value of meter2 and round it to two decimal places
    rate = ((round(ratemeter['amountused'], 2)/100)/12)
    years = int(yearsmeter['amountused'])
    periods = (years * 12)
    principal = int(txtAmount.get())  
    
    # Check if principal is empty or less than or equal to zero
    if not principal or principal <= 0:
        lbl2.config(text=f'"The principal mortgage amount must be greater than zero"')
        return
    
    if rate <= 0.0 and years <= 0: 
        lbl2.config(text=f'"Please enter a valid rate number of years:"')
        return    
   
    lbl2.config(text="")
    
    #principal =(round(int(txtAmount.get()),0), '${:,.2f}'.format(round(txtAmount.get(),2)))
    nper = np.arange(years*12) + 1
    ipmt = npf.ipmt(rate, nper, periods, principal)
    ppmt = npf.ppmt(rate, nper, periods, principal)
    #np.allclose(ipmt + ppmt, pmt)

    # Define data rows
    # principalAmount = []
    # fmt = '{0:d} {1:.2f} {2:.2f} {3:.2f} {4:.2f}'
    dv.delete_rows()

    for payment in nper:
        index = payment - 1
        pmt = (ppmt[index] + ipmt[index])
        principal = principal + ppmt[index]
        #row = [(round(payment,0), round(-pmt,2), round(-ppmt[index],2), round(-ipmt[index],2), round(principal,2))]
        #principalAmount.append(row)
       
        row = [(round(payment,0), 
                '${:,.2f}'.format(round(-pmt,2)),             
                '${:,.2f}'.format(round(-ipmt[index],2)), 
                '${:,.2f}'.format(round(-ppmt[index],2)),
                '${:,.2f}'.format(round(principal,2)))]
        dv.insert_rows('end', row)
  
  
    # Refresh the table view
    dv.load_table_data()
    
#dv.autofit_columns() # adjust the column widths
dv.autoalign_columns() # align the text in the cells

frame = tb.Frame(root)
frame.grid(row=0, column=0, pady=20, padx=350)

#Add a label
lbl1 = tb.Label(frame, text="Enter Loan Amount", font=("Calibri", 16), bootstyle="warning")
lbl1.pack(pady=10)

lbl2 = tb.Label(frame, text="", font=("Helvetica", 20), bootstyle="danger")
lbl2.pack(pady=10)

# Create a StringVar
#txtAmount_var = tb.StringVar()

#Add a text Entry Field
txtAmount = tb.Entry(frame, bootstyle="primary", font=("Calibri", 16))
txtAmount.insert(0, "0")    
txtAmount.pack(pady=10)

#txtAmount = tb.Entry(frame, bootstyle="primary", textvariable=txtAmount_var,  font=("Calibri", 16))
#txtAmount.pack(pady=10)


# Add a trace to the StringVar
#txtAmount_var.trace('w', format_amount)

meter_frame = tb.Frame(root)
meter_frame.grid(row=1, column=0, pady=20, padx=350)

yearsmeter = tb.Meter(meter_frame,
    metersize=150,
    padding=15,
    amountused=15,
    amounttotal=30,
    metertype="semi",
    stripethickness=15, 
    subtext="years",
    interactive=True,
    bootstyle="primary"
)
yearsmeter.grid(row=1, column=0, pady=5)  # Use grid instead of pack


# Create the second meter
ratemeter = tb.Meter(meter_frame,
    metersize=150,
    padding=15,
    amountused=5.25,
    amounttotal=20,
    stepsize = 0.25,
    metertype="semi",
    stripethickness=15, 
    subtext="rate",
    interactive=True,
    bootstyle="success"
)
ratemeter.grid(row=1, column=1, pady=5)  # Place it in the next column

# Add a button
btnCalc = tb.Button(frame, 
        bootstyle="primary outline", 
        width=35,
        text="Calculate", 
        command=calculate)
btnCalc.pack(pady=15)
        
# Start the main loop
root.mainloop()