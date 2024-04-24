from flask import render_template, request, session, redirect, flash
from flask_app.models.user import User

from flask_app import app

#Initialize Bcrypt for password hashing
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

#Route for the login/registration form
@app.route("/")
def index():
    #Render the login/registration HTML template
    return render_template("login_registration.html")
#Route for submitting the user login form
@app.route("/user/login", methods=['POST'])
def login():
    #Retrieve the user from the database based on the provided email 
    user = User.get_by_email(request.form)
    if not User.validate_login(request.form):
        #Redirect the user back to the login/registration form
        flash ("Invalid Email/Password")
        return redirect('/')    
    #Check if the user exists and the password is valid
    if not user or not bcrypt.check_password_hash(user.password, request.form ['password']):
        #Flash an error message if the email/password is invalid
        flash("Invalid Email/Password")
        #Redirect the user back to the login/registration form
        return redirect('/')
    #Store User's ID and First Name in Session
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    #Redirect the user to the dashboard
    return redirect('/dashboard')  
#Route for registering a New User
@app.route("/user/register", methods=['POST'])
def register():
    #Validate the user's registration form data
    if not User.validate_user(request.form):
        return redirect('/')
    #Create a New User in the Database
    data={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email_address": request.form['email'],
        "password":bcrypt.generate_password_hash(request.form['password']),
        }
    
    user_id=User.add(data)
    #Call the save method on the User model to create the new user
    session['user_id'] = user_id
    #Redirect the User to the dashboard
    return redirect("/dashboard")
#Route for the dashboard
@app.route("/dashboard")
def dashboard():
    #Check if the user is logged in 
    if 'user_id' not in session:
        #If the user is not logged in, redirect to the logout route
        return redirect('/logout')
    #If the user is logged in, render the dashboard template
    data = {
        'id': session['user_id']
    }
    #Render the dashboard template with the user's data
    return render_template("dashboard.html", user=User.get_by_id(data))
#Route for logging out the User
@app.route("/logout")
def logout():
    #Clear the User's session data
    session.clear()
    #Redirect the User to the login/registration page 
    return redirect('/')