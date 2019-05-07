from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..model import User

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests for to the database through the registration form

    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                            username= form.username.data,
                            first_name = form.first_name.data,
                            last_name = form.last_name.data,
                            password = form.password.data)
        #add employee to the database
        db.session.add(user)
        db.session.commit()
        flash('You have successively registered! You may now login.')

    #redirect to the login page
    return render_template('auth/register.html', form=form, title="Register")

@auth.route('/login', methods=['GET', 'POST'])
def login():
# @login_required
    """
    Handle requests to the /login route
    Log a user in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():
        #check whether employee exists in the database and whether
        #the password entered matches the password in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            #log employee in
            login_user(user)
            #redirect to the appropriate dashboard page
            if user.is_admin:
                return redirect(url_for('home.admin_dashboard'))
 
            #redirect to the dashboard page after login
            return redirect(url_for('home.index'))
        #when login details are incorrect
        else:
            flash('Invalid Email Or Password.')
    #load login template
    return render_template('home/index.html', form=form, title="Login")

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successively been logged out.')

    #redirect to the login page
    return redirect(url_for('home.index'))