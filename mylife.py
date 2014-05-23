import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def mylife():
    return "<html><h1>Live Die Repeat</h1></html>"
