from flask import Flask

app = Flask(__name__)

from btracker import routes

#@app.route("/")
#def main_():
#       my_str = 'hello ni hao'
#       return my_str
