import array
import random
from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
import datetime
import trash, innit_bd



app = Flask(__name__)
my_history = []
my_history_formated = []

def fill_missed_dates(db_array, conn):
    if len(db_array) == 0:
        delta_days = 366
    else:
        delta_days =  (datetime.datetime.now().date() - datetime.datetime.strptime(db_array[-1][1], '%Y-%m-%d').date()).days
    if delta_days>0:
        print("need to insert days ", delta_days)
        for i in range(delta_days, -1 , -1):
            conn.cursor().execute("INSERT INTO days (date) VALUES (?)",
                (datetime.date.today()-datetime.timedelta(days=i),))
        conn.commit()
    elif delta_days<0:
        print("DB mistake, need rebuild")
    else:
        print("DB looks fine!")

def get_db_connection():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def check_if_table_exist(table_name):
    test = coonect.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,)).fetchall()
    if test == []:
        innit_bd.create_db()
        return True
    return True

def create_array_for_heatmap():
    my_history_formated.clear()
    if check_if_table_exist('days'):
        my_history = coonect.execute('SELECT * FROM days').fetchall()
        fill_missed_dates(my_history, coonect)
        for rows in range(6):
            my_history_formated.append([])
            for cols in range(61):
                my_history_formated[rows].append(my_history.pop(-1))

def upd_db_day(day, rait):
   sql_upd = "UPDATE days SET raiting = ? WHERE date = ?"
   coonect.cursor().execute("UPDATE days SET raiting=(?) WHERE date=(?)", (rait, day))
   coonect.commit()
   create_array_for_heatmap()
@app.route('/')
def index():
    trash.Screenshot()
    return render_template('cheatmap.html' , table_data=my_history_formated)

@app.route('/<date>')
def date_page(date):
    trash.Screenshot()
    return render_template('date_page.html', date=date)

@app.route('/<date>/upd', methods=['GET', 'POST'])
def date_page_upd(date):
    trash.Screenshot()
    if request.method == 'POST':
        title = request.form["lvl_upd"]
        upd_db_day(date, int(title))

    return redirect('/')


if __name__ == '__main__':
    coonect = get_db_connection()
    create_array_for_heatmap()
    app.run()






