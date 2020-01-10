import sqlite3
import re
import logging
from datetime import datetime

connection = sqlite3.connect("Inventory.db")

cursor = connection.cursor()


def initDB():
    initvar = ["""
    CREATE TABLE Inventory ( 
    itemnumber INTEGER PRIMARY KEY, 
    name VARCHAR(255), 
    description VARCHAR(255), 
    storelocation VARCHAR(255), 
    stock VARCHAR(255), 
    minstock VARCHAR(255), 
    barcode VARCHAR(255), 
    checkedoutby VARCHAR(255), 
    checkedoutdate VARCHAR(255),
    category VARCHAR(255)),
    Sublocation VARCHAR(255));""",
    """
    CREATE TABLE Category ( 
    itemnumber INTEGER PRIMARY KEY, 
    name VARCHAR(255));""",
    """
    CREATE TABLE Location ( 
    itemnumber INTEGER PRIMARY KEY, 
    name VARCHAR(255));""",
    """
    CREATE TABLE SubLocation ( 
    itemnumber INTEGER PRIMARY KEY, 
    name VARCHAR(255));"""]

    for item in initvar:
        sqlCommand(item)


def listAll(db):
    rows = sqlCommand('SELECT * FROM {}'.format(db))
    for row in rows:
        print(row)
    return rows


def search(db, query):
    print(" ") # For cleaner output
    rows = sqlCommand('SELECT * FROM {}'.format(db))
    if db != "Inventory":
        for row in rows:
            itemnumber = row[0]
            name = row[1]
            if re.search(query, name, re.IGNORECASE) is not None:
                print("Itemnumber: {}, Name: {}\n".format(itemnumber, name))
            else:
                return None

    else:
        for row in rows:
            itemnumber = row[0]
            name = row[1]
            description = row[2]
            storelocation = row[3]
            stock = row[4]
            minstock = row[5]
            barcode = row[6]
            checkedoutby = row[7]
            checkedoutdate = row[8]
            category = row[9]
            sublocation = row[10]
            if query.lower() in (name+description+storelocation+barcode+sublocation+category).lower():
                print("Itemnumber: {}, Name: {}, Description: {}, Store location: {}, Sub location: {}, Stock: {}, Min stock: {}, Category: {}, Barcode: {}, Checked out by: {}, Checked out date: {}\n"
                      "".format(itemnumber, name, description, storelocation, sublocation, stock, minstock, category, barcode, checkedoutby, checkedoutdate))
            else:
                return None

def sqlCommand(sql_command):
    try:
        cursor.execute(sql_command)
    except:
        logging.error("sqlCommand failed to execute: ")
    connection.commit()
    return cursor.fetchall()


def update(db, itemnumber, colum, value):
    sql_command = """UPDATE {} SET {} = '{}' WHERE itemnumber = {};"""
    sqlCommand(sql_command.format(db, colum, value, itemnumber))
 


def delete(db):
    inputval = input("Scan barcode or write name:\n")
    search(db, inputval)
    itemnumber = input("Enter item number you want to delete: ")
    sql_command = """DELETE FROM {} WHERE itemnumber = {};"""
    sqlCommand(sql_command.format(db, itemnumber))


def appendDB(table, name, description, storelocation, stock, minstock, barcode, category, sublocation):
    sql_command = """INSERT INTO {} (itemnumber, name, description, storelocation, stock, minstock, barcode, category, Sublocation) VALUES (null,"{}","{}","{}","{}","{}","{}","{}","{}");"""
    sqlCommand(sql_command.format(table, name, description, storelocation, stock, minstock, barcode, category, sublocation))


def appendDBCategory(table, name):
    sql_command = """INSERT INTO {} (itemnumber, name) VALUES (null,"{}");"""
    sqlCommand(sql_command.format(table, name))   


def checkMinStock(stock, minstock):
    try:
        minstock = int(minstock)
        stock = int(stock)
        if stock <= minstock:
            val = "Stock({}) is less than minstock({})".format(stock, minstock)
        else:
            val = "Stock({}) is more than minstock({})".format(stock, minstock)
        print("val = {}".format(val))
        return val
    except:
        logging.error("Cant convert string to int")
        return 


def locAndCatSelector(db):
    dbreturn = listAll(db)

    inputvar = input("Select a number from the list for {} or write new: ".format(db))
    try:
        inputvar = int(inputvar)
        for x in dbreturn:
            if str(x[0]) == str(inputvar):
                logging.debug("Input is found and a number")
                return x[1]
            else:
                logging.debug("Input are a number, but not found")
                pass
    except:
        print("else {}".format(inputvar))
        appendDBCategory(db, inputvar)
        return inputvar


def gettime():
    now = datetime.now() 
    logging.debug("now = {}".format(now))
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    logging.debug("date and time = {}".format(dt_string))	
    return dt_string
    

def SubMenu(name, db):
        while True:
            print("""
            
Press A to add
Press L to list all {}
Press D to delete a {}
Press Q to exit to main menu
Press enter to select
""".format(name, name))

            menuselection = input()
            if menuselection == "a":
                name = input("Enter {} name: ".format(name))
                appendDBCategory(db, name)
            elif menuselection == "l":
                listAll(db)
            elif menuselection == "d":
                delete(db)
            elif menuselection == "q":
                break
            else:
                continue


def menu():
    print("""
    
Press S for search
Press A to add
Press U to update
Press C to checkout
Press L to list all items
Press D to delete a items
Press cat to goto category menu
Press store to goto category menu
Press sub to goto category menu
Press Q to exit

    """)
    menuselection = input().lower()
    if menuselection == "s":
        searchphrase = input("Enter search phrase\n")
        search("Inventory", searchphrase)

    elif menuselection == "a":
        name = input("Enter name: ")
        if name != "":
            logging.debug("Name ins not none")
            description = input("Enter description: ")
            storelocation = locAndCatSelector("Location")
            substorelocation = locAndCatSelector("SubLocation")
            stock = input("Enter stock: ")
            minstock = input("Enter min stock: ")
            barcode = input("Enter barcode (you can scan the barcode): ")
            category = locAndCatSelector("Category")
            appendDB("Inventory", name, description, storelocation, stock, minstock, barcode, category, substorelocation)


    elif menuselection.isdigit():
        search("Inventory", menuselection)

    elif menuselection == "u":
        inputval = input("Scan barcode or write name:\n")
        search("Inventory", inputval)
        itenmnumber = input("Inventory number: ")
        update("Inventory", itenmnumber, "stock", input("new Stock\n"))

    elif menuselection == "c":
        inputval = input("Scan barcode or write name:\n")
        search("Inventory", inputval)        # TODO if no return from search 
        itenmnumber = input("Enter item number: ")
        # TODO print current stock
        value = input("Enter new value: ")
        # TODO check minstock
        #TODO add this to the database 
        checkoutname = input("Enter your name: ")
        update("Inventory", itenmnumber, "stock", value)

    elif menuselection == "d":
        delete("Inventory")

    elif menuselection == "cat":
        SubMenu("Category", "Category")

    elif menuselection == "store":
        SubMenu("Location", "Location")

    elif menuselection == "sub":
        SubMenu("Sub location", "SubLocation")

    elif menuselection == "l":
        search("Inventory", "")

    elif menuselection == "q":
        quit()

    else:
        print("Invalid")


if __name__ == '__main__':
    while True:
        menu()
    connection.close()
else:
    pass