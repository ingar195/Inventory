import sqlite3
import re
import code128
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
    category VARCHAR(255));"""

    cursor.execute(sql_command)
    connection.commit()

    sql_command = """
    CREATE TABLE Category ( 
    itemnumber INTEGER PRIMARY KEY, 
    name VARCHAR(255));"""

    cursor.execute(sql_command)
    connection.commit()

    sql_command = """
    CREATE TABLE Location ( 
    itemnumber INTEGER PRIMARY KEY, 
    name VARCHAR(255));"""

    cursor.execute(sql_command)
    connection.commit()


def listAll(db):
    cursor.execute('SELECT * FROM {}'.format(db))
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return rows


def search(db, query):
    cursor.execute('SELECT * FROM {}'.format(db))
    rows = cursor.fetchall()
    if db is not "Inventory":
        for row in rows:
            itemnumber = row[0]
            name = row[1]
            if re.search(query, name, re.IGNORECASE) is not None:
                print(
                    "Itemnumber: {}, Name: {}".format(itemnumber, name))

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

            # if query.isdigit():
            #     if query == barcode:
            #         print("Itemnumber: {}, Name: {}, description: {}, storelocation: {}, stock: {}, minstock: {}, category: {}, barcode: {}, checkedoutby: {}, checkedoutdate: {}\n"
            #               "".format(itemnumber, name, description, storelocation, stock, minstock, category, barcode, checkedoutby, checkedoutdate))
            #         # returnval = checkMinStock(stock, minstock)
            #     else:
            #         print("")
            # else:
            if re.search(query, name, re.IGNORECASE) is not None or re.search(query, description, re.IGNORECASE) is not None or re.search(query, category, re.IGNORECASE) is not None or re.search(query, barcode, re.IGNORECASE) is not None:
                print("Itemnumber: {}, Name: {}, description: {}, storelocation: {}, stock: {}, minstock: {}, category: {}, barcode: {}, checkedoutby: {}, checkedoutdate: {}"
                      "".format(itemnumber, name, description, storelocation, stock, minstock, category, barcode, checkedoutby, checkedoutdate))

def sqlCommand(sql_command):
    cursor.execute(sql_command)
    connection.commit()


def update(db, itemnumber, colum, value):
    sql_command = """UPDATE {} SET {} = '{}' WHERE itemnumber = {};"""
    cursor.execute(sql_command.format(db, colum, value, itemnumber))
    connection.commit()


def delete(db):
    inputval = input("Scan barcode or write name:\n")
    search(db, inputval)
    itemnumber = input("Enter item number you want to delete: ")
    sql_command = """DELETE FROM {} WHERE itemnumber = {};"""
    cursor.execute(sql_command.format(db, itemnumber))
    connection.commit()


def appendDB(table, name, description, storelocation, stock, minstock, barcode, category):
    if category.isdigit():
        print("")
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


def categoryMenu():
    while True:
        print("\n"
              "Press A to add\n"
              "Press L to list all categories\n"
              "Press D to delete a categories\n"
              "Press enter to select"
        )
        menuselection = input()
        if menuselection == "a":
            name = input("Enter Category name: ")
            appendDBCategory("Category", name)
        elif menuselection == "l":
            listAll("Category")
        elif menuselection == "d":
            delete("Category")
        else:
            menu()


def test(db):
    listAll(db)
    var = input("Select a number from the list for {} or write new: ".format(db))
    if var.isdigit():
        rows = listAll(db)
        for row in rows:
            if row[0] == int(var):
                var2 = row[1]
            else:
                print("row[0]{} == category:{}".format(row[0], var))
    else:
        var2 = var
        appendDBCategory(db, var2)
    return var2


def barcodeGenerator():
    print("barcode")
    code128.image("Hello World").save("Hello World.png")  # with PIL present


def menu():
    print("\n"
          "Press S for search\n"
          "Press A to add\n"
          "Press U to update\n"
          "Press C to checkout\n"
          "Press L to list all items\n"
          "Press D to delete a items\n"
          "Press cat to goto category menu\n"
          "Press enter to select"
    )
    menuselection = input()
    if menuselection == "s":
        searchphrase = input("Enter search phrase\n")
        search("Inventory", searchphrase)

    elif menuselection == "a":
        name = input("Enter name: ")
        description = input("Enter description: ")
        storelocation = test("Location")
        print("123 {}".format(storelocation))
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
        categoryMenu()

    elif menuselection == "l":
        search("Inventory", "")

    else:
        print("Invalid")


while True:
    menu()
connection.close()

# gard was here
