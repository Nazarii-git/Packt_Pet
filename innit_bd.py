import sqlite3

def create_db():
    connection = sqlite3.connect('database_full.db')

    with open('schema.sql') as f:
        test = connection.executescript(f.read())
        print(test)

    connection.commit()
    connection.close()

