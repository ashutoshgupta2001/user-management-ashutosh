from flask import Flask, render_template, request, session, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import json
from flask_mail import *
from random import *
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer as Serializer
from datetime import datetime,date
from dotenv import load_dotenv
load_dotenv()


# with open("config.json", "r") as c:
#     params = json.load(c)["params"]

app = Flask(__name__)

gmail_user= os.getenv("EMAIL_USER")  
gmail_password= os.getenv("EMAIL_PASSWORD")  

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=gmail_user,
    MAIL_PASSWORD=gmail_password,
    MAIL_USE_TLS=False  
)
mail = Mail(app)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://dctbaweftgwoor:66ca3e590119e8a8562f420de326678f54da27d94b8798d55311ba8c28586bde@ec2-18-214-35-70.compute-1.amazonaws.com:5432/deh27mlcom5tav"

db = SQLAlchemy(app)
s = Serializer(app.secret_key)
bcrypt = Bcrypt(app)

from models import *
db.create_all()

@app.route('/')
def home():
    return render_template('newhome.html')


@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    if (session.get('username')):
        return redirect('/userdashboard')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # remember = True if request.form.get('remember') else False

        user = Users.query.filter_by(username=username).first()
        if (user and bcrypt.check_password_hash(user.password, password)):
            if user.status == 1:
                session['username'] = username
                flash("Login Successfully.", "success")
                return redirect('/userdashboard')
            else:
                flash("Your email is not verified yet, Please verify your email.", "danger")
                send_verification_mail(username)
                flash("Verification link has been sent to your email, Plaese Check your Email for confirmation", "success")
                session['newuser'] = username
        else:
            flash("Invalid Username or Password, Try again! ", "danger")

    return render_template('login1.html')


@app.route('/userdashboard')
def userdashboard():
    if session.get('username'):
        username = session.get('username')
        users = Users.query.filter_by(username=username).first()
        return render_template('dashboard.html', username=username, users=users)
    else:
        return redirect('/userlogin')

@app.route('/user/delete-profile',methods=['GET', 'POST'])
def user_delete():
    if not (session.get('username')):
        return redirect('/userlogin')
    if request.method == 'POST':
        username = session.get('username')
        user = Users.query.filter_by(username=username).first()
        current_password = request.form.get('current_password')
        if user and bcrypt.check_password_hash(user.password, current_password):
            db.session.delete(user)
            db.session.commit()
            session.pop('username')
            return redirect('/')
        flash("Wrong Password", "warning")
    return render_template('userdeleteprofile.html')

@app.route('/userlogout')
def userlogout():
    if ('username' in session):
        session.pop('username')
        flash("Logout Successfully.", "success")
        return redirect('/userlogin')
    return redirect('/')


@app.route('/user/update-profile', methods=['GET', 'POST'])
def userUpdateProfile():
    if not session.get('username'):
        return redirect('/userlogin')

    if session.get('username'):
        username = session.get('username')

    user = Users.query.filter_by(username=username).first()

    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        dob = request.form.get('dob')
        phone = request.form.get('phone')
        education = request.form.get('education')
        address = request.form.get('address')
        gender = request.form.get('gender')
        user.first_name=first_name
        user.last_name=last_name
        user.dob=dob
        user.phone=phone
        user.education=education
        user.address=address
        user.gender=gender
        db.session.commit()
        flash("Profile Updated Successfully", "success")
        return redirect('/userdashboard')

    return render_template('updateprofile.html', user=user)


@app.route('/user/change-password', methods=['GET', 'POST'])
def userChangePassword():
    if not session.get('username'):
        return redirect('/userlogin')

    username = session.get('username')
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        user = Users.query.filter_by(username=username).first()
        if not bcrypt.check_password_hash(user.password, current_password):
            flash("Current Password Wrong.","danger")
        else:    
            if new_password == confirm_password:
                hash_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                user.password = hash_password
                db.session.commit()
                flash("Password Changed Successfully", "success")
                # return redirect('/userdashboard')
            else:
                flash("New Password and Confirm Password did'nt matched", "danger")            
        
    return render_template('userchangepassword.html', username=username, title='user')



def send_verification_mail(username):
    token = s.dumps(username, salt='email-confirmation-key')
    link = url_for('confirm', token=token, _external=True)
    msg = Message('Email Verification-mail', sender=gmail_user, recipients=[username])
    msg.body = f'''To verify your account Click here:  {link} \n This link is valid only for 5 Minuts. after this it will autumatically expired.\n If you did not make this request then simply ignore this email and no changes will be made. '''

    mail.send(msg)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        password = request.form.get('password')

        euser = Users.query.filter_by(username=username).first()

        if euser:
            flash("The account for this username is already exist.", "warning")
        else:
            hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = Users(first_name=first_name, last_name=last_name, username=username, password=hash_password,status=0, date=date.today())
            
            session['newuser'] = username
            send_verification_mail(username)
            db.session.add(user)
            db.session.commit()
            flash("Account created Successfully","success")
            flash("Verification link has been sent to your email, Plaese Check your Email for confirmation", "success")
            
            return redirect('/signup')

    return render_template('signup2.html')


