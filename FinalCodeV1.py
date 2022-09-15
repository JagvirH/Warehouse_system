from tkinter import *   
import time
import mysql.connector
import random
global mydb
import tkinter.ttk as ttk
from hashlib import sha256
from tkinter import messagebox

global username_ID

# Connects my code to my database
mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    passwd="jagvir02",
    database="Stock_Control"
    )
 
##to_do = []
window1=Tk()
window1.geometry("1300x1000")
window1.configure(bg='lightgrey')
window1.title("")
to_do_sidebar = Scrollbar(window1)
to_do_box_place=Listbox(window1,height=5,width=35,yscrollcommand=to_do_sidebar.set,fg="blue",bg="red",font=('times', 15, 'italic'))

def options_for_user(): # this defenition is called from the bottom of the user login for the 4 pages

    # This is where the order list is holoding all new new orders done through the system
    treeOrder = ttk.Treeview(window1,height=35)
    treeOrder["columns"] = ("company_Name","company_ID","description","location")
    treeOrder.column("#0",width=100,minwidth=25)
    treeOrder.column("company_Name",width=100,minwidth=25)
    treeOrder.column("company_ID",width=100,minwidth=25)
    treeOrder.column("description",width=100,minwidth=25)
    treeOrder.column("location",width=100,minwidth=25)
    treeOrder.heading("#0", text = "Task")
    treeOrder.heading("company_Name", text = "Customer Name")
    treeOrder.heading("company_ID",text="Company ID")
    treeOrder.heading("description",text="Description")
    treeOrder.heading("location",text="Location")
    treeOrder.place(x=560,y=100)
    
    def placement_page(): # the placement page
        cover = Label(text="             \n        \n ",bg="lightgrey",font=("times",160))
        cover.place(x=0,y=0)
        cover = Label(text="             \n        \n ",bg="lightgrey",font=("times",160))     # covers 
        cover.place(x=0,y=400)
        cover = Label(text="                            \n",bg="lightgrey",font=("times",40))
        cover.place(x=550,y=0)
        
        typeL = Label(text = "Placing Page",font=("times",35),bg="lightgrey",highlightbackground="lightgrey") #    
        typeL.place(x=550,y=10) 


        db_loc = [] # used to get the location
        db_compNames = [] # used for getting the company names
        db_used_loc = [] # used to get the locations used that are in the table

        def finding(unit_val):     # takes valu from 1-8 further down
            item_name = clicked_companyName.get()
            item_compID = compIDE.get()
            for i in range(0,5):  
                for j in range(0,4):
                    w.create_rectangle(10+(i*50),500+(j*50),60+(i*50),550+(j*50),fill="red")   # this all draws the grid
            for i in range(0,4):
                w.create_rectangle(10+(i*70),320,35+(i*70),480 )
                w.create_rectangle(10+(i*70),320,60+(i*70),480 )
            for i in range(0,len(db_used_loc)):
                db_used_loc.pop(0)
                  
            def grid_checkTest(blue_showCheck,stateIntoDB):    # this is to get the blue box 
                X_checkTest = int(blue_showCheck[0])
                Y_checkTest = int(blue_showCheck[1]) #gets the coords
                
                finding(unit_val)
                X_val = 10 +  ((int(X_checkTest-1)) * 50)
                Y_val = 650 - ((int(Y_checkTest-1)) * 50) #calculates the coords 
                
                w.create_rectangle(X_val, Y_val, X_val+50, Y_val+50, fill="blue") # draws the blue box
                
                global final_location
                final_location = str(unit_val) +str(X_checkTest)+ str(Y_checkTest)
                item_name = clicked_companyName.get()
                item_desc = clicked_productName.get()
                item_amount = itemAmountE.get()        #gets all the data ready to be entered into the database
                item_compID = compIDE.get()
                show_current_order = Label(text="Comapny name: " + item_name + "\n item description: " + item_desc + "\n Item amount: " + item_amount + "\n Location: " + final_location + "\n company ID: " + item_compID)
                show_current_order.place(x=100,y=720)

                def place_int_DB(state):  # placing into the DB
                    
                    mycursor = mydb.cursor()
                    mycursor.execute("select * from CompanyProducts")
                    records = mycursor.fetchall()
                    for row in records:                #gets the ID from company products table
                        if item_desc == row[1]:         
                            product = row[0]
                            limit = row[2]
                            
                    mycursor = mydb.cursor()
                    mycursor.execute("select * from CompanyList")
                    records = mycursor.fetchall()
                    for row in records:                           #gets the ID from company table
                        if item_name == row[1]:
                            CompName = row[0]

                            
                    final_location = str(unit_val) +str(X_checkTest)+ str(Y_checkTest)
                    treeOrder.insert('',0,text = "PLACING", values = (item_name,item_compID,item_desc,final_location))  # puts the order in the order list 
                    
                    if state == "NewLoc":   # if the location chosen was a new one this is for making a new field
                        mycursor = mydb.cursor()
                        add_data_Formula = "INSERT INTO Warehouse1 (Quantity,Stock_Location,comp_uniqueID,CompanyList_Company_Name_ID,CompanyProducts_CompanyProducts_ID,Users1_UserID) VALUES (%s,%s,%s,%s,%s,%s)"
                        add_data1 = (item_amount,final_location,item_compID,CompName,product,username_ID)    
                        mycursor.execute(add_data_Formula,add_data1)
                        mydb.commit()
                        
                    elif state == "Place": # If the location ws added to an existing location then this adds it to the current field
                        mycursor = mydb.cursor()
                        mycursor.execute("select * from Warehouse1")
                        records = mycursor.fetchall()
                        for row in records:
                            if row[2] == int(final_location):
                                newAmount = int(row[1]) +  int(item_amount)
                                if int(newAmount) >= int(limit):
                                    placement_page()
                                else:
                                    add_data_Formula = "UPDATE Warehouse1 SET Quantity = %s WHERE Stock_Location = %s"
                                    add_data1 = (newAmount,final_location)
                                    mycursor.execute(add_data_Formula,add_data1)
                                    mydb.commit()
                            else:
                                print("row doesnt exist")
                                
                    placement_page()
                    
                confirm_intoDB = Button(text="Confirm",command = lambda : place_int_DB(stateIntoDB),width=9,highlightbackground="lightgrey",bg="lightgrey",fg="red")
                confirm_intoDB.place(x=310,y=590)   #This is th ebutton to enter it into the   
                
            SameCompID = []
            for i in range (0,len(db_loc)):   # Goes through all the existing locations in the database
                loc_val = list(map(int, str(db_loc[i])))  
                if loc_val[0] == unit_val:  # uses the locations to see if there in thesame aisle 
                    used_loc = (str(loc_val[1])+str(loc_val[2]))
                    db_used_loc.append(int(used_loc))
                    X_val = 10 + ( (loc_val[1]-1) * 50)
                    Y_val = 650 - ((loc_val[2]-1) * 50)    # gets the coords
                    if db_compNames[i] == item_compID:     # Checks the locations on the same aisle if they share the same company id as the user input
                        w.create_rectangle(X_val, Y_val, X_val+50, Y_val+50, fill="green") 
                        SameCompID.append(int(used_loc)) 
                    else:
                        w.create_rectangle(X_val, Y_val, X_val+50, Y_val+50, fill="orange")
                        
            global addOrPlaceaddOrPlace
            
            def addOrPlace(state):    # Checks if the user wants a new bin location or existing
                
                sidebar_place = Scrollbar(window1)
                sidebar_place.place(x=400,y=390)
                box_place=Listbox(window1,height=10,width=10,yscrollcommand=sidebar_place.set)  # for the sidebar that shows the locations avaliable
                box_place.place(x=310,y=340)
                sidebar_place.config(command=box_place.yview)
                
                if state == "place":
                    for i in range(1,5):
                        for j in range(1,6):
                            used_loc_check = str(j) + str(i)     # gets the existing locations and puts it in the sidebar
                            if int(used_loc_check) in SameCompID   :
                                box_place.insert(END,used_loc_check)
                    addToDB_State = "Place"  # this statement used for the confrim order
                    
                elif state == "newLoc":
                    for i in range(1,5):
                        for j in range(1,6):
                            used_loc_check = str(j) + str(i)
                            if int(used_loc_check) not in db_used_loc:
                                box_place.insert(END,used_loc_check)
                    addToDB_State = "NewLoc" # this statement used for the confrim order
                     
                place_test = Button(text="Check",command = lambda: grid_checkTest(box_place.get(ANCHOR),addToDB_State) ,width=9,bg="lightgrey",highlightbackground="lightgrey",fg="red")
                place_test.place(x=310,y=540)  # when they select a location this will use the blue box to show the user the location
                
            addToExisting = Button(text="Add to existing",command = lambda:addOrPlace("place"))
            addToExisting.place(x=425,y=350)  
            addNewLoc = Button(text="Add new bin",command = lambda: addOrPlace("newLoc"))         # the two options for either adding to existing or getting new bin
            addNewLoc.place(x=425,y=390)
            
        def placement_confirm():  #  the first confrimation
            checktot = 0
            time.sleep(1)
            item_name = clicked_companyName.get()
            item_desc = clicked_productName.get()    # this gets all the inputs   
            item_amount = itemAmountE.get()
            item_compID = compIDE.get()
            if clicked_companyName.get() != "":
                checktot +=1
            if clicked_productName.get() != "":
                checktot +=1
            if itemAmountE.get() != "":             # this checks that none of them are empty
                checktot +=1
            if compIDE.get() != "":
                checktot +=1
            if checktot == 4:
                mycursor = mydb.cursor()
                sql_select_Query = "select * from Warehouse1"          # this gets all the data from hte sql database
                mycursor.execute(sql_select_Query)
                records = mycursor.fetchall()
                for row in records:
                    db_compNames.append(row[3])                 
                    db_loc.append(row[2])
                unit1 = Button(text="1",command = lambda: finding(1), bg = "darkgrey",highlightbackground="lightgrey")
                unit1.place(x=15,y=385)
                unit2 = Button(text="2",command = lambda: finding(2), bg = "darkgrey",highlightbackground="lightgrey")
                unit2.place(x=40,y=385)
                unit3 = Button(text="3",command= lambda:finding(3), bg = "darkgrey",highlightbackground="lightgrey")
                unit3.place(x=85,y=385)
                unit4 = Button(text="4",command= lambda:finding(4), bg = "darkgrey",highlightbackground="lightgrey")       # when any of the top 8 buttons are pressed
                unit4.place(x=110,y=385)                                                                                   # sends the value to finding defenition
                unit5 = Button(text="5",command= lambda:finding(5), bg = "darkgrey",highlightbackground="lightgrey")
                unit5.place(x=155,y=385)
                unit6 = Button(text="6",command= lambda:finding(6), bg = "darkgrey",highlightbackground="lightgrey")
                unit6.place(x=180,y=385)
                unit7 = Button(text="7",command= lambda:finding(7), bg = "darkgrey",highlightbackground="lightgrey")
                unit7.place(x=225,y=385)
                unit8 = Button(text="8",command= lambda:finding(8), bg = "darkgrey",highlightbackground="lightgrey")
                unit8.place(x=250,y=385)
            else:
                messagebox.showerror('Error','There are empty slots')

                
        w = Canvas( width=550, height=900, bg = "lightgrey",highlightbackground="lightgrey")        # to allow the grids to be drawn
        w.place(x=0,y=0)
        for i in range(0,4):
            w.create_rectangle(10+(i*70),320,35+(i*70),480 )
            w.create_rectangle(10+(i*70),320,60+(i*70),480 )                              # draws the grid
        for i in range(0,5):  
            for j in range(0,4):
                w.create_rectangle(10+(i*50),500+(j*50),60+(i*50),550+(j*50))  
        itemcompanyL = Label(text="Company Name:" , bg = "lightgrey",)
        itemcompanyL.place(x= 10, y=50)
        mycursor = mydb.cursor()                                        # uses lists fir the company name and product so no issue arrises
        mycursor.execute("select * from CompanyList")       
        records = mycursor.fetchall()
        Company_dropdown_list = []
        clicked_companyName = StringVar()
        for row in records:
            Company_dropdown_list.append(row[1])            # for the drop down list
        itemcompanyE = OptionMenu(window1,clicked_companyName,*Company_dropdown_list)    
        itemcompanyE.place(x=120,y=50)
        Product_dropdown_list = []
        clicked_productName = StringVar()
        mycursor = mydb.cursor()
        mycursor.execute("select * from CompanyProducts")
        records = mycursor.fetchall()
        for row in records:
            Product_dropdown_list.append(row[1])   
        itemContentL = Label(text="Description:" , bg = "lightgrey")
        itemContentL.place(x= 30, y=100)
        itemContentE = OptionMenu(window1,clicked_productName,*Product_dropdown_list)
        itemContentE.place(x=120,y=100)
        itemAmountL = Label(text="Quantity:", bg = "lightgrey")                         # for the description and quantity inputs
        itemAmountL.place(x= 30, y=150)
        itemAmountE = Entry(text="",highlightbackground="lightgrey")
        itemAmountE.place(x=120,y=150)
        compIDL = Label(text="Company ID:", bg = "lightgrey")
        compIDL.place(x= 22, y=200)
        compIDE = Entry(text="",highlightbackground="lightgrey")
        compIDE.place(x=120,y=200)
        confirmBox = Button(text="confirm",command = placement_confirm, bg = "lightgrey",highlightbackground="lightgrey",fg="red")
        confirmBox.place(x=30, y=250)
        clear = Button(text="clear", command = placement_page, bg = "lightgrey",highlightbackground="lightgrey",fg="red")
        clear.place(x=180, y=250)
