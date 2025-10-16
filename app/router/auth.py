from flask import Blueprint, flash, render_template, redirect, request, url_for, session, current_app
from ..models.model import User
from .. import db, mail
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("pass")
        password2 = request.form.get("pass2")

        if not (username and email and password and password2):
            flash("Please fill all required fields", "warning")
            return render_template("signup.html")
            
        if password != password2:
            flash("Passwords do not match", "danger")
            return render_template("signup.html")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered", "warning")
            return render_template("signup.html")

        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("DB commit failed: %s", e)
            flash("Could not create user. Maybe email already exists?", "danger")
            return render_template("signup.html")

        # Send welcome email
        try:
            msg = Message(subject="Welcome to AetherCorp",
                          recipients=[email])
            msg.body = f"Hi {username},\n\nThanks for signing up!"
            mail.send(msg)
        except Exception as e:
            current_app.logger.exception("Failed to send welcome email: %s", e)

        flash("Your account has been created successfully", "success")
        return redirect(url_for("home.models"))

    return render_template("signup.html")


@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not (email and password):
            flash("Please provide both email and password", "warning")
            return render_template("login.html")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user"] = user.username
            session["email"] = user.email
            flash("Login successful!", "success")
            return redirect(url_for("home.models"))  # Replace with your actual home endpoint
        else:
            flash("Incorrect email or password", "danger")

    return render_template("login.html")
