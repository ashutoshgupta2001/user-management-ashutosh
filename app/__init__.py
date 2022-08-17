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
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://dctbaweftgwoor:66ca3e590119e8a8562f420de326678f54da27d94b8798d55311ba8c28586bde@ec2-18-214-35-70.compute-1.amazonaws.com:5432/deh27mlcom5tav"

db = SQLAlchemy(app)
s = Serializer(app.config['SECRET_KEY'])
bcrypt = Bcrypt(app)

from app import mainroutes
from app import userroutes
from app import adminroutes
