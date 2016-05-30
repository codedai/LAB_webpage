from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/milGo')
def milGo():
    return render_template("milGo.html")


@app.route('/project')
def project():
    return render_template("project.html")