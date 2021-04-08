from flask import Flask, make_response, jsonify, request, render_template, redirect
from flask_pymongo import PyMongo
import json, os, dotenv, base64, re, argon2, random, string
from argon2 import PasswordHasher
from flask_cors import CORS
from cryptography.fernet import Fernet

app = Flask(__name__)
dotenv.load_dotenv()
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', None)
mongo = PyMongo(app)



@app.route("/")
def main():
    return "main route"




if __name__ == "__main__":
    app.run()
