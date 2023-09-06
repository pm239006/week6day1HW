from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from datetime import datetime
import uuid

db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) #this queries our database and brings back the user with the same id 

class User(db.Model,UserMixin):
        #think of this part as the CREATE TABLE 'User' 
    user_id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(30))
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self,username,email,password, first_name= "", last_name = ""):
        self.user_id = self.set_id() #method to create unique id 
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = self.set_password(password) #method to hash our password for security 

    def set_id(self):
        return str(uuid.uuid4()) #random username - unique user id 

    def set_password(self,password):
        return generate_password_hash(password)
    
    def __repr__(self):
        return f"USER: {self.username}"
    
