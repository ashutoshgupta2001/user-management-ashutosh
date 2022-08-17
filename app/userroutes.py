from flask import render_template, request, session, redirect, flash, url_for
from flask_mail import *
import os
from datetime import date
from app import app, db, mail, bcrypt, s
from .models import Users


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
    msg = Message('Email Verification-mail', sender=os.environ.get('EMAIL_USER'), recipients=[username])
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
    msg = Message('Reset Password Mail', sender=os.environ.get('EMAIL_USER'), recipients=[username])
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

