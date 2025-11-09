
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
import requests;
from werkzeug.utils import secure_filename
from model import DAL
from werkzeug.utils import secure_filename
import geminiCall as gemini
from geminiCall import call_read  # your existing function

ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif'}
DELIMITER: str = ";"

app = Flask(__name__,template_folder='templates')

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
    return render_template('index.html',username=username)

#renders a login form to get a username
@app.route('/login_form', methods=['POST'])
def loginForm():
    if "logged_in" not in session:
        return render_template('login_form.html')
    return redirect("/")

@app.route('/login', methods=['POST'])
def login():
    #if your logged in redirect to index
    if "logged_in" in session:
        return render_template('index.html')
    #stores username in the json file if it's not there and in the session cookie
    username = request.form.get('username')
    session['username'] = username
    if (username not in DAL.get_users_as_list()):
        DAL.add_new_user(username)
    #adds a cookie to say you're logged in
    session["logged_in"] = True
    #sends you to index
    return redirect("/")

#logs you out
@app.route('/logout')
def logout():
    if "logged_in" not in session:
        #redirects to login
        return render_template('login_form.html')
    username: str = session["username"]
    DAL.eraseUserData(username)
    #removes all info from cookie
    session.pop("username", None)
    session.pop("logged_in", None)
    return redirect("/")

#uploads the file to
@app.route("/upload_image", methods=['GET', 'POST'])
def uploadFile():
    if "logged_in" not in session:
        #redirects to login
        return render_template('login_form.html')
    FORMNAME = 'image_input'
    username = session["username"]
    if request.method == 'POST':
        if FORMNAME not in request.files:
            flash('No file part')
            return redirect("/")
        files= request.files.getlist(FORMNAME)
        test = request.files[FORMNAME]
        print(files)
        print(test)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        filePaths = []
        for file in files:
            if file.filename == '':
                flash('No selected file')
                return redirect("/")
            if file and allowed_file(file.filename):
                IMAGESPATH = "database/images/"
                print(file)
                #makes the filename safe so no malware
                filename = secure_filename(file.filename)
                #saves the file to the images folder in database
                DAL.saveFile(file, session["username"],filename)
                filePaths.append(IMAGESPATH+session["username"]+"/"+filename)

        #Gemini Stuff
        questionsList: list[str] = gemini.call_read(stage=1, filepaths=filePaths)
        print(questionsList)
        return render_template('questions.html',testQuestions=questionsList,images=filePaths,username=username)

    return redirect("/")

@app.route("/solution", methods=['GET',"POST"])
def getSolutions():
    if "logged_in" not in session:
        #redirects to login
        return redirect('/')
    username:str = session["username"]
    answers:list[str] = []
    for value in request.values:
        answers.append(value)
    filePaths:list[str] = DAL.get_file_paths(username)
    result = gemini.call_read(2,"|".join(answers),filePaths)

    return render_template('solutionsIframePotential.html', solutions=result["solutions"])

if __name__ == "__main__":
    app.run(host="0.0.0.0")