#--------------------------------------------------------------------------------------------
    def finding_page():                 # start of the finding page 
        cover = Label(text="             \n        \n ",bg="lightgrey",font=("times",160))
        cover.place(x=0,y=0)
        cover = Label(text="             \n        \n ",bg="lightgrey",font=("times",160))
        cover.place(x=0,y=400)
        cover = Label(text="                            \n",bg="lightgrey",font=("times",40))                   # cover labels
        cover.place(x=550,y=0)
        typeL = Label(text = "Finding Page",font=("times",35),bg="lightgrey",highlightbackground="lightgrey")
        typeL.place(x=550,y=10)
        global grid_loc
        db_check = []
        db_grid_loc = []
        w = Canvas(width=550, height=800,bg="lightgrey",highlightbackground="lightgrey")
        w.place(x=0,y=50)
        for i in range(0,4):
            w.create_rectangle(10+(i*70),320,35+(i*70),480 )            # creates the grid
            w.create_rectangle(10+(i*70),320,60+(i*70),480 ) 
        for i in range(0,5):  
            for j in range(0,4):
                w.create_rectangle(10+(i*50),500+(j*50),60+(i*50),550+(j*50))
        class choices:   # this is the main class that is used for the finding page
            def __init__(self,stock_id,comp_name,comp_desc,compID):
                self._stock_id = stock_id
                self._comp_name = comp_name
                self._comp_desc = comp_desc# this has the details that the user inputs to use as a set of objects 
                self._comp_ID = compID
            def search_db(self):        # this helps filter the database for the inputs
                print(self._comp_name)
                ID = []
                comp_name = []
                desc = []
                comp_id = []
                ProductSearch = []      # puts any of the IDs from later in the program in the list
                compProductID = 0
                compProductID = 0
                notSearched = 0
                mycursor = mydb.cursor()
                sql_select_Query = "select * from CompanyList"
                mycursor.execute(sql_select_Query)
                records = mycursor.fetchall()
                for row in records:
                    if row[1] == self._comp_name:
                        compNameID = row[0]
                mycursor = mydb.cursor()
                sql_select_Query = "select * from CompanyProducts"  # this all checks each row in the database
                mycursor.execute(sql_select_Query)
                records = mycursor.fetchall()
                for row in records:
                    if row[1] == self._comp_desc:
                        compProductID = row[0]
                for i in range(0,len(db_check)):
                    db_check.pop(i)
                for i in range(0,len(db_grid_loc)):
                    db_grid_loc.pop(i)
                mycursor = mydb.cursor()
                sql_select_Query = "select * from Warehouse1"
                mycursor.execute(sql_select_Query)
                records = mycursor.fetchall()
                if len(self._stock_id) != 0:
                    for row in records:
                        if row[0] == int(self._stock_id):
                            ProductSearch.append(row[0])
                else:
                    notSearched += 1
                if len(self._comp_name) != 0: #and len(self._comp_desc) != 0:
                    for row in records:
                        if row[4] == compNameID: #and row[2] == self._comp_desc:
                            ProductSearch.append(row[0])        
                else:
                    notSearched += 1
                if len(self._comp_desc) != 0:
                    for row in records:
                        if row[5] == compProductID:
                            ProductSearch.append(row[0])
                else:
                    notSearched += 1
                if len(self._comp_ID) != 0:
                    for row in records:
                        if row[3] == self._comp_ID:
                            ProductSearch.append(row[0])# this is part of the filter algorithm, where it puts the relevant data in the top lists
                else:
                    notSearched += 1
                searched = (4-notSearched)
                final = []
                for i in range (0,len(ProductSearch)):
                    total = 0 
                    if ProductSearch[i] not in final:
                        for j in range (0,len(ProductSearch)):          # this is the final algorithm that puts all the filtered ones in the final list
                            if ProductSearch[i] == ProductSearch[j]:
                                total +=1
                        if total == searched:
                            final.append(ProductSearch[i])          
                if len(final) == 0:
                    messagebox.showerror('Error','There was nothing fitting the description')
                for i in range(0,len(final)):
                    mycursor = mydb.cursor()
                    sql_select_Query = "select * from Warehouse1"
                    mycursor.execute(sql_select_Query)
                    records = mycursor.fetchall()
                    for row in records:
                        if final[i] == row[0]:                              # this uses the final list and gets all the 
                            quantity = row[1]
                            compID = row[3]
                            location = row[2]
                            compNameID = row[4]
                            CompProductID = row[5]
                            ID = row[0]
                            mycursor = mydb.cursor()
                            sql_select_Query = "select * from CompanyList"
                            mycursor.execute(sql_select_Query)
                            records = mycursor.fetchall()
                            for row in records :
                                if row[0] == compNameID:
                                    compName = row[1]
                            mycursor = mydb.cursor()
                            sql_select_Query = "select * from CompanyProducts"
                            mycursor.execute(sql_select_Query)
                            records = mycursor.fetchall()
                            for row in records :
                                if row[0] == CompProductID:
                                    compProduct = row[1]
                            treeFinding.insert('',0,text = "FINDING", values = (ID,compName,compID,compProduct,location,quantity))
                            # this puts the data on the list

            def placing_on_grid(self):  # this places the chosen stock on the grid
                for i in range(0,4):
                    w.create_rectangle(10+(i*70),320,35+(i*70),480,fill="lightgrey" )
                    w.create_rectangle(35+(i*70),320,60+(i*70),480,fill="lightgrey" )
                for i in range(0,5):  
                    for j in range(0,4):
                        w.create_rectangle(10+(i*50),500+(j*50),60+(i*50),550+(j*50),fill="lightgrey")
                curItem = treeFinding.focus()
                selected = treeFinding.item(curItem)

                loc = selected["values"][4]
                loc = list(map(int, str(selected["values"][4])))
                X_val = 10 + ( (loc[1]-1) * 50)     # this calculates the 
                Y_val = 650 - ((loc[2]-1) * 50)
                Z_valb = loc[0] - 1
                if loc[0] % 2 == 0:
                    Z_val = ((Z_valb+1) / 2) - 1
                    w.create_rectangle(35+(Z_val*70),320,60+(Z_val*70),480,fill="green" )   
                else:
                    Z_val = ((Z_valb) / 2) 
                    w.create_rectangle(10+(Z_val*70),320,35+(Z_val*70),480,fill="green" )
                w.create_rectangle(X_val, Y_val, X_val + 50, Y_val + 50, fill="green")
        class change_quantity():    # this is a new class that uses the change amount objects
            def __init__(self,state,amount):
                self._state = state
                self._amount = amount
            def add_rem_quantity(self): # this class checks if the user wants to add or remove an amount and then updates the code
                curItem = treeFinding.focus()
                selected = treeFinding.item(curItem)
                stock_ID = selected["values"][0]
                product = selected["values"][3]
                quan_of_stock = selected["values"][5]                   
                mycursor = mydb.cursor()
                sql_select_Query = "select * from CompanyProducts"
                mycursor.execute(sql_select_Query)
                records = mycursor.fetchall()
                for row in records:
                    if row[1]==product:
                        stockLimit = row[2]
                if self._state == "add":
                    new_amount = int(quan_of_stock) + int(self._amount)
                    if new_amount <= stockLimit:
                        mycursor = mydb.cursor()
                        add_data_Formula = "UPDATE Warehouse1 SET Quantity = %s WHERE Stock_ID = %s"
                        add_data1 = (new_amount,stock_ID)
                        mycursor.execute(add_data_Formula,add_data1)
                        mydb.commit()
                        treeOrder.insert('',0,text = "ADD " + str(self._amount) , values = (selected["values"][1],selected["values"][2],selected["values"][3],selected["values"][4]))
                    else:
                        messagebox.showerror('Error','The quantity is to much')
                elif self._state == "remove":
                    new_amount = int(quan_of_stock) - int(self._amount)
                    if new_amount < 0:
                        messagebox.showerror('Error','there is not that many items in the chosen location')
                    elif new_amount == 0:
                        print("DELETING")
                        mycursor = mydb.cursor()
                        add_data_Formula = "DELETE FROM Warehouse1 WHERE Stock_ID = %s"
                        add_data1 = (stock_ID)
                        mycursor.execute(add_data_Formula,add_data1)
                        mydb.commit()
                        treeOrder.insert('',0,text = "REMOVE " + new_amount , values = (selected["values"][1],selected["values"][2],selected["values"][3],selected["values"][4]))
                    else:
                        mycursor = mydb.cursor()
                        add_data_Formula = "UPDATE Warehouse1 SET Quantity = %s WHERE Stock_ID = %s"
                        add_data1 = (new_amount,stock_ID)
                        mycursor.execute(add_data_Formula,add_data1)
                        mydb.commit()
                        treeOrder.insert('',0,text = "REMOVE " + str(new_amount) , values = (selected["values"][1],selected["values"][2],selected["values"][3],selected["values"][4]))
                finding_page()
        itemContentL = Label(text="Description:" , bg = "lightgrey")
        itemContentL.place(x= 20, y=122)
        Product_dropdown_list = []
        clicked_productName = StringVar()
        mycursor = mydb.cursor()
        mycursor.execute("select * from CompanyProducts")
        records = mycursor.fetchall()
        for row in records:
            Product_dropdown_list.append(row[1])
        itemContentE = OptionMenu(window1,clicked_productName,*Product_dropdown_list)
        itemContentE.place(x=105,y=120)
        check_ID_L = Label(text = "Stock ID:",bg="lightgrey")
        check_ID_L.place(x= 30, y=42)
        check_ID_E = Entry(text="",highlightbackground="lightgrey")
        check_ID_E.place(x=105,y=40)
        check_compName_L = Label(text = "Company name:",bg="lightgrey")
        check_compName_L.place(x= 0, y=82)                          # tgus us all the layout for the finding page
        mycursor = mydb.cursor()
        mycursor.execute("select * from CompanyList")
        records = mycursor.fetchall()
        Company_dropdown_list = []
        clicked_companyName = StringVar()
        for row in records:
            Company_dropdown_list.append(row[1])
            
        check_compName_E = OptionMenu(window1,clicked_companyName,*Company_dropdown_list)
        check_compName_E.place(x=105,y=80)
        check_CompID_L = Label(text = "Company ID:",bg="lightgrey")
        check_CompID_L.place(x= 20, y=162)
        check_CompID_E = Entry(text="",highlightbackground="lightgrey")
        check_CompID_E.place(x=105,y=160)
        treeFinding = ttk.Treeview(window1,height=5)
        treeFinding["columns"] = ("ID","company_Name","company_ID","description","location","quantity")
        treeFinding.column("#0",width=70,minwidth=25)
        treeFinding.column("ID",width=40,minwidth=25)
        treeFinding.column("company_Name",width=90,minwidth=25)
        treeFinding.column("company_ID",width=80,minwidth=25)               # this is the layout to show the stock that meets the inputted criteria
        treeFinding.column("description",width=80,minwidth=25)
        treeFinding.column("location",width=80,minwidth=25)
        treeFinding.column("quantity",width=80,minwidth=25)
        treeFinding.heading("#0", text = "Task")
        treeFinding.heading("ID", text = "ID")
        treeFinding.heading("company_Name", text = "Customer Name")
        treeFinding.heading("company_ID",text="Company ID")
        treeFinding.heading("description",text="Description")
        treeFinding.heading("location",text="Location")
        treeFinding.heading("quantity",text="Quantity")
        treeFinding.place(x=15,y=240)
        check_confirm = Button(text="Confirm",command = lambda: choices(check_ID_E.get(),clicked_companyName.get(),clicked_productName.get(),check_CompID_E.get() ).search_db(),bg="lightgrey",highlightbackground="lightgrey",fg = "red")
        check_confirm.place(x=105,y=210)
        check_onGrid = Button(text="Check",command = lambda: choices(check_ID_E.get(),clicked_companyName.get(),clicked_productName.get(),check_CompID_E.get()).placing_on_grid(),bg="lightgrey",highlightbackground="lightgrey",fg = "red")
        check_onGrid.place(x=320,y=380)
        add_rem_amount = Entry(text="",width=5)     # this is for the buttons that confirm the process and send the data to the classes
        add_rem_amount.place(x=320,y=420 )
        add_to_wh =Button(text="add",command = lambda: change_quantity("add",add_rem_amount.get()).add_rem_quantity(),bg="lightgrey",highlightbackground="lightgrey",fg = "red")
        add_to_wh.place(x=320,y=450 )
        rem_from_wh = Button(text="remove",command = lambda:change_quantity("remove",add_rem_amount.get()).add_rem_quantity(),bg="lightgrey",highlightbackground="lightgrey",fg = "red")
        rem_from_wh.place(x=320,y=480 )

    def locating_page(): # this is the locating page
        cover = Label(text="             \n        \n ",bg="lightgrey",font=("times",160))
        cover.place(x=0,y=0)
        cover = Label(text="             \n        \n ",bg="lightgrey",font=("times",160))
        cover.place(x=0,y=400)                                                                  # this covers up the pervious page contents
        cover = Label(text="                            \n",bg="lightgrey",font=("times",40))
        cover.place(x=550,y=0)
        typeL = Label(text = "Locating Page",font=("times",35),bg="lightgrey",highlightbackground="lightgrey")
        typeL.place(x=550,y=10)
        w = Canvas(width=525, height=800,bg="lightgrey",highlightbackground="lightgrey")        # this sets up the canvas for the grid
        w.place(x=0,y=20)
        LocatingList = ttk.Treeview(window1)
        LocatingList["columns"] = ("company_Name","company_ID","description","location")
        LocatingList.column("#0",width=70,minwidth=25)
        LocatingList.column("company_Name",width=90,minwidth=25)
        LocatingList.column("company_ID",width=80,minwidth=25)              # this sets the list up for the data to go from the order list to the current locating list
        LocatingList.column("description",width=80,minwidth=25)
        LocatingList.column("location",width=80,minwidth=25)
        LocatingList.heading("#0", text = "Task")
        LocatingList.heading("company_Name", text = "Customer Name")
        LocatingList.heading("company_ID",text="Company ID")
        LocatingList.heading("description",text="Description")
        LocatingList.heading("location",text="Location")
        LocatingList.place(x=65,y=420)
        gridLoc = []
        for j in range(0,4):
            for i in range(0,5):
                w.create_rectangle(55+(j*120),70+(i*30),85+(j*120),100+(i*30),fill="lightgrey") # cubes on left
                w.create_line(45+(j*120),85+(i*30),55+(j*120),85+(i*30),fill="lightgrey") # line of cube on left
                w.create_rectangle(85+(j*120),70+(i*30),115+(j*120),100+(i*30),fill="lightgrey") # cubes on right
                w.create_line(115+(j*120),85+(i*30),125+(j*120),85+(i*30),fill="lightgrey") # line of cube on right
                w.create_line(45+(j*120),240,125+(j*120),240,fill="lightgrey") # line across bottom long one
                w.create_line(5+(i*120),240,45+(i*120),240,fill="lightgrey") # line connecting others for shorter path at bottom
                w.create_line(5+(i*120),70,45+(i*120),70,fill="lightgrey") # line connecting others for shorter path on top
                w.create_line(45+(i*120),70,45+(i*120),240,fill="lightgrey") # line across y axis connecting all cubes on left
                w.create_line(5+(i*120),70,5+(i*120),240,fill="lightgrey") # line across y axis connecting all cubes on right
        def confirm_pathFinder():
            for j in range(0,4):
                for i in range(0,5):
                    w.create_rectangle(55+(j*120),70+(i*30),85+(j*120),100+(i*30),fill="lightgrey") # cubes on left
                    w.create_line(45+(j*120),85+(i*30),55+(j*120),85+(i*30),fill="lightgrey") # line of cube on left
                    w.create_rectangle(85+(j*120),70+(i*30),115+(j*120),100+(i*30),fill="lightgrey") # cubes on right
                    w.create_line(115+(j*120),85+(i*30),125+(j*120),85+(i*30),fill="lightgrey") # line of cube on right
                    w.create_line(45+(j*120),240,125+(j*120),240,fill="lightgrey") # line across bottom long one
                    w.create_line(5+(i*120),240,45+(i*120),240,fill="lightgrey") # line connecting others for shorter path at bottom
                    w.create_line(5+(i*120),70,45+(i*120),70,fill="lightgrey") # line connecting others for shorter path on top
                    w.create_line(45+(i*120),70,45+(i*120),240,fill="lightgrey") # line across y axis connecting all cubes on left
                    w.create_line(5+(i*120),70,5+(i*120),240,fill="lightgrey") # line across y axis connecting all cubes on right
            
            path1 = 0
            path2 = 0
            path3 = 0
            path4 = 0               # these variables are used to help the algorithm calculate the shortest route
            path5 = 0
            path6 = 0
            path7 = 0
            path8 = 0 
            def longOrShortPath(path,loc):
                if path > 0:
                    w.create_line(45+(loc*120),240,125+(loc*120),240,fill="red")
                    w.create_line(5+(loc*120),70,45+(loc*120),70,fill="red")            # thus us where the red lines get drawn
                    w.create_line(45+(loc*120),70,45+(loc*120),240,fill="red")
                    w.create_line(5+(loc*120),70,5+(loc*120),240,fill="red")
                else:
                    w.create_line(5+(loc*120),240,45+(loc*120),240,fill="red")
                    w.create_line(45+(loc*120),240,125+(loc*120),240,fill="red")
            for i in range(0,8):
                for j in range(0,len(gridLoc)):
                    check_path_loc = str(gridLoc[j])
                    which_box = int(check_path_loc[1]) - 1
                    if check_path_loc[0] == "1" :
                        path1 =+ 1
                        w.create_rectangle(55,70+(which_box*30),85,100+(which_box*30),fill="red")
                        w.create_line(45,85+(which_box*30),55,85+(which_box*30),fill= "red")
                    elif check_path_loc[0] == "2" :
                        path2 =+ 19 
                        w.create_rectangle(85,70+(which_box*30),115,100+(which_box*30),fill="red")
                        w.create_line(115,85+(which_box*30),125,85+(which_box*30),fill="red")
                    elif check_path_loc[0] == "3" :
                        path3 =+ 1
                        w.create_rectangle(175,70+(which_box*30),205,100+(which_box*30),fill="red")
                        w.create_line(175,85+(which_box*30),165,85+(which_box*30),fill="red")
                    elif check_path_loc[0] == "4" :
                        path4 =+ 1
                        w.create_rectangle(205,70+(which_box*30),235,100+(which_box*30),fill="red")    # these creates the highlighted box locations 
                        w.create_line(235,85+(which_box*30),245,85+(which_box*30),fill="red")
                    elif check_path_loc[0] == "5" :                                                         
                        path5 =+ 1
                        w.create_rectangle(295,70+(which_box*30),325,100+(which_box*30),fill="red")
                        w.create_line(285,85+(which_box*30),295,85+(which_box*30),fill="red")
                    elif check_path_loc[0] == "6" :
                        path6 =+ 1
                        w.create_rectangle(325,70+(which_box*30),355,100+(which_box*30),fill="red")
                        w.create_line(365,85+(which_box*30),355,85+(which_box*30),fill="red")
                    elif check_path_loc[0] == "7" :
                        path7 =+ 1
                        w.create_rectangle(415,70+(which_box*30),445,100+(which_box*30),fill="red")
                        w.create_line(415,85+(which_box*30),405,85+(which_box*30),fill="red")
                    elif check_path_loc[0] == "8" :
                        path8 =+ 1
                        w.create_rectangle(445,70+(which_box*30),475,100+(which_box*30),fill="red")
                        w.create_line(475,85+(which_box*30),485,85+(which_box*30),fill="red")
            longOrShortPath(path1,0)
            longOrShortPath(path2+path3,1)
            longOrShortPath(path4+path5,2)
            longOrShortPath(path6+path7,3)
            longOrShortPath(path8,4)
        def add_to_grid_loc ():
            curItem = treeOrder.focus()
            selected = treeOrder.item(curItem)      # this gets the order from the order list to the new list on the locating list
            treeOrder.delete(curItem)
            LocatingList.insert('',0,text = "Locate ", values = (selected["values"][0],selected["values"][1],selected["values"][2],selected["values"][3]))
            gridLoc.append(selected["values"][3])
        def empty_page():
            locating_page()
        show_path = Button(text = "Check Route", command = confirm_pathFinder,fg="red",font=('times', 28, 'italic') ,highlightbackground="lightgrey")   # confirms the rotue by using the locating defenition
        show_path.place(x=180,y=310)
        getOrder_from_to_do=Button(text="Get Orders",command=add_to_grid_loc,fg="red",font=('times', 28, 'italic'),highlightbackground="lightgrey")
        getOrder_from_to_do.place(x=20,y=310)
        confirm = Button(text="Confirm",command = empty_page,fg="red",font=('times', 28, 'italic'),highlightbackground="lightgrey") # confirm gets rid of the route shown
        confirm.place(x=360,y=310)
    def AdminPage():  # this is the admin page
        cover = Label(text="             \n        \n ",bg="lightgrey",font=("times",160))
        cover.place(x=0,y=0)
        cover = Label(text="             \n        \n ",bg="lightgrey",font=("times",160)) # this covers up anything else from the other pages
        cover.place(x=0,y=400)
        cover = Label(text="                            \n",bg="lightgrey",font=("times",40))
        cover.place(x=550,y=0)
        typeL = Label(text = "Locating Page",font=("times",35),bg="lightgrey",highlightbackground="lightgrey")
        typeL.place(x=550,y=10)
        
        class admin():  # this admin class holds the set up for the page and also has sub classes for the processes

            def buttons(self):
                self.addUserB = Button(text = "Add User",command= lambda: admin().addNewUser(),bg = "darkgrey",highlightbackground="lightgrey")
                self.addUserB.place(x=100,y=100)
                self.CheckStockB = Button(text = "Check Stock",command = lambda: admin().showLowStock(),bg = "darkgrey",highlightbackground="lightgrey")  # this is for the opions on the page
                self.CheckStockB.place(x=200,y=100)
                self.addCompB=Button(text="add company",command= lambda: admin().addCompanyWidgets(),bg = "darkgrey",highlightbackground="lightgrey")
                self.addCompB.place(x=100,y=150)
                self.addCompB=Button(text="add Product",command= lambda: admin().addProductWidgets(),bg = "darkgrey",highlightbackground="lightgrey")
                self.addCompB.place(x=200,y=150)

            def showLowStock(self):
                admin().cover()
                typeL = Label(text ="Show Stock",bg = "lightgrey",highlightbackground="lightgrey")
                typeL.place(x=200,y=220)
                self.showLowStock = ttk.Treeview(window1,height=15)
                self.showLowStock["columns"] = ("comapny_ID","amount_remaning")
                self.showLowStock.column("#0",width=100,minwidth=25)
                self.showLowStock.column("comapny_ID",width=100,minwidth=25)
                self.showLowStock.column("amount_remaning",width=100,minwidth=25)
                self.showLowStock.heading("#0", text = "stock_ID")
                self.showLowStock.heading("comapny_ID", text = "Comapny ID")                # if this option is picked, it shows all the stock that is low in the database
                self.showLowStock.heading("amount_remaning", text = "amount remaning")
                self.showLowStock.place(x=80,y=250)
                mycursor = mydb.cursor()
                mycursor.execute("select * from Warehouse1")
                records = mycursor.fetchall()
                for row in records:
                    if int(row[1]) < 40:
                        self.showLowStock.insert('',0,text = row[0], values = (row[3],row[1]))

            def addCompanyWidgets(self):
                admin().cover()
                typeL = Label(text ="Add Company",bg = "lightgrey",highlightbackground="lightgrey")
                typeL.place(x=200,y=220)
                companyNameL=Label(text="Company name:",bg = "lightgrey",highlightbackground="lightgrey")
                companyNameL.place(x=70,y=262)
                companyNameE=Entry(text="",highlightbackground="lightgrey")                 # this adds the widgets to enter the new company
                companyNameE.place(x=180,y=260)
                companyTypeL=Label(text="Company type:",bg = "lightgrey",highlightbackground="lightgrey")
                companyTypeL.place(x=70,y=292)
                companyTypeE=Entry(text="",highlightbackground="lightgrey")
                companyTypeE.place(x=180,y=290)
                enterToDatabase = Button(text="Enter",command = lambda: addToDatabase(companyNameE.get(),companyTypeE.get()).addCompanyToTable(companyNameE.get(),companyTypeE.get()),bg = "darkgrey",highlightbackground="lightgrey")
                enterToDatabase.place(x=200,y=325)      # this uses the sub class to add the company

            def addProductWidgets(self):
                admin().cover()
                typeL = Label(text ="Add Product",bg = "lightgrey",highlightbackground="lightgrey")
                typeL.place(x=200,y=220)
                productNameL=Label(text="Producr name:",bg = "lightgrey",highlightbackground="lightgrey")
                productNameL.place(x=70,y=262)
                productNameE=Entry(text="",highlightbackground="lightgrey")
                productNameE.place(x=180,y=260)
                productLimitL=Label(text="Product Limit:",bg = "lightgrey",highlightbackground="lightgrey")     # this adds the widgets to enter the new product
                productLimitL.place(x=70,y=292)
                productLimitE=Entry(text="",highlightbackground="lightgrey")
                productLimitE.place(x=180,y=290)
                enterToDatabase = Button(text="Enter",command = lambda: addToDatabase(productNameE.get(),productLimitE.get()).addProductToTable(productNameE.get(),productLimitE.get()),bg = "darkgrey",highlightbackground="lightgrey")
                enterToDatabase.place(x=200,y=325)# this uses the sub class to add the product

            def addNewUser(self):
                admin().cover()
                typeL = Label(text ="Add New User",bg = "lightgrey",highlightbackground="lightgrey")
                typeL.place(x=200,y=220)
                newUserL=Label(text="Username:",bg = "lightgrey",highlightbackground="lightgrey")
                newUserL.place(x=70,y=262)
                newUserE=Entry(text="",highlightbackground="lightgrey")                         # this adds the widgets to enter the new user
                newUserE.place(x=150,y=260)
                LastNameL=Label(text="Last Name:",bg = "lightgrey",highlightbackground="lightgrey")
                LastNameL.place(x=70,y=292)
                LastNameE=Entry(text="",highlightbackground="lightgrey")
                LastNameE.place(x=150,y=290)
                newPwL=Label(text="Password:",bg = "lightgrey",highlightbackground="lightgrey")
                newPwL.place(x=70,y=322)
                newPwE=Entry(text="",highlightbackground="lightgrey")
                newPwE.place(x=150,y=320)
                confirm = Button(text="confirm",command = lambda: addNewUsers(newUserE.get(),newPwE.get(),LastNameE.get()).addNewDetails(newUserE.get(),newPwE.get(),LastNameE.get()),bg = "lightgrey",highlightbackground="lightgrey")
                confirm.place(x=100,y=360)# this uses the sub class to add the new user
            def cover(self):
                grid_test_cover = Label(text="                \n               \n             \n            ",bg="lightgrey",font=("times",110))
                grid_test_cover.place(x=50,y=210)

        class addToDatabase(admin):         # this subclass adds the details to the new databse
            def __init__(self,Name,Type):
                self._Name = Name
                self._Type = Type
                
            def addCompanyToTable(self,Name,Type):          # this adds the new company to the databse
                if self._Name and self._Type != "":
                    mycursor = mydb.cursor()
                    add_data1 = (self._Name,self._Type)
                    sqlStatement = "INSERT INTO CompanyList (Company_Name,CompType) VALUES (%s,%s)"#.format(self._companyName)
                    mycursor.execute(sqlStatement,add_data1)
                    mydb.commit()
                    messagebox.showerror('Error','Details have been added')
                    admin().buttons()
                    admin().cover()

                else:
                    messagebox.showerror('Error','Not all entries have been filled')
            def addProductToTable(self,Name,Type):# this adds the new product to the databse
                print(Name)
                print(Type)
                if self._Name == "":
                    messagebox.showerror('Error','Not all entries have been filled')
                else:
                    mycursor = mydb.cursor()
                    add_data1 = (self._Name,self._Type)
                    sqlStatement = "INSERT INTO CompanyProducts (Company_product,product_limit) VALUES (%s,%s)"#.format(self._companyName)
                    mycursor.execute(sqlStatement,add_data1)
                    mydb.commit()
                    messagebox.showerror('Error','Details have been added')
                    admin().buttons()
                    admin().cover()
        class addNewUsers(admin):       # this adds the new user to the databse and the text file
            def __init__(self,username,password,lastName):
                self._username = username
                self._password = password
                self._lastName = lastName
            def addNewDetails(self,username,password,lastName): 
                print(type(self._username))
                if len(self._username) and len(self._password) and len(self._lastName) != 0:
                    mycursor = mydb.cursor()
                    mycursor.execute("select * from Users1")
                    records = mycursor.fetchall()
                    add_data_Formula = "INSERT INTO Users1 (First_Name,Last_name) VALUES (%s,%s)"
                    add_data1 = (self._username,self._lastName)
                    mycursor.execute(add_data_Formula,add_data1)
                    mydb.commit()
                    combine = str(self._username) + str(self._password)
                    print(combine)
                    file = open("new_file2.txt","a+")
                    file.write(str(("\n" +sha256(combine.encode()).hexdigest())))
                    file.close()
                    messagebox.showerror('Success','Details have been added')
                    admin().buttons()
                    admin().cover()
                else: 
                    messagebox.showerror('Error','Not all entries have been filled')   
        admin().buttons()
    cover_wrong_login_l = Label(text="             \n ",bg="lightgrey",font=("times",50))
    cover_wrong_login_l.place(x=350,y=420)
    cover_login = Label(text="             \n        \n ",bg="lightgrey",font=("times",160))
    cover_login.place(x=0,y=0)
    cover_login = Label(text="             \n        \n ",bg="lightgrey",font=("times",160))   
    placement = Button(text="Placement",command = lambda: placement_page(),highlightbackground="lightgrey",font=("times",30))
    placement.place(x=1160,y=120)
    finding = Button(text="Finding",command = lambda: finding_page(),highlightbackground="lightgrey",font=("times",30))         # this is for all the options on the page to be selected
    finding.place(x=1160,y=180)
    Location = Button(text="Locating ",command = lambda: locating_page(),highlightbackground="lightgrey",font=("times",30))
    Location.place(x=1160,y=240)
    Location = Button(text="Admin",command = lambda: AdminPage(),highlightbackground="lightgrey",font=("times",30))
    Location.place(x=1160,y=300)
