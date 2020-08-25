import json
import sqlite3
import sys

db = []

def openConnection():
    database = r"C:\98_GitRepo\Flask\DataBase.db"
    connection = None
    try:
        connection = sqlite3.connect(database)
    except Error as e:
        print(e,file=sys.stderr)
    return connection

def closeConnection(connection):
    connection.commit()
    connection.close()

def loadTasks():
    global db
    connection = openConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT * from Tasks")
    db = []
    while True:
        row = cursor.fetchone()
        if row == None:
            break;
        print(row[0], row[1], row[2], row[3], row[4], file=sys.stdout)
        task = {"id": row[0], "titel": row[1], "contact": row[2], "description": row[3], "priorityId": row[4]}
        db.append(task)
    closeConnection(connection)

def insertTask(task):
    global db
    connection = openConnection()
    cursor = connection.cursor()
    sql = "INSERT INTO Tasks(titel, contact, description, priorityId) VALUES(?,?,?,?)"
    cursor.execute(sql, (task['titel'], task['contact'], task['description'], len(db)))
    closeConnection(connection)
    db.clear()
    loadTasks()

def deleteTask(index):
    global db
    taskToDelete = db[index]
    connection = openConnection()
    cursor = connection.cursor()
    sql = 'DELETE FROM tasks WHERE id=?'
    cursor.execute(sql, (taskToDelete['id'],))
    closeConnection(connection)
    db.clear()
    loadTasks()

def updateTask(task, id):
    global db
    connection = openConnection()
    cursor = connection.cursor()
    sql = 'UPDATE tasks SET titel = ?, contact = ?, description = ? WHERE id = ?'
    print(task, file=sys.stdout)
    cursor.execute(sql, (task['titel'], task['contact'], task['description'], id))
    closeConnection(connection)
    db.clear()
    loadTasks()

loadTasks()
