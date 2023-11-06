from flask import Flask, render_template

import trash

app = Flask(__name__)


@app.route('/')
def index():
    trash.Screenshot()
    return render_template('index.html')







if __name__ == '__main__':
    app.run()
