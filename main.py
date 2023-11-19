
from flask import Flask, render_template, request, url_for, flash, redirect
import trash, db_manager
import json



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
    reg_activity, tasks, date_info = db_manager.get_datepage_info(date)
    return render_template('date_page.html', datetest=date_info, reg_activity = reg_activity, task_array=tasks)

@app.route('/<date>/upd', methods=['GET', 'POST'])
def date_page_upd(date):

    trash.Screenshot()
    if request.method == 'POST':
        form_data = request.form["lvl_upd"]
        db_manager.upd_db_day(date, int(form_data))
        create_array_for_heatmap()

    return redirect('/')

@app.route('/ajax', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        db_manager.add_ActivityLog(request.get_json()["taskName"])
    return "200"





if __name__ == '__main__':
    create_array_for_heatmap()

    app.run()
