
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
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
@app.route('/modal')
def modal():
    trash.Screenshot()
    return render_template('task_modal.html')

@app.route('/<date>')
def date_page(date):
    test = []
    trash.Screenshot()
    reg_activity, tasks, date_info, day_logs, day_points = db_manager.get_datepage_info(date)
    return render_template('date_page.html', datetest=date_info, reg_activity = reg_activity, task_array=tasks, day_board = day_logs, day_points=day_points)

@app.route('/lvl_upd', methods=['GET', 'POST'])
def date_page_upd():
    if request.method == 'POST':
        db_manager.upd_db_day(request.get_json())
        create_array_for_heatmap()
    return "200"

@app.route('/ajax', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        db_manager.add_ActivityLog(request.get_json())
    return "200"

@app.route('/addTaskReq', methods=['GET', 'POST'])
def addTask():
    if request.method == 'POST':
        db_manager.add_Activity(request.form.to_dict().values())
    return "200"

@app.route('/EditTaskReq', methods=['GET', 'POST'])
def EditTask():
    if request.method == 'POST':
        db_manager.edit_Activity(list(request.form.to_dict().values()))
    return "200"


@app.route('/delTaskReq', methods=['GET', 'POST'])
def delTask():
    if request.method == 'POST':
        db_manager.del_ActivityLog(request.data.decode('ASCII'))  #why is it bytestring?
    return "200"


@app.route('/detailsTaskReq/<string:task_id>', methods=['GET'])
def detailsTask(task_id):
    print("Task details requested, id ", task_id)
    current_values = db_manager.get_ActivityLog_details(task_id)

    current_values = dict(current_values)
    dict.__delitem__(current_values, "ActivityID")
    dict.__delitem__(current_values, "UserID")
    current_values = json.dumps(current_values)

    print(current_values)

    return current_values




if __name__ == '__main__':
    create_array_for_heatmap()

    app.run()
