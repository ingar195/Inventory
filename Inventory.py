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
    checkedoutdate VARCHAR(255),
    category VARCHAR(255);"""

    cursor.execute(sql_command)
    connection.commit()
def checkifexist(dbname, query):
    print("todo")

def search(db, query):
    print("todo")


def delete(db, itemnumber):
    sql_command = """DELETE FROM {} WHERE itemnumber = {};"""
    cursor.execute(sql_command.format(db, itemnumber))
    connection.commit()


def appeddb(table, name, description, storelocation, stock, minstock, barcode, checkedoutby, checkedoutdate, category):
    # Check if exist func
    sql_command = """INSERT INTO {} (itemnumber, name, description, storelocation, stock, minstock, barcode, checkedoutby, checkedoutdate, category) VALUES (null,"{}","{}","{}","{}","{}","{}","{}","{}","{}");"""
    print(" debug: " + sql_command.format(table, name, description, storelocation, stock, minstock, barcode, checkedoutby, checkedoutdate, category))
    cursor.execute(sql_command.format(table, name, description, storelocation, stock, minstock, barcode, checkedoutby, checkedoutdate, category))

    connection.commit()


# initdb()
print("123")

# appeddb("Inventory", "Hammer", "Bighammer", "WorkShop_A3", "1", "0", "5000112637397", "Ingar", "2019-08-21", "Hand tools") # cola
# appeddb("Inventory", "Helmet", "protective helmet", "WorkShop_P1", "5", "2", "7025150014106", "Ingar", "2019-08-21", "Hand tools") #eplejuce
# appeddb("Inventory", "M5", "M5 hex 25mm", "WorkShop_S1", "73", "10", "", "", "2019-08-21", "Skrews")

delete("Inventory", 5)
print("321")
connection.close()
