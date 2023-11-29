import sqlite3
import datetime
from uuid import uuid4
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
        print('No DB was found')
        create_db()
    return True



# Can be better
#
#

def upd_missed_dates():
    conn = get_db_connection()
    db_array = conn.execute('SELECT * FROM DailyLogs').fetchall()
    if len(db_array) == 0:
        delta_days = 366
        print("DailyLogs is empty")
    else:
        delta_days = (datetime.datetime.now().date() - datetime.datetime.strptime(db_array[-1][2], '%Y-%m-%d').date()).days
    if delta_days>0:
        print("Need to insert days ", delta_days)
        for i in range(delta_days, -1 , -1):
            conn.cursor().execute("INSERT INTO DailyLogs (LogID, Date) VALUES (?, ?)",
                (str(uuid4()), datetime.date.today()-datetime.timedelta(days=i)))
    elif delta_days<0:
        print("DB mistake, need rebuild")
    else:
        print("DB looks fine!")
    db_array = conn.execute('SELECT * FROM DailyLogs').fetchall()
    close_db_connection(conn)
    return db_array

def get_days_array():
    days_array = []
    if check_if_table_exist('DailyLogs'):
        days_array = upd_missed_dates()
        return days_array


#
#
#
#

def get_datepage_info(date):
    conn = get_db_connection()
    reg_activity = conn.execute('SELECT * FROM Activities').fetchall()
    tasks = conn.execute('SELECT * FROM Activities').fetchall()
    date_info = conn.execute('SELECT Date, DailyPerformanceMetrics FROM DailyLogs WHERE Date = ?;', [date]).fetchone()
    day_logs = conn.execute('SELECT ActivityName, LogID FROM Activities INNER JOIN ActivityLog '
                            'ON Activities.ActivityID=ActivityLog.ActivityID WHERE DailyLogID = ?;', [date]).fetchall()



    close_db_connection(conn)
    return reg_activity, tasks, date_info, day_logs

def upd_db_day(day, rait):
    conn = get_db_connection()
    conn.cursor().execute("UPDATE DailyLogs SET DailyPerformanceMetrics=(?) WHERE Date=(?)", (rait, day))
    close_db_connection(conn)

def add_ActivityLog(task):  #Тут костиль по доступу по назві, треба переписати
    print("Inserting activityLog to BD")
    conn = get_db_connection()
    activityID = conn.execute('SELECT ActivityID, duration FROM Activities WHERE ActivityName = ?;', [task['taskName']]).fetchone()
    conn.cursor().execute("INSERT INTO ActivityLog (LogID, ActivityID, TimeSpent, DailyLogID) VALUES (?,?,?,?)", (str(uuid4()), *activityID, task["date"]))
    close_db_connection(conn)

def del_ActivityLog(logID):
    conn = get_db_connection()
    print("Deleting activityLog from BD")

    print(conn.cursor().execute("DELETE FROM ActivityLog  WHERE LogID=(?)", (logID,)))
    close_db_connection(conn)


def add_Activity(task):
    print("Inserting activity to BD")
    conn = get_db_connection()
    id = str(uuid4())
    conn.cursor().execute("INSERT INTO Activities(ActivityID, ActivityName, Description, Category, Repeats, Points, Time, Duration) VALUES (?,?,?,?,?,?,?,?)",
                          (id, *task))
    close_db_connection(conn)
    return id

def create_db():
    print('Creating DB')
    connection = get_db_connection()

    with open('schema.sql') as f:
        test = connection.executescript(f.read())
        print(test)

    close_db_connection(connection)


