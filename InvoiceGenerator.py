from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from docxtpl import DocxTemplate
import pymysql as myconn
import datetime


# Create the main window
root = Tk()

# Set the window title
root.title("Invoice Generator")

# Set the window size
root.geometry("1540x780+0+0")
root.resizable(False,False)
root['background']='gray'

InvoiceNumber=IntVar()
Company=StringVar()
GSTNumber=StringVar()
ProductName=StringVar()
Quantity=IntVar()
Date=StringVar()
Rate=StringVar()
Price=StringVar()

invoice_list = []




def generate_invoice():
    doc = DocxTemplate("invoice_template.docx")
    name = customer_entry.get()
    invoice = invoice_entry.get()
    subtotal = float(price_entry.get())
    salestax = float(gst_entry.get())
    gstprice = (subtotal*salestax)/100
    total = subtotal+gstprice

    doc.render({"name":name,  
                "invoice":invoice, 
                "invoice_list":invoice_list, 
                "subtotal":subtotal, 
                "salestax":salestax, 
                "total":total})
    
    doc_name = "new_invoice" + name + datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S") + ".docx"
    doc.save(doc_name)
    
    messagebox.showinfo("Invoice Complete","Invoice Generated")

def entrydata():
    if invoice_entry.get()=='' or gst_entry.get()=='':
        messagebox.showerror('Error','All fields are Required')
    else:
        con=myconn.connect(host='localhost',user='root',password='tejas02_',database="Entries")
        mycursor=con.cursor()
        query='insert into entrydata(invoice_number, company_name, gst_number, date, product_name, quantity, gstrate, price) values(%s, %s, %s, %s, %s, %s, %s, %s)'
        mycursor.execute(query, (invoice_entry.get(),customer_entry.get(),gst_entry.get(),date_entry.get(),product_Entry.get(),quantity_entry.get(),GSTRate_entry.get(),price_entry.get()))
        
        mycursor.execute("select * from entrydata")
        rows=mycursor.fetchall()
        if len(rows)!=0:
            Entries_Table.delete(*Entries_Table.get_children())
        for i in rows:
            Entries_Table.insert("",END,values=i)
            

        con.commit()
        # fetchdata()
        con.close()

# def selected_items(tree):
#     curItem=tree.focus()
#     values=tree.item(curItem,"values")
#     print(values)
def entrydata1():
    print("in entrydata1")
    # if invoice_entry.get()=='' or gst_entry.get()=='':
    #     messagebox.showerror('Error','All fields are Required')
    # else:
    con=myconn.connect(host='localhost',user='root',password='tejas02_',database="Entries")
    mycursor=con.cursor()
    query='insert into entrydata(invoice_number, company_name, gst_number, date, product_name, quantity, gstrate, price) WHERE invoice_number = '+invoice_entry.get()+' values(%s, %s, %s, %s, %s, %s, %s, %s)'
    #mycursor.execute(query, (invoice_entry.get(),customer_entry.get(),gst_entry.get(),date_entry.get(),product_Entry.get(),quantity_entry.get(),GSTRate_entry.get(),price_entry.get()))
    
    mycursor.execute("select * from entrydata")
    rows=mycursor.fetchall()
    if len(rows)!=0:
        Entries_Table.delete(*Entries_Table.get_children())
    for i in rows:
        Entries_Table.insert("",END,values=i)
        

    con.commit()
    # fetchdata()
    con.close()

def Update():
    print("in update")
    entrydata1()
    cursor_row=Entries_Table.focus()
    content=Entries_Table.item(cursor_row)
    print("content",content)

    row=content["values"]
    print("row",row)
    InvoiceNumber.set(row[0])
    Company.set(row[1])
    GSTNumber.set(row[2])
    ProductName.set(row[3])
    Quantity.set(row[4])
    Date.set(row[5])
    Rate.set(row[6])
    Price.set(row[7])
    entrydata1()

def select_record():
    InvoiceNumber.delete(0, END)
    Company.delete(0, END)
    GSTNumber.delete(0, END)
    ProductName.delete(0, END)
    Quantity.delete(0, END)
    Date.delete(0, END)
    Rate.delete(0, END)
    Price.delete(0, END)

    Selected = Entries_Table.focus()
    values = Entries_Table.item(Selected, 'values')
    temp_label.config(text=values)

