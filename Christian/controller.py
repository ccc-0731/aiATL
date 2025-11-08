from flask import Flask, render_template, redirect, url_for, request, session
import requests;
from werkzeug.utils import secure_filename


import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



app = Flask(__name__)

app.secret_key = "hi"


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
