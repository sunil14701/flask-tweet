# it will contain all routes related to authentication like login,signup,signin,logout


from flask import Blueprint,redirect,url_for,request,flash
from flask import render_template # allows us to render HTML templates
from . import db 
from .models import User
from flask_login import login_user , logout_user , login_required , current_user
from werkzeug.security import generate_password_hash,  check_password_hash

# blueprint for storing diff routes
auth2 = Blueprint("auth",__name__)


@auth2.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # if user exist
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("Logged in!",category="success")
                login_user(user,remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect Password",category="error")
        else:
            flash("Email not registered",category="error")

    return render_template("login.html",user=current_user)


@auth2.route("/signup",methods=["GET","POST"])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        #checking if email exist . wapis jane ko bolna hai agar kuch pehle se hi hai database mein
        email_exist = User.query.filter_by(email=email).first()
        username_exist = User.query.filter_by(username=username).first()
        if email_exist:
            flash("Email already registered.",category="error")
        elif username_exist:
            flash("Username already exist.",category="error")
        elif password1 != password2:
            flash("Password don\'t match",category="error")
        elif len(username)<2:
            flash("Username is too short.",category="error")
        elif len(password1)<2:
            flash("password is too short.",category="error")
        elif len(email)<10:
            flash("Email is Invalid.",category="error")
        else:
            # if no error messages from above than create account
            new_user = User(email=email , username = username , password=generate_password_hash(password1,method="sha256")) # id will be auto generated so no need to pass id as argument , same for date_created
            # now adding user to database
            db.session.add(new_user) # ready to put it in the db
            db.session.commit() # put it in the db
            login_user(new_user,remember=True)
            flash("User created")
            return redirect(url_for("views.home"))
             
    return render_template("signup.html",user=current_user)

@auth2.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))