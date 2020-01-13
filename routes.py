from btracker import app

@app.route("/")
def main_():
        my_str = 'hello routes'
        return my_str
