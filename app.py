from flask import Flask, make_response, jsonify, request, render_template, redirect, session, flash, url_for
from flask_pymongo import PyMongo
import json, os, dotenv, base64, re, argon2, random, string
from argon2 import PasswordHasher
from flask_cors import CORS
from cryptography.fernet import Fernet
from datetime import timedelta

app = Flask(__name__)
dotenv.load_dotenv()
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', None)
app.config['SECRET_KEY'] = "23435khhdajk983hagsdh134dsda745112dsfksa93assd0sas8s"
mongo = PyMongo(app)



@app.route("/")
def main():
    return "main route"


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":  # Check to make sure it's a post
    
        login = mongo.db.login  # Get the login collection
    
        email = request.form.get("email").lower()  # Get the person's email

        password= request.form.get("password")  # Get the person's password
        username= request.form.get("username")  # Get the person's username
        
        if len(password)<8:
            flash("That password is not secure, please try another one.") #Flashes this msg if the password is shorter than 8 characters
        if len(username) < 3:
            flash("Thats username is not long enough, please try again")
        if not re.search('^[^@ ]+@[^@ ]+\.[^@ .]{2,}$', email):  # Check to make sure they entered a valid email

            flash("The Email that you entered is not valid, please try again.")  # Return an error message if they didn't (will be implemented later)

        if login.find_one({'email': email}) is not None:  # Make sure their email does not already exist
            
            flash("This email is already associated with an account.")  # Return an error message if it does
            return redirect('/signup')

        login.insert_one({"firstName": request.form.get("firstName"), "lastName": request.form.get("lastName"),

                          "email": email, "username": request.form.get("username"),

                          "password": request.form.get("password")})  # Create a new document in the login database with all their info
        response = make_response(render_template("index.html"))  # Create a response object of the rendered website HTML
        cookie = json.dumps({'email': email})  # Create a json encoded key: value pair with their email
        cookie = str.encode(cookie)  # Encode the key: value pair into bytes
        cookie = base64.b64encode(cookie)  # base64 encode the cookie to make it more secure
        response.set_cookie('login_info', cookie,max_age=172800)  # Set the cookie to the website and make it expire after 2 days for security
        return response  # Return our response object, solidifying the cookie creation and showing the page to the user.
    return render_template("signup.html")  # If none of the other stuff happens, take them to the sign up page


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        login = mongo.db.login
        if not login.find_one({"email": request.form.get("email").lower()}):
            flash("This email is not associated with an account.")
            return render_template("login.html")
        if not login.find_one({"email": request.form.get("email").lower(), "password": request.form.get("password")}):
            flash("Incorrect password.")
            return render_template("login.html")
        response = make_response(render_template("index.html"))
        cookie = json.dumps({'email': request.form.get('email').lower()})
        cookie = str.encode(cookie)
        cookie = base64.b64encode(cookie)
        response.set_cookie('login_info', cookie, max_age=172800)
        return response
    return render_template("login.html")



if __name__ == "__main__":
    app.run(debug=True, port=5002)
