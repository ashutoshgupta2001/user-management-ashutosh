from app import db

class Users(db.Model):
    '''
    sn, name, username,password,date
    '''
    user_id = db.Column(db.Integer, nullable=False, primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50),nullable=True )
    username = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(250), nullable=False)
    dob = db.Column(db.String(30), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    education = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Integer,nullable=False)

class Admin(db.Model):
    '''
    sn, name, username,password
    '''
    sn = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
    name = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False, )
    password = db.Column(db.String(20), nullable=False)

class Contact(db.Model):
    '''
    sn, first_name,last_name, email, mobile_no,date,message
    '''
    sn = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(30),nullable=False)
    phone = db.Column(db.String(10), nullable=True)
    message = db.Column(db.String(250), nullable=False)
    status = db.Column(db.String(25),nullable=True)
    date = db.Column(db.DateTime(timezone=True), nullable=False)





