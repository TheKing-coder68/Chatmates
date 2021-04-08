from flask import Flask, make_response, jsonify, request, render_template, redirect, session
from flask_pymongo import PyMongo
import json, os, dotenv, base64, re, argon2, random, string
from argon2 import PasswordHasher
from flask_cors import CORS
from cryptography.fernet import Fernet
from datetime import timedelta

app = Flask(__name__)
<<<<<<< HEAD
app.permanent_session_lifetime=timedelta(minutes=5)
=======
dotenv.load_dotenv()
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', None)
mongo = PyMongo(app)



>>>>>>> 1f0bc3775c2e3813aeae452f224393c615701e28
@app.route("/")
def main():
    return "main route"

@app.route("/signup", methods=["POST","GET"])
def signup():
    if request.method=="POST":
        session.permanent= True
        first_name = request.form["FirstName"]
        session["first_name"] = first_name
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
