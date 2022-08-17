from flask import render_template, request, session, redirect, flash, url_for
from flask_mail import *
import os
from datetime import datetime
from app import app, db, mail, bcrypt, s
from .models import Users, Admin, Contact


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
        msg = Message('Contact Request-UMS', sender=email, recipients=[os.environ.get('EMAIL_USER')])
        msg.body = f'''{message}\nRegards:\n{first_name} {last_name}\n{phone}'''

        mail.send(msg)

    return render_template('contactus.html')

