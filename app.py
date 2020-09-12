from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
import numpy as np
from numpy import genfromtxt

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "apiuser": "typingtool"
}


valid_levels = {1: [1, 2, 3, 4, 5, 6],
                 2: [1, 2, 3, 4, 5, 6],
                 3: [1, 2, 3, 4, 5, 6],
                 4: [1, 2, 3, 4, 5, 6],
                 5: [1, 2, 3, 4, 5, 6],
                 6: [1, 2, 3, 4, 5, 6],
                 7: [1, 2, 3, 4, 5, 6],
                 8: [1, 2, 3, 4, 5, 6],
                 9: [1, 2, 3, 4, 5, 6],
                 10: [0, 1],
                 11: [0, 1],
                 12: [0, 1],
                 13: [0, 1],
                 14: [0, 1],
                 15: [0, 1],
                 16: [0, 1]}

coef = genfromtxt('coefficients.csv')

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

def validate_request(r):
    response = ''
    for variable in valid_levels:
        level = r.args.get(str(variable))
        if level:
            if level.isnumeric:
                level = int(level)
                if level in valid_levels[variable]:
                    response += f'{variable}={level},'
                else:
                    response += (
                        f'{variable}: must be in {valid_levels[variable]},'
                    )
            else:
                response += f'{variable}: must be numeric,'
        else:
            response += f'{variable}: no data received,'
    return response


@app.route('/')
#@auth.login_required
def api():
    return validate_request(request)
