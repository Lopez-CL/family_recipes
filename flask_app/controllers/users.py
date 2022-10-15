from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import recipe,user #import models
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# HOME + DASHBOARD Route


@app.route("/")
def index():
    return render_template("index.html")

# LOGIN/LOGOUT ROUTES
@app.route('/register', methods=['post'])
def reg_user():
    if not user.User.validate_reg(request.form):
        return redirect('/')
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = user.User.save(data)
    return redirect('/recipes')

@app.route('/login',methods=['post'])
def login_user():
    #find the user in the db
    found_user_or_none = user.User.validate_login(request.form)
    if not found_user_or_none:
        return redirect('/')
    else: #don't forget to create the session for the user_id!
        session["user_id"] = found_user_or_none.id
        return redirect('/recipes')


@app.route('/logout')
def clear_user_session():
    session.clear()
    return redirect('/')