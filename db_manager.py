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
        for i in range(delta_days, 0 , -1):
            conn.cursor().execute("INSERT INTO DailyLogs (LogID, Date) VALUES (?, ?)",
                (str(uuid4()), datetime.date.today()-datetime.timedelta(days=i-1)))
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
    reg_activity = conn.execute('SELECT ActivityName, Activities.ActivityID, Points, Repeats-ifnull(Done_number, 0) AS Repeats '
                                'FROM Activities LEFT JOIN (SELECT ActivityID, COUNT(LogID) AS Done_number '
                                'FROM ActivityLog '
                                'WHERE DailyLogID > ? GROUP BY ActivityID) AL on Activities.ActivityID = AL.ActivityID WHERE Activities.Category = \'Weekly\''
                                                                'GROUP BY Activities.ActivityID;', [str(datetime.date.today() - datetime.timedelta(days=7))]).fetchall()

    tasks = conn.execute('SELECT * FROM Activities WHERE Category = "Task"').fetchall()
    date_info = conn.execute('SELECT Date, DailyPerformanceMetrics FROM DailyLogs WHERE Date = ?;', [date]).fetchone()
    day_logs = conn.execute('SELECT ActivityName, LogID, Points FROM Activities INNER JOIN ActivityLog '
                            'ON Activities.ActivityID=ActivityLog.ActivityID WHERE DailyLogID = ?;', [date]).fetchall()
    day_points = conn.execute('SELECT ifnull(sum(Points), 0) FROM (SELECT ActivityName, LogID, Points FROM Activities INNER JOIN ActivityLog '
                            'ON Activities.ActivityID=ActivityLog.ActivityID WHERE DailyLogID = ?);', [date]).fetchone()
    close_db_connection(conn)
    return reg_activity, tasks, date_info, day_logs, day_points

def upd_db_day(lvl_info):
    conn = get_db_connection()
    conn.cursor().execute("UPDATE DailyLogs SET DailyPerformanceMetrics=(?) WHERE Date=(?)", (lvl_info["lvl"], lvl_info["date"]))
    close_db_connection(conn)

def add_ActivityLog(task):  #Тут костиль по доступу по назві, треба переписати
    print("Inserting activityLog to BD")
    conn = get_db_connection()
    activityID = conn.execute('SELECT ActivityID, duration FROM Activities WHERE ActivityName = ?;', [task['taskName']]).fetchone()
    conn.cursor().execute("INSERT INTO ActivityLog (LogID, ActivityID, TimeSpent, DailyLogID) VALUES (?,?,?,?)", (str(uuid4()), *activityID, task["date"]))
    close_db_connection(conn)

def get_ActivityLog_details(task):
    print("Getting activityLog details")
    conn = get_db_connection()
    activityID = conn.execute('SELECT * FROM Activities WHERE ActivityID = ?;', [task,]).fetchone()
    close_db_connection(conn)
    return activityID

def del_ActivityLog(logID):
    conn = get_db_connection()
    print("Deleting activityLog from BD")

    print(conn.cursor().execute("DELETE FROM ActivityLog  WHERE LogID=(?)", (logID,)))
    close_db_connection(conn)


def del_Activity(logID):
    conn = get_db_connection()
    print("Deleting Activity from BD")
    print(conn.cursor().execute("DELETE FROM Activities WHERE ActivityID=(?)", (logID,)))
    close_db_connection(conn)

def add_Activity(task):
    print("Inserting activity to BD")
    conn = get_db_connection()
    id = str(uuid4())
    conn.cursor().execute("INSERT INTO Activities(ActivityID, ActivityName, Description, Category, Repeats, Points, Time, Duration) VALUES (?,?,?,?,?,?,?,?)",
                          (id, *task))
    close_db_connection(conn)
    return id

def add_SignleTask(task):
    print("Inserting add_SignleTask to BD")
    conn = get_db_connection()
    id = str(uuid4())
    conn.cursor().execute("INSERT INTO Activities(ActivityID, ActivityName, Category, Points) VALUES (?,?,?,?)",
                          (id, task, "Task", 3))
    close_db_connection(conn)


def update_duration(task_id, duration):
    print("Updating duration in the database")
    conn = get_db_connection()
    conn.cursor().execute("UPDATE Activities SET Duration = ? WHERE ActivityID = ?",
                          (duration, task_id))
    close_db_connection(conn)

def edit_Activity(task):
    print("Editing activity in BD")
    conn = get_db_connection()
    id = task.pop(-1)

    conn.cursor().execute("""
        UPDATE Activities
        SET ActivityName = ?, Description = ?, Category = ?, Repeats = ?, Points = ?, Time = ?, Duration = ?
        WHERE ActivityID = ?
    """, (*task, id))
    close_db_connection(conn)
    return id


def create_db():
    print('Creating DB')
    connection = get_db_connection()

    with open('schema.sql') as f:
        test = connection.executescript(f.read())
        print(test)

    close_db_connection(connection)


