import flask
import model
import os
import requests

UPLOAD_FOLDER = './logs'

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'log'])

@app.route("/")
def home():
    return flask.render_template("home.html", tasks=model.db)

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
        model.db.append(task)
        model.save_db()
        return flask.redirect(flask.url_for('taskView', index=len(model.db)-1))
    else:
        # GET
        return flask.render_template("addTask.html")

@app.route('/removeTask/<int:index>', methods=["GET", "POST"])
def removeTask(index):
    try:
        if flask.request.method == "POST":
            del model.db[index]
            model.save_db()
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

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return flask.Response(status=200) 
    #return flask.send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/logfile/upload', methods=["POST"])
def postLogFile():
    # check if the post request has the file part
    #if 'file' not in flask.request.files:
    #    #flash('No file part')
    #    return flask.redirect(request.url)
    #file = flask.request.files['file']
    ## if user does not select file, browser also
    ## submit an empty part without filename
    #if file.filename == '':
    #    #return flask.redirect(request.url)
    logging.warning("See this message in Flask Debug Toolbar!")
    if file and allowedFile(file.filename):
        filename = flask.secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return flask.redirect(url_for('uploaded_file', filename=filename))