@app.route('/confirm/<token>')
def confirm(token):
    if 'newuser' in session:
        try:
            email = s.loads(token, salt='email-confirmation-key', max_age=600)
            # flash("Email Verified,Please set your password")
        except Exception:
            session.pop('newuser')
            flash("Session Expired....", "danger")
            return redirect('/sign-up')
        if email:
            username = session.get('newuser')
            print(username)
            user = Users.query.filter_by(username=username).first()
            user.status = 1
            db.session.commit()
            return render_template('emailverified.html')
    return redirect('/userlogin')



def send_forgetPassword_mail(username):
    token = s.dumps(username, salt='email-confirmation-key')
    link = url_for('reset', token=token, _external=True)
    msg = Message('Reset Password Mail', sender=gmail_user, recipients=[username])
    msg.body = f'''To reset your account password Click here:  {link} \n This link is valid only for 5 Minuts. after this it will autumatically expired.\n If you did not make this request then simply ignore this email and no changes will be made.'''

    mail.send(msg)


@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == "POST":
        username = request.form.get('username')

        euser = Users.query.filter_by(username=username).first()
        if euser:
            session['user'] = username
            send_forgetPassword_mail(username)
            flash("Reset-Password link has been sent successfully to your email. ", "success")
            # return redirect('reset_password')
        else:
            flash("The account does'nt exist for this username", "danger")
            # return redirect('/reset_password')

    return render_template('forget_password.html')


@app.route('/reset/<token>')
def reset(token):
    if 'user' in session:
        try:
            email = s.loads(token, salt='email-confirmation-key', max_age=60)
            # flash("Reset Password,Please set your new password")
        except Exception:
            flash("Session Expired...", "danger")
            session.pop('user')
            return redirect('/forget_password')

        if email:
            return redirect('/createnew_password')
    return redirect('/forget_password')


@app.route('/createnew_password', methods=['GET', "POST"])
def createnew_password():
    if 'user' in session:
        username = session.get('user')
        if request.method == 'POST':
            new_password = request.form.get('new_password')
            cpassword = request.form.get('confirm_password')

            if (new_password == cpassword):
                hash_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                user = Users.query.filter_by(username=username).first()
                user.password = hash_password
                db.session.commit()
                session.pop('user')
                flash("Password updated successfully", "success")
                return redirect('/userlogin')
            else:
                flash("Password and Confirm Password did'nt match, try again", "warning")
        return render_template('/setnew_password.html', username=username)
    return render_template('/forget_password.html')


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if ('admin' in session):
        return redirect('/admindashboard')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()

        if admin and password == admin.password:
            session['admin'] = username
            flash("Login Successfully.", "success")
            return redirect('/admindashboard')

        else:
            flash("Invalid Username or Password, Try again! ", "danger")

    return render_template('adminlogin.html')


@app.route('/admindashboard')
def admindashboard():
    if ('admin' in session):
        page = request.args.get('page', 1, type=int)
        # employees = Employees.query.paginate(per_page=5, page=page_num, error_out=True)
        users = Users.query.paginate(page=page, per_page=3)
        return render_template('admindashboard.html', users=users, page=page)
    else:
        return redirect('/adminlogin')

@app.route('/admindashboardcontacts')
def admindashboardcontacts():
    if ('admin' in session):
        page = request.args.get('page', 1, type=int)
        contact = Contact.query.paginate(page=page, per_page=3)
        return render_template('admindashboardcontact.html', contact=contact, page=page)
    else:
        return redirect('/adminlogin')

@app.route('/contactrequestcompleted/<string:sn>')
def contactrequestcompleted(sn):
    if session.get('admin'):
        contact = Contact.query.filter_by(sn=sn).first()
        contact.status = "Completed"
        db.session.commit()
        return redirect('/admindashboardcontacts')

    return redirect('/')        

@app.route('/admin/change-password', methods=['GET', 'POST'])
def adminChangePassword():
    if not session.get('admin'):
        return redirect('/adminlogin')

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        c_password = request.form.get('confirm_password')
        username = session.get('admin')

        if new_password == c_password:
            admin = Admin.query.filter_by(username=username).first()
            admin.password = new_password
            db.session.commit()
            flash("Password Changed Successfully", "success")
        else:
            flash("New Password and Confirm Password did'nt matched", "danger")

    return render_template('adminchangepassword.html')

@app.route('/delete/<string:user_id>')
def delete(user_id):
    if session.get('admin'):
        user = Users.query.filter_by(user_id=user_id).first()
        db.session.delete(user)
        db.session.commit()
    return redirect('/admindashboard')



@app.route('/adminlogout')
def adminlogout():
    if ('admin' in session):
        session.pop('admin')
        flash("Logout Successfully.", "success")
        return redirect('/adminlogin')
    else:
        return redirect('/')


@app.route('/contact', methods=['GET','POST'])
def contact():
    if(request.method =="POST"):
        ''' Add entry to database'''
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        entry = Contact(first_name=first_name, last_name=last_name, email=email, phone=phone,status="", date=datetime.now(), message=message )
        db.session.add(entry)
        db.session.commit()
        flash("Thanks for contacting us. We will get back to you soon.", "success")
        msg = Message('Contact Request-UMS', sender=email, recipients=[gmail_user])
        msg.body = f'''{message}\nRegards:\n{first_name} {last_name}\n{phone}'''

        mail.send(msg)

    return render_template('contactus.html')

if __name__ == "__main__":
    app.run(debug=True)