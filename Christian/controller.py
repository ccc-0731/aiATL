from flask import Flask, render_template, redirect, url_for, request, session, flash
import requests;
from werkzeug.utils import secure_filename
from model import DAL
from werkzeug.utils import secure_filename
import geminiCall as gemini

ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.secret_key = "hi"

#takes in a filename and checks if the extention is allowed
def allowed_file(filename) -> list[str]:
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#renders the index page
#if not logged in sends user to login
@app.route('/')
def index():  # put application's code here
    if "logged_in" not in session:
        #redirects to login
        return render_template('login_form.html')
    #adds username to the session cookie which just acts as a dictionary
    username = session["username"]
    #renders index
    return render_template('index.html')

#renders a login form to get a username
@app.route('/login_form', methods=['POST'])
def login():
    #if your logged in redirect to index
    if "logged_in" in session:
        return render_template('index.html')
    #stores username in the json file if it's not there and in the session cookie
    username = request.form.get('username')
    session['username'] = username
    if (username not in DAL.get_users_as_list):
        DAL.add_new_user(username)
    #adds a cookie to say you're logged in
    session["logged_in"] = True
    #sends you to index
    return redirect(url_for('index'))

#logs you out
@app.route('/logout')
def logout():
    #removes all info from cookie
    session.pop("username", None)
    session.pop("logged_in", None)
    return redirect(url_for('index'))

#uploads the file to 
@app.route("/upload_image", methods=['GET', 'POST'])
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
        #
        if file and allowed_file(file.filename):
            #makes the filename safe so no malware
            filename = secure_filename(file.filename)
            #saves the file to the images folder in database
            DAL.saveFile(file, session["username"])
            
            #Gemini Stuff
            questionsRaw: str = gemini.call_read(file)
            presentQuestions()
            return redirect(url_for('questions'))
            
    return


@app.route("/questions", methods=['GET','POST'])
def presentQuestions():
    


@app.route("/soulutions", methods=['GET','POST'])
def presentSolutions():


if __name__ == "__main__":
    app.run(debug=True)