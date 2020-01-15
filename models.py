# Since we need the database, grab it from the main application file
from btracker import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin): # Create User Model # IMPORT: from flask_login import UserMixin
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    budgets = db.relationship('Budget', backref='budget_owner', lazy=True)
    entries = db.relationship('Entries', backref='entry_owner', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # __repr__ how our object is printed
    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.email}')"

class Budget(db.Model):
    bid = db.Column(db.Integer, primary_key=True)
    budget = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False )    

    def __repr__(self):
        return f"Budget('{self.user_id}', '{self.bid}', '{self.budget}')"

class Entries(db.Model):
    eid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # IMPORT from datetime import datetime
    category = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False )
    
    def __repr__(self):
        return f"Entries('{self.eid}', '{self.amount}', '{self.date_posted}')"