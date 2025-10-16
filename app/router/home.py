from http.cookiejar import Cookie
import os
from flask import Blueprint, flash,render_template,redirect,request,url_for,session
from ..models.model import User
import pandas as pd
import pickle
from flask_mail import Mail, Message
from .. import mail, db, current_app

home_bp=Blueprint("home",__name__)

@home_bp.route("/")
def home():
    return render_template("home.html")

@home_bp.route("/model")
def models():
    if session["email"]:
        print("yes")
        return render_template("model.html")
    else:
        return redirect(url_for("auth.login"))

@home_bp.route("/house_loan",methods=["GET","POST"])
def house_loan():
    if session["email"]:
        if request.method=="POST":
            gender=request.form.get("gender")
            married=request.form.get("married")
            dependents=int(request.form.get("dependents"))
            education=request.form.get("education")
            Self_Employed=request.form.get("Self_Employed")
            ApplicantIncome=int(request.form.get("ApplicantIncome"))
            CoapplicantIncome=int(request.form.get("CoapplicantIncome"))
            LoanAmount=int(request.form.get("LoanAmount"))
            Loan_Amount_Term=int(request.form.get("Loan_Amount_Term"))
            Credit_History=int(request.form.get("Credit_History"))
            Property_Area=request.form.get("Property_Area")
            Applicant_Age=int(request.form.get("Applicant_Age"))
            Existing_Liabilities=int(request.form.get("Existing_Liabilities"))

            data = {
            "Gender": gender,
            "Married": married,
            "Dependents": dependents,
            "Education": education,
            "Self_Employed": Self_Employed,
            "ApplicantIncome": ApplicantIncome,
            "CoapplicantIncome": CoapplicantIncome,
            "LoanAmount": LoanAmount,
            "Loan_Amount_Term": Loan_Amount_Term,
            "Credit_History": Credit_History,
            "Property_Area": Property_Area,
            "Applicant_Age": Applicant_Age,
            "Existing_Liabilities": Existing_Liabilities
            }

            x=pd.DataFrame([data])
            model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "home_model.pkl")

            with open (model_path,"rb") as f:
                model=pickle.load(f)

            pred=int(model.predict(x)[0])
            print("model prediction is",pred)
            session["pred"]=pred

            return render_template("result.html",pred=pred)


        return render_template("house_loan.html")
    else:
        return redirect(url_for("auth.login"))
    

@home_bp.route("/next_steps", methods=["GET","POST"])
def next_steps():
    if request.method == "POST":
        result = session.get("pred", 0)
        user = User.query.filter_by(username=session["email"]).first()
        recipient_email = [session["email"]]  # must be a list

        if result == 0:
            # Loan denied
            msg = Message(
                subject="Update on Your Loan Application",
                sender="sourav177official@gmail.com",
                recipients=recipient_email
            )
            msg.body = f"""
Dear {user},

We appreciate your recent application for a loan with [Your Company Name]. After careful review, we regret to inform you that we are unable to approve your loan request at this time.

This decision was made based on our internal evaluation criteria. Please understand that this is not a reflection on your personal standing, and you are welcome to apply again in the future if your circumstances change.

If you would like more information or guidance regarding your application, please do not hesitate to contact us at abcbank@gmail.com / 643453646456.

Sincerely,
Mohit Roy
Loan provider
"""
            mail.send(msg)

        else:
            # Loan approved
            msg = Message(
                subject="Your Loan Application Has Been Approved",
                sender="sourav177official@gmail.com",
                recipients=recipient_email
            )
            msg.body = f"""
Dear {user},

We are pleased to inform you that your loan application with [Your Company Name] has been approved.

Our team will proceed with the necessary steps to process your loan. You will receive further instructions and details regarding the disbursement and repayment schedule shortly.

If you have any questions or need assistance, please do not hesitate to contact us at abcbank@gmail.com / 643453646456.

Sincerely,
Mohit Roy
Loan provider
"""
            mail.send(msg)

        return render_template("next_steps.html")
    return render_template("next_steps.html")

@home_bp.route("/general_loan", methods=["GET", "POST"])
def general_loan():
    if session["email"]:
        if request.method == "POST":
            # receive form data
            data = {
                "Gender": request.form.get("gender"),
                "Married": request.form.get("married"),
                "Dependents": int(request.form.get("dependents")),
                "Education": request.form.get("education"),
                "Self_Employed": request.form.get("self_employed"),
                "LoanAmount": float(request.form.get("loan_amount")),
                "Loan_Amount_Term": int(request.form.get("loan_amount_term")),
                "Credit_History": int(request.form.get("credit_history")),
                "Property_Area": request.form.get("property_area"),
                "CIBIL_Score": float(request.form.get("cibil_score")),
                "Income_Type": request.form.get("income_type"),
                "Loan_Purpose": request.form.get("loan_purpose"),
                "Existing_Liabilities": float(request.form.get("existing_debts")),
                "Applicant_Age": int(request.form.get("age")),
                "ApplicantIncome": float(request.form.get("family_income")),
                "CoapplicantIncome":float(request.form.get("CoapplicantIncome"))
            }
            x=pd.DataFrame([data])
            model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "home_model.pkl")
            with open (model_path,"rb") as f:
                model=pickle.load(f)
            pred=int(model.predict(x)[0])

            return render_template("result.html",pred=pred)
        return render_template("general_form.html")
@home_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404