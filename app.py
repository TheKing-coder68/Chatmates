from flask import Flask, make_response, jsonify, request, render_template, redirect, session
from flask_pymongo import PyMongo
import json, os, dotenv, base64, re, argon2, random, string
from argon2 import PasswordHasher
from flask_cors import CORS
from cryptography.fernet import Fernet
from datetime import timedelta

app = Flask(__name__)
dotenv.load_dotenv()
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', None)
mongo = PyMongo(app)



@app.route("/")
def main():
    return "main route"


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":  # Check to make sure it's a post
        login = mongo.db.login  # Get the login collection
        email = request.form.get("email").lower()  # Get the person's email
        if not re.search('^[^@ ]+@[^@ ]+\.[^@ .]{2,}$', email):  # Check to make sure they entered a valid email
            return render_template("signup.html", error="Please enter a valid email")  # Return an error message if they didn't (will be implemented later)
        if login.find_one({'email': email}) is not None:  # Make sure their email does not already exist
            return render_template('signup.html', error='This email is already associated with an account')  # Return an error message if it does
        login.insert_one({"firstName": request.form.get("firstName"), "lastName": request.form.get("lastName"),
                          "email": email, "username": request.form.get("username")})  # Create a new document in the login database with all their info
        return render_template("index.html")
    return render_template("signup.html")  # If none of the other stuff happens, take them to the sign up page


if __name__ == "__main__":
    app.run(debug=True, port=5002)