#     InvoiceNumber.insert(0, END)
#     Company.insert(0, END)
#     GSTNumber.insert(0, END)
#     ProductName.insert(0, END)
#     Quantity.insert(0, END)
#     Date.insert(0, END)
#     Rate.insert(0, END)
#     Price.insert(0, END)

def delete_record():
    con=myconn.connect(host='localhost',user='root',password='tejas02_',database="Entries")
    mycursor=con.cursor()
    value=int(InvoiceNumber.get())
    print(value)
    mycursor.execute(f"delete from entrydata where invoice_number={value}")
    con.commit()
    mycursor.execute(f"select * from entrydata where invoice_number={value}")
    rows=mycursor.fetchall()
    if len(rows)==0:
        messagebox.showinfo("Success","Record Delete Successfully")
        entrydata1()
    else:
        messagebox.showinfo("Failure","Record not Deleted")

    

    con.commit()
    entrydata()


def get_cursor(event=""):
    cursor_row=Entries_Table.focus()
    content=Entries_Table.item(cursor_row)
    row=content["values"]
    InvoiceNumber.set(row[0])
    Company.set(row[1])
    GSTNumber.set(row[2])
    ProductName.set(row[3])
    Quantity.set(row[4])
    Date.set(row[5])
    Rate.set(row[6])
    Price.set(row[7])

       
def gst_cal():
    
    root1 = tk.Tk()

    class GSTCalculator:
        def __init__(self, master):
            self.master = master
            master.title("GST Calculator")

            # Create entry fields for price and GST rate
            tk.Label(master, text="Price (Rs.):").grid(row=0, column=0, padx=5, pady=5)
            self.price_entry = tk.Entry(master)
            self.price_entry.grid(row=0, column=1, padx=5, pady=5)
            tk.Label(master, text="GST Rate (%):").grid(row=1, column=0, padx=5, pady=5)
            self.rate_entry = tk.Entry(master)
            self.rate_entry.grid(row=1, column=1, padx=5, pady=5)

            # Create calculate button
            tk.Button(master, text="Calculate GST", command=self.calculate_gst).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

            # Create result label
            tk.Label(master, text="GST Amount (Rs.):").grid(row=3, column=0, padx=5, pady=5)
            self.result_label = tk.Label(master, text="")
            self.result_label.grid(row=3, column=1, padx=5, pady=5)

        def calculate_gst(self):
            try:
                price = float(self.price_entry.get())
                rate = float(self.rate_entry.get())
                gst = (price * rate) / 100
                self.result_label.config(text="{:.2f}".format(gst))
            except:
                self.result_label.config(text="Error")

    # Create the main window


    # Create the GST Calculator app
    app = GSTCalculator(root1)

    # Run the main loop
    root.mainloop()


       

# def Add_Tree():
    # invoiceno = int(invoice_entry.get())
    # companyname = customer_entry.get()
    # gstno = gst_entry.get()
    # productname = product_Entry
    # quantity = quantity_entry
    # date = date_entry
    # gstrate = GSTRate_entry
    # price = price_entry
    # invoice_item = [invoiceno, companyname, gstno, productname, quantity, date, gstrate, price]

    # Entries_Table.insert('',0, values=invoice_item)

    
# def fetchdata():
#     con=myconn.connect(host='localhost',user='root',password='tejas02_',database="Entries")
#     mycursor=con.cursor()
#     mycursor.execute("select * from entrydata")
#     rows=mycursor.fetchall()
#     if len(rows)!=0:
#         Entries_Table.delete(*Entries_Table.get_children())
#         for i in rows:
#             Entries_Table.insert("",END,values=i)
#             messagebox.showinfo("Success","Entries Added Successfully")
#             con.commit()
#             con.close()

def Cancel():
    InvoiceNumber.set("")
    Company.set("")
    GSTNumber.set("")
    ProductName.set("")
    Quantity.set("")
    Date.set("")
    Rate.set("")
    Price.set("")

