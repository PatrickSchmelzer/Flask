import json
import sqlite3
import sys

db = []

def openConnection():
    database = r"C:\98_GitRepo\Flask\taskListDB.b.db"
    connection = None
    try:
        connection = sqlite3.connect(database)
    except Error as e:
        print(e,file=sys.stderr)
    return connection

def closeConnection(connection):
    connection.commit()
    connection.close()

def load_db():
    global db
    connection = openConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT * from tasks")
    db = []
    while True:
        row = cursor.fetchone()
        if row == None:
            break;
        print(row[0], row[1], row[2], file=sys.stdout)
        task = {"titel": row[0], "contact": row[1], "description": row[2]}
        db.append(task)
    closeConnection(connection)

def insertTask(task):
    global db
    connection = openConnection()
    cursor = connection.cursor()
    sql = "INSERT INTO Tasks VALUES(?,?,?)"
    cursor.execute(sql, (task['titel'], task['contact'], task['description']))
    closeConnection(connection)
    db.clear()
    load_db()

def deleteTask(index):
    global db
    taskToDelete = db[index]
    connection = openConnection()
    cursor = connection.cursor()
    sql = 'DELETE FROM tasks WHERE task_titel=?'
    cursor.execute(sql, (taskToDelete['titel'],))
    closeConnection(connection)
    db.clear()
    load_db()

load_db()
