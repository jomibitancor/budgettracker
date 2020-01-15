# __init__.py is Where we initialize our application and bring together different components
from flask import Flask # Flask - let's us start the app and the live webserver
from flask_sqlalchemy import SQLAlchemy # INSTALL: pip install flask-sqlalchemy
from flask_bcrypt import Bcrypt # INSTALL: pip install flask-bcrypt
from flask_login import LoginManager # INSTALL: pip install flask-login
from flask_mail import Mail # INSTALL: pip install flask-mail
import os # To be able to grab access to environment variables  

app = Flask(__name__)
app.config['SECRET_KEY'] = '6bd69d9af78717a288b5a483cdc04dcc' # A secret key will protect from modifying cookies and cross-site request forgery attacks
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # sqlite:/// three slashes means a relative path from the current file
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'jomibitancor@gmail.com'
app.config['MAIL_PASSWORD'] = 'JoMiGmail9241997:D'   
     
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'primary'

mail = Mail(app)


from btracker import routes