def Quit():
    quit=messagebox.askyesno("Invoice Generator","Confirm You want To Quit")
    if quit>0:
        root.destroy()
        return
            


# Create labels and entry boxes for the invoice information

#======================INVOICE LABEL AND ENTRY=======================================
invoice_label = Label(root, text="Invoice Number :", bg='gray',fg='white')
invoice_label.place(x=50, y=50)

invoice_entry = Entry(root, textvariable=InvoiceNumber)
invoice_entry.place(x=200, y=50)

#======================CUSTOMER NAME LABEL AND ENTRY=======================================

customer_label = Label(root, text="Company Name :",  bg='gray',fg='white')
customer_label.place(x=50, y=90)

customer_entry = Entry(root, textvariable=Company)
customer_entry.place(x=200, y=90)

#======================GST NUMBER LABEL AND ENTRY=======================================

gst_label = Label(root, text="GST Number :",  bg='gray',fg='white')
gst_label.place(x=50, y=130)

gst_entry = Entry(root, textvariable=GSTNumber)
gst_entry.place(x=200, y=130)

#======================PRODUCT LABEL AND ENTRY=======================================

# Create a label and listbox for the products
product_label = Label(root, text="Product :",  bg='gray',fg='white')
product_label.place(x=50, y=200)

product_Entry = Entry(root, textvariable=ProductName)
product_Entry.place(x=200, y=200)

#======================QUANTITY LABEL AND ENTRY=======================================


quantity_label = Label(root, text="Quantity :",  bg='gray',fg='white')
quantity_label.place(x=50, y=240)

quantity_entry = Entry(root, textvariable=Quantity)
quantity_entry.place(x=200, y=240)



#======================DATE LABEL AND ENTRY=======================================

# Create a label and entry box for the date
date_label = Label(root, text="Date (dd/mm/yyyy ):",  bg='gray',fg='white')
date_label.place(x=50, y=280)

date_entry = Entry(root, textvariable=Date)
date_entry.place(x=200, y=280)

#======================GST Rate LABEL AND ENTRY=======================================


GSTRate_label = Label(root, text="GST Rate(%) :",  bg='gray',fg='white')
GSTRate_label.place(x=50, y=320)

GSTRate_entry = Entry(root, textvariable=Rate)
GSTRate_entry.place(x=200, y=320)

#======================PRICE LABEL AND ENTRY=======================================

# Create a label and entry box for the price
price_label = Label(root, text="Price :",  bg='gray',fg='white')
price_label.place(x=50, y=360)

price_entry = Entry(root, textvariable=Price)
price_entry.place(x=200, y=360)


temp_label = Label(root, text="", bg='white')
temp_label.place(x=500, y=320)

# Create a function to generate the bill
def generate_bill():
    # Get the invoice information from the entry boxes
    invoice_number = invoice_entry.get()
    customer_name = customer_entry.get()
    gst_number = gst_entry.get()
    
    # Get the selected product from the listbox
    selected_product = product_Entry.get()
    Quantity = quantity_entry.get()
    
    # Get the date and price from the entry boxes
    date = date_entry.get()
    gst_rate = GSTRate_entry.get()
    price = price_entry.get()
    
    # Create a text widget to display the bill
    bill_text = Text(root, height=20, width=50)
    bill_text.place(x=500, y=50)

    #===========================CALCULATE GST PRICE RATE==================================

    price = float(price_entry.get())
    rate = float(GSTRate_entry.get())
    gst = (price * rate) / 100

    #===========================CALCULATE TOTAL==================================

    Quantity = int(quantity_entry.get())
    price = float(price_entry.get())
    Total = (Quantity * price) + gst


    #==============================RESULT TEXT===============================
    
    # Insert the invoice information into the bill
    bill_text.insert(END, "Invoice Number: {}\n".format(invoice_number))
    bill_text.insert(END, "Customer Name: {}\n".format(customer_name))
    bill_text.insert(END, "GST Number: {}\n".format(gst_number))
    bill_text.insert(END, "----------------------------------------\n")
    
    # Insert the product, date, and price into the bill
    bill_text.insert(END, "Product: {}\n".format(selected_product))
    bill_text.insert(END, "Quantity: {}\n".format(Quantity))
    bill_text.insert(END, "Date: {}\n".format(date))
    bill_text.insert(END, "GST Rate(%): {}\n".format(gst_rate))
    bill_text.insert(END, "Price: {}\n".format(price))
    bill_text.insert(END, "----------------------------------------\n")
    bill_text.insert(END, "GST Price: {}\n".format(gst))
    bill_text.insert(END, "Total Price(with GST): {}\n".format(Total))

