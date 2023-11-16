import array
import random
from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
import datetime
import trash, innit_bd, db_manager



app = Flask(__name__)
my_history = []
my_history_formated = []



def create_array_for_heatmap():
    my_history_formated.clear()
    my_history = db_manager.get_days_array()
    for rows in range(6):
        my_history_formated.append([])
        for cols in range(61):
            my_history_formated[rows].append(my_history.pop(-1))


@app.route('/')
def index():
    trash.Screenshot()
    return render_template('cheatmap.html' , table_data=my_history_formated)

@app.route('/<date>')
def date_page(date):
    test = []
    trash.Screenshot()
    tasks, date_info = db_manager.get_datepage_info(date)
    return render_template('date_page.html', datetest=date_info, task_array=tasks)

@app.route('/<date>/upd', methods=['GET', 'POST'])
def date_page_upd(date):

    trash.Screenshot()
    if request.method == 'POST':
        form_data = request.form["lvl_upd"]
        db_manager.upd_db_day(date, int(form_data))
        create_array_for_heatmap()

    return redirect('/')


if __name__ == '__main__':
    create_array_for_heatmap()

    app.run()
    '''

    for i in range(10):
        coonect.cursor().execute("INSERT INTO tasks (task, descr) VALUES (?, ?)",
                                 ("Wake up", "first try"))
        coonect.cursor().execute("INSERT INTO tasks (task, descr) VALUES (?, ?)",
                                 ("Make tea", "black"))
    coonect.commit()
'''