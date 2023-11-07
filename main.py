import random
from flask import Flask, render_template
import sqlite3
from datetime import datetime, timedelta
import trash


connection = sqlite3.connect('database.db')

app = Flask(__name__)
my_history = []
my_history_formated = []


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
def create_array_for_heatmap():
    my_history = coonect.execute('SELECT * FROM days').fetchall()
    for rows in range(6):
        my_history_formated.append([])
        for cols in range(61):
            my_history_formated[rows].append(my_history.pop(0))
@app.route('/')
def index():
    trash.Screenshot()
    return render_template('cheatmap.html' , table_data=my_history_formated)

@app.route('/<date>')
def date_page(date):
    trash.Screenshot()
    return render_template('index.html')


if __name__ == '__main__':
    coonect = get_db_connection()
    create_array_for_heatmap()
    app.run()






