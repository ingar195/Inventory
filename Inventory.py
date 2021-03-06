import sqlite3
import re
import logging
import os

DBFile = "Inventory.db"
DBExist = os.path.exists(DBFile)

connection = sqlite3.connect(DBFile)
cursor = connection.cursor()


def listTables():
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    except:
        logging.error("listTables execute failed")
    print(cursor.fetchall())
    return cursor.fetchall()


def listColums(table):
    try:
        cursor.execute("""PRAGMA table_info('{}');""".format(table))
    except:
        logging.error("listColums execute failed")
    print(cursor.fetchall())
    return cursor


def initDB():
    # Check if table exists
    sql_command = """
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
    category VARCHAR(255),
    Sublocation VARCHAR(255));"""

    cursor.execute(sql_command)

    connection.commit()

    sql_command = """
    CREATE TABLE Category ( 
    itemnumber INTEGER PRIMARY KEY, 
    name VARCHAR(255));"""

    try:
        cursor.execute(sql_command)
    except:
        logging.error("initdb failed to execute command 2")
    connection.commit()

    sql_command = """
    CREATE TABLE Location ( 
    itemnumber INTEGER PRIMARY KEY, 
    name VARCHAR(255));"""
    try:
        cursor.execute(sql_command)
    except:
        logging.error("initdb failed to execute command 3")
    connection.commit()

    sql_command = """
    CREATE TABLE SubLocation ( 
    itemnumber INTEGER PRIMARY KEY, 
    name VARCHAR(255));"""
    try:
        cursor.execute(sql_command)
    except:
        logging.error("initdb failed to execute command 4")
    connection.commit()


def listAll(db):
    try:
        cursor.execute('SELECT * FROM {}'.format(db))
    except:
        logging.error("listAll failed to execute")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return rows


def search(db, query):
    try:
        cursor.execute('SELECT * FROM {}'.format(db))
    except:
        logging.error("search failed to execute")
    rows = cursor.fetchall()
    if db != "Inventory":
        for row in rows:
            itemnumber = row[0]
            name = row[1]
            if re.search(query, name, re.IGNORECASE) is not None:
                print("Itemnumber: {}, Name: {}".format(itemnumber, name))

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
                print("Itemnumber: {}, Name: {}, Description: {}, Store location: {}, Sub location: {}, Stock: {}, Min stock: {}, Category: {}, Barcode: {}, Checked out by: {}, Checked out date: {}"
                      "".format(itemnumber, name, description, storelocation, sublocation, stock, minstock, category, barcode, checkedoutby, checkedoutdate))
    return rows

def sqlCommand(sql_command):
    try:
        cursor.execute(sql_command)
    except:
        logging.error("sqlCommand failed to execute")
    connection.commit()


def update(db, itemnumber, colum, value):
    if value != "":        
        sql_command = """UPDATE {} SET {} = '{}' WHERE itemnumber = {};"""
        try:
            cursor.execute(sql_command.format(db, colum, value, itemnumber))
        except:
            logging.error("update failed to execute")
        connection.commit()


def delete(db):
    #if in inventory
    inputval = input("Scan barcode or write name:\n")
    skip = False
    if db != "Inventory":
        print("Search =")
        for item in search("Inventory", db):
            print(item)
            if db in item:
                skip = True
                break            
        if not skip:
            search(db, inputval)
            itemnumber = input("Enter item number you want to delete: ")
            sql_command = """DELETE FROM {} WHERE itemnumber = {};"""
            try:
                cursor.execute(sql_command.format(db, itemnumber))
            except:
                logging.error("delete failed to execute")
            connection.commit()
        else:
            print("{} is in use can not delete".format(db))


def appendDB(table, name, description, storelocation, stock, minstock, barcode, category, sublocation):
    if name.lower() != "q" and description.lower() != "q" and storelocation.lower() != "q" and stock.lower() != "q" and minstock.lower() != "q" and barcode.lower() != "q" and category.lower() != "q" and sublocation.lower() != "q": 
        sql_command = """INSERT INTO {} (itemnumber, name, description, storelocation, stock, minstock, barcode, category, Sublocation) VALUES (null,"{}","{}","{}","{}","{}","{}","{}","{}");"""
        try:
            cursor.execute(sql_command.format(table, name, description, storelocation, stock, minstock, barcode, category, sublocation))
        except:
            logging.error("appendDB failed to execute")

        connection.commit()


