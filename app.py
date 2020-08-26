import flask
import model
import os
import io
import requests
import sys
import covidData
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import datetime
import matplotlib.dates as mdates
import waitress

absolutePath = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = absolutePath + "\logs"

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)

ALLOWED_EXTENSIONS = set(['txt', 'log'])

@app.route("/")
def home():
    return flask.render_template("home.html", tasks=model.db, covidData=covidData.getCovidData(), inhabitants=covidData.getInhabitants())

@app.route('/login', methods=['POST'])
def login():
    if flask.request.form['password'] == '123' and flask.request.form['username'] == 'admin':
        flask.session['logged_in'] = True
        return flask.redirect(flask.url_for('home'))
    else:
        flask.flash('Wrong Login/Password!')
    return flask.render_template("login.html")

@app.route("/logout")
def logout():
    flask.session['logged_in'] = False
    return flask.render_template("login.html")

@app.route("/taskView/<int:index>")
def taskView(index):
    try:
        task = model.db[index]
        return flask.render_template("task.html", task=task, index=index, maxIndex=len(model.db)-1)
    except IndexError:
        flask.abort(404)

@app.route("/plot/<country>")
def plot(country):
    casesPerDay, date, url = covidData.getDataPerCountry(country)
    fig=Figure()
    ax=fig.add_subplot(111)
    numdays = len(date)
    base = datetime.datetime.today() - datetime.timedelta(numdays)
    date_list = [base + datetime.timedelta(days=x) for x in range(0, numdays)]
    locator = mdates.MonthLocator()  # every month
    fmt = mdates.DateFormatter('%b')
    ax.plot_date(date_list, casesPerDay, '-')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(fmt)
    ax.set_xlabel("Month")
    ax.set_ylabel("New Covid Cases")
    ax.grid()
    fig.suptitle(f"New Covid Cases in {country}", fontsize=16)
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = io.BytesIO()
    canvas.print_png(png_output)
    response=flask.make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


@app.route("/addTask", methods=["GET", "POST"])
def addTask():
    if not flask.session.get('logged_in'):
        return flask.render_template("login.html")
    else:
        if flask.request.method == "POST":
            task = {"titel": flask.request.form['titel'], "contact": flask.request.form['contact'], "description": flask.request.form['description']}
            model.insertTask(task)
            return flask.redirect(flask.url_for('taskView', index=len(model.db)-1))
        else:
            # GET
            return flask.render_template("addTask.html")

@app.route("/updateTask/<int:index>", methods=["GET", "POST"])
def updateTask(index):
    if flask.request.method == "POST":
        task = {"titel": flask.request.form['titel'], "contact": flask.request.form['contact'], "description": flask.request.form['description']}
        model.updateTask(task, model.db[index]['id'])
        return flask.redirect(flask.url_for('taskView', index=index))
    else:
        # GET
        return flask.render_template("updateTask.html", task=model.db[index])

@app.route('/removeTask/<int:index>', methods=["GET", "POST"])
def removeTask(index):
    try:
        if flask.request.method == "POST":
            model.deleteTask(index)
            return flask.redirect(flask.url_for('home'))
        else:
            return flask.render_template("removeTask.html", task=model.db[index])
    except IndexError:
        abort(404)

@app.route("/api/tasks/")
def api_taskList():
    return flask.jsonify(model.db)

@app.route("/api/task/<int:index>")
def api_card_detail(index):
    try:
        return model.db[index]
    except IndexError:
        flask.abort(404)

def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

waitress.serve(app, host='0.0.0.0', port=8080, threads=1)