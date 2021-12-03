from flask import render_template, url_for, flash, redirect 
from lAsthIts import app

@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"