def appendDBCategory(table, name):
    # Check if exist func
    sql_command = """INSERT INTO {} (itemnumber, name) VALUES (null,"{}");"""
    try:
        cursor.execute(sql_command.format(table, name))
    except:
        logging.error("appendDBCategory failed to execute")
    connection.commit()


def checkMinStock(stock, minstock):
    minstock = int(minstock)
    stock = int(stock)
    if stock <= minstock:
        val = "Stock({}) is less than minstock({})".format(stock, minstock)
    else:
        val = "Stock({}) is more than minstock({})".format(stock, minstock)
    print("val = {}".format(val))
    return val


def SelectorCreator(db):
    dbreturn = listAll(db)

    var = input("Select a number from the list for {} or write new: ".format(db))
    if var != "" and var.lower() != "q":
        try:
            var = int(var)
            for x in dbreturn:
                if str(x[0]) == str(var):
                    return x[1]
        except:
            logging.debug("Created {}".format(var))
            appendDBCategory(db, var)
            return var


def menu():
    print("""
Press A to add
Press C to checkout
Press E to edit
Press D to delete a items
Press L to list all items  
Press S for search
Press U to update

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
            description = input("Enter description: ")
            storelocation = str(SelectorCreator("Location"))
            substorelocation = str(SelectorCreator("SubLocation"))
            stock = input("Enter stock: ")
            minstock = input("Enter min stock: ")
            barcode = input("Enter barcode (you can scan the barcode): ")

            category = str(SelectorCreator("Category"))
            appendDB("Inventory", name, description, storelocation, stock, minstock, barcode, category, substorelocation)

    elif menuselection.isdigit():
        search("Inventory", menuselection)

    elif menuselection == "u":
        inputval = input("Scan barcode or write name:\n")
        search("Inventory", inputval)
        itemnumber = input("Inventory number or R: ")
        # Add retry
        update("Inventory", itemnumber, "stock", input("new Stock\n"))

    elif menuselection == "c":
        inputval = input("Scan barcode or write name:\n")
        search("Inventory", inputval)
        itemnumber = input("Enter item number: ")
        value = input("Enter new value: ")
        update("Inventory", itemnumber, "stock", value)

    elif menuselection == "d":
        delete("Inventory")

    elif menuselection == "e":
        inputval = input("Scan barcode or write name:\n")
        search("Inventory", inputval)
        itemnumber = input("Enter item number: ")
        # Add retry
        update("Inventory", itemnumber, "name", input("new name\n"))
        update("Inventory", itemnumber, "description", input("new description\n"))
        update("Inventory", itemnumber, "minstock", input("new minstock\n"))

    elif menuselection == "cat":
        while True:
            print("""
            
Press A to add
Press L to list all categories
Press D to delete a categories
Press Q to exit to main menu
Press enter to select

""")
            menuselection = input()
            if menuselection == "a":
                name = input("Enter Category name: ")
                appendDBCategory("Category", name)
            elif menuselection == "l":
                listAll("Category")
            elif menuselection == "d":
                delete("Category")
            elif menuselection == "q":
                break
            else:
                continue


    elif menuselection == "store":
        while True:
            print("""
            
Press A to add
Press L to list all store location
Press D to delete a store location
Press Q to exit to main menu
Press enter to select

""")
            menuselection = input()
            if menuselection == "a":
                name = input("Enter Location name: ")
                appendDBCategory("Location", name)
            elif menuselection == "l":
                listAll("Location")
            elif menuselection == "d":
                delete("Location")
            elif menuselection == "q":
                break
            else:
                continue

    elif menuselection == "sub":
        while True:
            print("""l
            
Press A to add
Press L to list all Sub location
Press D to delete a Sub location
Press Q to exit to main menu
Press enter to select

""")
            menuselection = input()
            if menuselection == "a":
                name = input("Enter Sub location name: ")
                appendDBCategory("SubLocation", name)
            elif menuselection == "l":
                listAll("SubLocation")
            elif menuselection == "d":
                delete("SubLocation")
            elif menuselection == "q":
                break
            else:
                continue

    elif menuselection == "l":
        search("Inventory", "")

    elif menuselection == "q":
        quit()

    else:
        print("Invalid")


if __name__ == '__main__':
    if not DBExist:
        initDB()
    while True:
        menu()
    connection.close()
else:
    pass

# gard was here
