from flask import Flask, render_template, redirect, url_for, request, session, flash
import requests;
from werkzeug.utils import secure_filename
from model import DAL
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.secret_key = "hi"

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():  # put application's code here
    if "logged_in" not in session:
        return render_template('login_form.html')
    username = session["username"]
    return render_template('index.html')


@app.route('/login_form', methods=['POST'])
def login():
    if "logged_in" in session:
        return render_template('index.html')
    username = request.form.get('username')
    session['username'] = username
    session["logged_in"] = True
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop("username", None)
    session.pop("logged_in", None)
    return redirect(url_for('index'))

@app.route("/upload", methods=['GET', 'POST'])
def uploadFile():
    FORMNAME = 'file'
    if request.method == 'POST':
        if FORMNAME not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files[FORMNAME]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            DAL.saveFile(file, session["username"])
            return redirect(url_for('download_file', name=filename))
    return

if __name__ == "__main__":
    app.run(debug=True)