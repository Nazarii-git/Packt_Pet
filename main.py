import random

from flask import Flask, render_template
from datetime import datetime, timedelta
import trash

app = Flask(__name__)
my_history = []
my_history_formated = []

@app.route('/')
def index():
    trash.Screenshot()
    return render_template('cheatmap.html' , table_data=my_history_formated)






if __name__ == '__main__':
    for i in range(0,366):
        my_history.append([(datetime.today() - timedelta(days=i)).strftime("%x"), random.randint(0,4)])

    for rows in range(6):
        my_history_formated.append([])
        for cols in range(61):
            my_history_formated[rows].append(my_history.pop(0))




    app.run()
