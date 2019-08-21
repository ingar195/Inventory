import sqlite3
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
    return rows


def search(db, query):
    if query.isdigit():
        for row in cursor.execute("SELECT itemnumber,barcode FROM {} WHERE name MATCH '%{}%';".format(db, query)):
            print(row)
    else:
        for row in cursor.execute("SELECT itemnumber,name FROM {} WHERE name LIKE '%{}%';".format(db, query)):
            print(row)

    # print(cursor.execute(sql_command.format(db, query)))
    # cursor.fetchall(sql_command.format(db, query))
    # cursor.
    # cursor.execute('SELECT * FROM {}'.format(db))
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row[2])
    #     print(row[6])
    #     rows
    #     # tuple


def update(db, itemnumber, colum, value):
    sql_command = """UPDATE {} SET {} = '{}' WHERE itemnumber = {};"""
    cursor.execute(sql_command.format(db, colum, value, itemnumber))
    connection.commit()

def delete(db, itemnumber):
    sql_command = """DELETE FROM {} WHERE itemnumber = {};"""
    cursor.execute(sql_command.format(db, itemnumber))
    connection.commit()


def appendDB(table, name, description, storelocation, stock, minstock, barcode, checkedoutby, checkedoutdate, category):
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

# delete("Inventory", 5)
# update("Inventory", 2, "stock", "4")

#listTables()
search("Inventory", "ammer")
print("321")
connection.close()
