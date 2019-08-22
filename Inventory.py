import sqlite3
import re
from datetime import date

connection = sqlite3.connect("Inventory.db")

cursor = connection.cursor()


def listTables():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())
    return cursor.fetchall()


def listColums(table):
    cursor.execute("""PRAGMA table_info('{}');""".format(table))
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
    category VARCHAR(255);"""

    cursor.execute(sql_command)
    connection.commit()


def checkTfExist(dbname, query):
    print("todo")


def listAll(db):
    cursor.execute('SELECT * FROM {}'.format(db))
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    # return rows


def search(db, query):
    cursor.execute('SELECT * FROM {}'.format(db))
    rows = cursor.fetchall()

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

        if query.isdigit():
            if query == barcode:
                print("Itemnumber: {}, Name: {}, description: {}, storelocation: {}, stock: {}, minstock: {}, category: {}, barcode: {}, checkedoutby: {}, checkedoutdate: {}\n"
                      "".format(itemnumber, name, description, storelocation, stock, minstock, category, barcode, checkedoutby, checkedoutdate))
                # returnval = checkMinStock(stock, minstock)
            else:
                print("")
        else:
            if re.search(query, name, re.IGNORECASE) is not None:
                print("Itemnumber: {}, Name: {}, description: {}, storelocation: {}, stock: {}, minstock: {}, category: {}, barcode: {}, checkedoutby: {}, checkedoutdate: {}"
                      "".format(itemnumber, name, description, storelocation, stock, minstock, category, barcode, checkedoutby, checkedoutdate))
                 # returnval = checkMinStock(stock, minstock)
    # return returnval



def update(db, itemnumber, colum, value):
    sql_command = """UPDATE {} SET {} = '{}' WHERE itemnumber = {};"""
    cursor.execute(sql_command.format(db, colum, value, itemnumber))
    connection.commit()


def delete(db, itemnumber):
    sql_command = """DELETE FROM {} WHERE itemnumber = {};"""
    cursor.execute(sql_command.format(db, itemnumber))
    connection.commit()


def appendDB(table, name, description, storelocation, stock, minstock, barcode, category):
    # Check if exist func
    sql_command = """INSERT INTO {} (itemnumber, name, description, storelocation, stock, minstock, barcode, category) VALUES (null,"{}","{}","{}","{}","{}","{}","{}");"""
    # print(" debug: " + sql_command.format(table, name, description, storelocation, stock, minstock, barcode, category))
    cursor.execute(sql_command.format(table, name, description, storelocation, stock, minstock, barcode, category))

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


def menu():
    print("\n"
          "Press S for search\n"
          "Press A to add\n"
          "Press U to update\n"
          "Press C to checkout\n"
          "Press L to list all items\n"
          "Press D to delete a items\n"
          "Press enter to select"
    )
    menuselection = input()
    if menuselection == "s":
        searchphrase = input("Enter search phrase\n")
        search("Inventory", searchphrase)

    elif menuselection == "a":
        name = input("Enter name: ")
        description = input("Enter description: ")
        storelocation = input("Enter store location: ")
        stock = input("Enter stock: ")
        minstock = input("Enter min stock: ")
        barcode = input("Enter barcode (you can scan the barcode): ")
        # checkedoutby = input("Enter the name that checked out the item ")
        # checkedoutdate = date.today()
        category = input("Enter Category: ")
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
        inputval = input("Scan barcode or write name:\n")
        search("Inventory", inputval)
        itenmnumber = input("Enter item number you want to delete: ")
        delete("Inventory", itenmnumber)
        # update 2 things at same tine

    elif menuselection == "l":
        search("Inventory", "")
    else:
        print("Invalid")


# listTables()


while True:
    menu()
connection.close()




# get store lokations ?
