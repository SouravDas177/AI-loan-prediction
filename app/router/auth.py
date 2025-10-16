from flask import Blueprint, flash, render_template, redirect, request, url_for, session, current_app
from ..models.model import User
from .. import db
from flask_mail import Message
from .. import mail


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        print("done")
        username = request.form.get("username") 
        email = request.form.get("email")
        password = request.form.get("pass") 
        password2 = request.form.get("pass2") 
        print("done1")
        if not (email and password and password2):
            flash("Please fill all required fields", "warning")
            return render_template("signup.html")
            
        if password != password2:
            flash("Passwords do not match", "danger")
            return render_template("signup.html")
        print("done3")
        user = User(username=username , email=email, password=password)

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("DB commit failed: %s", e)
            flash("Could not create user. Maybe email already exists?", "danger")
            return render_template("signup.html")

        # send welcome email (optional — wrap in try/except so DB success isn't blocked)
        try:
            msg = Message(subject="Welcome to AetherCorp",
                          recipients=[email])
            msg.body = f"Hi {username or email.split('@')[0]},\n\nThanks for signing up!"
            mail.send(msg)
        except Exception as e:
            current_app.logger.exception("Failed to send welcome email: %s", e)

        flash("Your account has been created successfully", "success")
        return redirect("/")  # or url_for("home.<endpoint>")

    return render_template("signup.html")



@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password:
            user = User.query.filter_by(email=email).first()

            if user:
                if user.password == password:
                    session["user"] = user.username
                    session["email"] = user.email
                    flash("Login successful!", "success")
                    return redirect(url_for("home.models"))   # <- changed from url_for("home.models")
                else:
                    flash("Incorrect password", "danger")
            else:
                flash("No account found with that email", "warning")
                return render_template("login.html")  # <- show login page, not signup

    return render_template("login.html")

