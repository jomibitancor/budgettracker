from btracker import app
from flask import render_template

@app.route("/")
def main_():
        return render_template('intro.html')
