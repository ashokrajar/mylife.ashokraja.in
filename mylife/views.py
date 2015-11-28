from flask import render_template

from mylife import app


@app.route('/')
def home():
    return render_template('home.html')
