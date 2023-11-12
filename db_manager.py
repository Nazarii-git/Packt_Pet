import sqlite3
import datetime

def get_db_connection():
    conn = sqlite3.connect('database_full.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def close_db_connection(conn):
    conn.commit()
    conn.close()

def check_if_table_exist(table_name):
    conn = get_db_connection()
    test = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,)).fetchall()
    close_db_connection(conn)
    if test == []:
        create_db()
    return True



# In progress area
#
#

def upd_missed_dates(db_array):
    conn = get_db_connection()

    if len(db_array) == 0:
        delta_days = 366
    else:
        delta_days =  (datetime.datetime.now().date() - datetime.datetime.strptime(db_array[-1][1], '%Y-%m-%d').date()).days
    if delta_days>0:
        print("need to insert days ", delta_days)
        for i in range(delta_days, -1 , -1):
            conn.cursor().execute("INSERT INTO days (date) VALUES (?)",
                (datetime.date.today()-datetime.timedelta(days=i),))
        close_db_connection(conn)
    elif delta_days<0:
        print("DB mistake, need rebuild")
    else:
        print("DB looks fine!")

def get_days_array():
    days_array = []
    conn = get_db_connection()
    if check_if_table_exist('days'):
        my_history = conn.execute('SELECT * FROM days').fetchall()
        upd_missed_dates(my_history, conn)


#
#
#
#








def create_db():
    connection = get_db_connection()

    with open('schema.sql') as f:
        test = connection.executescript(f.read())
        print(test)

    close_db_connection(connection)


