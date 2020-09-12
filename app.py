from flask import Flask
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "apiuser": "typingtool"
}


@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username


@app.route('/')
#@auth.login_required
def hello_world():
        return f'Hello, {auth.current_user()}'
