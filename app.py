import flask
import model
import os
import requests
import sys
import covidData

absolutePath = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = absolutePath + "\logs"

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'log'])

@app.route("/")
def home():
    return flask.render_template("home.html", tasks=model.db, covidData=covidData.getCovidData(), inhabitants=covidData.getInhabitants())

@app.route("/taskView/<int:index>")
def taskView(index):
    try:
        task = model.db[index]
        return flask.render_template("task.html", task=task, index=index, maxIndex=len(model.db)-1)
    except IndexError:
        flask.abort(404)


@app.route("/addTask", methods=["GET", "POST"])
def addTask():
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