def login_check():      # this is where the login gets checked
    cover_wrong_login_l = Label(text="             \n ",bg="lightgrey",font=("times",50))
    cover_wrong_login_l.place(x=350,y=420)
    username = username_entry.get()
    password = password_entry.get()
    combine = "no"
    mycursor = mydb.cursor()            
    sql_select_Query = "select * from Users1"
    mycursor.execute(sql_select_Query)
    records = mycursor.fetchall()
    login_count = 0
    time.sleep(0.5)
    for row in records:
        if username == row[1]:
            global username_ID
            username_ID = row[0]
            login_count += 1
            combine = str(username)+str(password)
    file = open("new_file2.txt","r")
    if str((sha256(combine.encode()).hexdigest())) in file.read():
        login_count += 1
    file.close()
    if login_count == 2:#2:
        cover_wrong_login_l = Label(text="             \n ",bg="white",font=("times",50))
        cover_wrong_login_l.place(x=350,y=420)
        cover_login = Label(text="             \n        \n ",bg="lightgrey",font=("times",167))
        cover_login.place(x=0,y=0)
        cover_login = Label(text="             \n        \n ",bg="lightgrey",font=("times",167))
        options_for_user()
        to_do_sidebar.place(x=640,y=390)
        to_do_box_place.place(x=560,y=100)
    else:
        messagebox.showerror('Error','Incorrect username or password')
        
username_label = Label(text="Username",width=9,height=1,bg="lightgrey",bd="2",highlightbackground="lightgrey")
username_label.place(x=275,y=300)
username_entry = Entry(text="",highlightbackground="lightgrey")
username_entry.place(x=360,y=298)
password_label = Label(text="Password",width=9,height=1,bg="lightgrey",highlightbackground="lightgrey")
password_label.place(x=275,y=340)
password_entry = Entry(text="",highlightbackground="lightgrey",show = "*")
password_entry.place(x=360,y=338)
login_confirm = Button(text="Confirm",command = login_check,highlightbackground="lightgrey")
login_confirm .place(x=330,y=380)  
 
