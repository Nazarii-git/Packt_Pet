import random
import sqlite3
import datetime

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()


for i in range(366):
    cur.execute("INSERT INTO days (date, raiting) VALUES (?, ?)",
                (datetime.date.today()-datetime.timedelta(days=i), random.randint(0,4))
                )

connection.commit()
connection.close()