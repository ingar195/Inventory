import sqlite3
import re
import logging
connection = sqlite3.connect("Inventory.db")

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
    category VARCHAR(255));"""

    try:
        cursor.execute(sql_command)
    except:
        logging.error("initDB failed to execute")
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
    if db is not "Inventory":
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
            if query.lower() in (name+description+storelocation+barcode).lower():
                print("Itemnumber: {}, Name: {}, description: {}, storelocation: {}, stock: {}, minstock: {}, category: {}, barcode: {}, checkedoutby: {}, checkedoutdate: {}"
                      "".format(itemnumber, name, description, storelocation, stock, minstock, category, barcode, checkedoutby, checkedoutdate))

def sqlCommand(sql_command):
    try:
        cursor.execute(sql_command)
    except:
        logging.error("sqlCommand failed to execute")
    connection.commit()


def update(db, itemnumber, colum, value):
    sql_command = """UPDATE {} SET {} = '{}' WHERE itemnumber = {};"""
    try:
        cursor.execute(sql_command.format(db, colum, value, itemnumber))
    except:
        logging.error("update failed to execute")
    connection.commit()


def delete(db):
    inputval = input("Scan barcode or write name:\n")
    search(db, inputval)
    itemnumber = input("Enter item number you want to delete: ")
    sql_command = """DELETE FROM {} WHERE itemnumber = {};"""
    cursor.execute(sql_command.format(db, itemnumber))
    connection.commit()


def appendDB(table, name, description, storelocation, stock, minstock, barcode, category):
    sql_command = """INSERT INTO {} (itemnumber, name, description, storelocation, stock, minstock, barcode, category) VALUES (null,"{}","{}","{}","{}","{}","{}","{}");"""
    cursor.execute(sql_command.format(table, name, description, storelocation, stock, minstock, barcode, category))

    connection.commit()


def appendDBCategory(table, name):
    # Check if exist func
    sql_command = """INSERT INTO {} (itemnumber, name) VALUES (null,"{}");"""
    cursor.execute(sql_command.format(table, name))
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


def test(db):
    listAll(db)
    var = input("Select a number from the list for {} or write new: ".format(db))
    appendDBCategory(db, var)
    return var


def menu():
    print("""
    
Press S for search
Press A to add
Press U to update
Press C to checkout
Press L to list all items
Press D to delete a items
Press cat to goto category menu
Press Q to exit

    """)
    menuselection = input().lower()
    if menuselection == "s":
        searchphrase = input("Enter search phrase\n")
        search("Inventory", searchphrase)

    elif menuselection == "a":
        name = input("Enter name: ")
        description = input("Enter description: ")
        storelocation = test("Location")
        print(storelocation)
        stock = input("Enter stock: ")
        minstock = input("Enter min stock: ")
        barcode = input("Enter barcode (you can scan the barcode): ")

        category = test("Category")
        appendDB("Inventory", name, description, storelocation, stock, minstock, barcode, category)

    elif menuselection.isdigit():
        search("Inventory", menuselection)

    elif menuselection == "u":
        inputval = input("Scan barcode or write name:\n")
        search("Inventory", inputval)
        itenmnumber = input("Inventory number or R: ")
        # Add retry
        update("Inventory", itenmnumber, "stock", input("new Stock\n"))

    elif menuselection == "c":
        inputval = input("Scan barcode or write name:\n")
        search("Inventory", inputval)
        itenmnumber = input("Enter itenm number: ")
        value = input("Enter new value: ")
        update("Inventory", itenmnumber, "stock", value)

    elif menuselection == "d":
        delete("Inventory")

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

# gard was here
