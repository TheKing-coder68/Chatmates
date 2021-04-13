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
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', None)
mongo = PyMongo(app)



@app.route("/")
def main():
    return render_template("servers.html")


@app.route("/create_server")
def create_server():
    if request.cookies.get('login_info'):  # Check to see if they are logged in
        login_info = json.loads(base64.b64decode(request.cookies.get('login_info')))  # Decode all that login information (the email_
        servers = mongo.db.servers  # Get the servers collection
        ids = [dict(server)['id'] for server in servers.find()]  # Create a list of all server ids using a list comp
        id = ''.join([random.choice([char for char in string.ascii_letters]) for _ in range(16)])  # Generate a random 16 letter ID
        while id in ids:  # While the ID already exists, create a new one
            id = ''.join([random.choice([char for char in string.ascii_letters]) for _ in range(16)])
        channel_ids = [channel_id for channel_id in [[channel['id'] for channel in server['channels']] for server in servers.find()]]
        # This bit of code above is quite a bitch. Basically, the inside is a list comp getting every server.
        # Then, the next inner bit, ([channel['id'] for channel in server]), is going through and getting the ID of every channel in every server.
        # Finally, the very beginning is putting every id of every server in a list.
        channel_id = ''.join([random.choice([char for char in string.ascii_letters]) for _ in range(16)])  # Generate a random 16 letter ID
        while channel_id in channel_ids:  # While the ID already exists, create a new one
            channel_id = ''.join([random.choice([char for char in string.ascii_letters]) for _ in range(16)])
        servers.insert_one({'name': request.args.get("name"), 'id': id,
                            'channels': [{'name': 'general', 'id': channel_id,
                                          'messages': []}],
                            'members': [{'email': login_info['email'], 'nickname': '',
                                         'messages': 0}],
                            'logo': ''})  # Create a document with all that collected information
        return 'done'  # Display 'done' to the page
    else:
        return redirect("/login")  # If they're not logged in, redirect them to the login page


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
        cookie = json.dumps({'email': email, 'username': request.form.get("username")})  # Create a json encoded key: value pair with their email
        cookie = cookie.encode()  # Encode the key: value pair into bytes
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
        cookie = json.dumps({'email': request.form.get('email').lower(), 'username': request.form.get("username")})
        cookie = cookie.encode()
        cookie = base64.b64encode(cookie)
        response.set_cookie('login_info', cookie, max_age=172800)
        return response
    return render_template("login.html")



if __name__ == "__main__":
    app.run(debug=True, port=5002)