#==============================GENERATE BUTTON=======================


    
# Create a button to generate the bill
generate_button = Button(root, text="G:Generate Bill",command=generate_bill, bd=0, cursor='hand2', padx=20, pady=10, 
                         background='#E6F0FF',activebackground='#E6F0FF', fg='#FF9900',activeforeground='orange',font=('century', 9, "bold"))
generate_button.place(x=50, y=400)

addentry_button = Button(root, text="A:Add Entry",command=entrydata, bd=0, cursor='hand2', padx=20, pady=10, 
                         background='#E6F0FF',activebackground='#E6F0FF', fg='orange',activeforeground='orange',font=('century', 9,"bold"))
addentry_button.place(x=220, y=400)


save_button = Button(root, text="S:Save(Database)",bd=0, cursor='hand2', padx=20, pady=10, 
                         background='#E6F0FF',activebackground='#E6F0FF', fg='orange',activeforeground='orange',font=('century', 9,"bold"))
save_button.place(x=370, y=400)

update_button = Button(root, text="U:Update",command=Update, bd=0, cursor='hand2', padx=20, pady=10, 
                         background='#E6F0FF',activebackground='#E6F0FF', fg='orange',activeforeground='orange',font=('century', 9, "bold"))
update_button.place(x=560, y=400)

delete_button = Button(root, text="D:Delete",command=delete_record,bd=0, cursor='hand2', padx=20, pady=10, 
                         background='#E6F0FF',activebackground='#E6F0FF', fg='orange',activeforeground='orange',font=('century', 9, "bold"))
delete_button.place(x=710, y=400)

gstcal_button = Button(root, text="GC:GST Calculator",bd=0, cursor='hand2', padx=20, pady=10, 
                         background='#E6F0FF',activebackground='#E6F0FF', command = lambda : gst_cal(), fg='orange',activeforeground='orange',font=('century', 9, "bold"))
gstcal_button.place(x=840, y=400)

print_button = Button(root, text="P:Print",bd=0, command=generate_invoice, cursor='hand2', padx=20, pady=10, 
                         background='#E6F0FF',activebackground='#E6F0FF', fg='orange',activeforeground='orange',font=('century', 9, "bold"))
print_button.place(x=1050, y=400)

clear_button = Button(root, text="C:Clear",command=Cancel, bd=0, cursor='hand2', padx=20, pady=10, 
                         background='#E6F0FF',activebackground='#E6F0FF', fg='orange',activeforeground='orange',font=('century', 9, "bold"))
clear_button.place(x=1190, y=400)


Quit_button = Button(root, text="Q:Quit",bd=0,command=Quit, cursor='hand2', padx=20, pady=10, 
                         background='#E6F0FF',activebackground='#E6F0FF', fg='orange',activeforeground='orange',font=('century', 9, "bold"))
Quit_button.place(x=1390, y=400)
#======================================SCROLLBAR=============================

Entries_Table = ttk.Treeview(root, columns=("InvoiceNumber","Company","GSTNumber","Date","ProductName","Quantity","Rate","Price"))



Entries_Table.heading("InvoiceNumber",text="Invoice Number")
Entries_Table.heading("Company",text="Comapany Name")
Entries_Table.heading("GSTNumber",text="GST Number")
Entries_Table.heading("Date",text="Date")
Entries_Table.heading("ProductName",text="Product Name")
Entries_Table.heading("Quantity",text="Quantity")
Entries_Table.heading("Rate",text="GST Rate")
Entries_Table.heading("Price",text="Price")

Entries_Table["show"]="headings"
Entries_Table.place(x=0,y=480)
Entries_Table.bind("<ButtonRelease-1>",get_cursor)
# fetchdata()
entrydata()



# Run the main loop
root.mainloop()
