from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_mail import *
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer as Serializer
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.environ.get("EMAIL_USER"),
    MAIL_PASSWORD=os.environ.get("EMAIL_PASSWORD"),
    MAIL_USE_TLS=False  
)
mail = Mail(app)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] =os.getenv('DATABASE_URL')

db = SQLAlchemy(app)
s = Serializer(app.config['SECRET_KEY'])
bcrypt = Bcrypt(app)

from app import mainroutes
from app import userroutes
from app import adminroutes
