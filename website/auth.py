from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
#Blueprint has a bunch of roots/URL defined inside for the app to work and access the root
from flask_login import login_user, login_required, logout_user, current_user
#current user holds current user 

auth=Blueprint("auth",__name__)#defining the name of the blueprint

@auth.route('/login',methods=['GET','POST'])# /login routes us to login page that returns Login as a <p>
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')

        #user stores boolean value
        user=User.query.filter_by(email=email).first()#here we're filtering all same email id and finding the first email id with same email id
        if user:
            if check_password_hash(user.password,password):#checking if user's pwd in db is equal to current pwd typed by user
                flash('Logged in successfully',category='success')
                login_user(user,remember=True)# remember means that server knows that the user 
                #has previously logged in and doesn't ask for user credentials 
                return redirect(url_for('views.home'))
            else:
                flash('Wrong password, try again',category='error')
        else:
            flash('Invalid username or password',category='error')
    # data=request.form #gets form data
    # print(data)
    return render_template("login.html",user=current_user)#render_template() can have as many parameters as possible and any variable name

@auth.route('/logout')
@login_required# can access home only when user is logged in 
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        email=request.form.get('email')
        first_name=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        user=User.query.filter_by(email=email).first()#making sure that no duplicate user exists 
        if user:
            flash('User exists create new user',category='error')

        if len(email)<4:
            flash('email must be at least 4 characters', category='error')
        
        elif len(first_name)<3:
            flash('first name must be at least 3 characters',category='error')

        elif len(password1)<8:
            flash('password must be at least 8 characters', category='error')

        elif password1!=password2:
            flash('passwords don\'t match',category='error')

        else:
            #create new user 
            new_user=User(email=email,first_name=first_name,password=generate_password_hash(password1,method='sha256'))#there are many methods we can use
            #add created user to database if no errors are present
            db.session.add(new_user)
            db.session.commit()#letting the db know that there are changes made
            login_user(user,remember=True)
            flash ('account created', category='success')
            return redirect(url_for('views.home'))#return home method from views blueprint

    return render_template("sign_up.html",user=current_user)
