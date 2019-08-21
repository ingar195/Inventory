import sqlite3
connection = sqlite3.connect("Inventory.db")

cursor = connection.cursor()


def initdb():
    # Check if db exists
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
    checkedoutdate VARCHAR(255));"""

    cursor.execute(sql_command)
    connection.commit()


def appeddb(table, name, description, storelocation, stock, minstock, barcode, checkedoutby, checkedoutdate):
    sql_command = """INSERT INTO {} (itemnumber, name, description, storelocation, stock, minstock, barcode, checkedoutby, checkedoutdate) VALUES (null,"{}","{}","{}","{}","{}","{}","{}","{}");"""
    print(" debug: " + sql_command.format(table, name, description, storelocation, stock, minstock, barcode, checkedoutby, checkedoutdate))
    cursor.execute(sql_command.format(table, name, description, storelocation, stock, minstock, barcode, checkedoutby, checkedoutdate))

    connection.commit()




#initdb()
print("123")
appeddb("Inventory", "Hammer", "Bighammer", "WorkShop_A3", "1", "0", "5000112637397", "Ingar", "2019-08-21")
print("321")
connection.close()