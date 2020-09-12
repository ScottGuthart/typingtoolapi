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
                 4: [0, 1],
                 5: [1, 2, 3, 4, 5, 6],
                 6: [1, 2, 3, 4, 5, 6],
                 7: [0, 1],
                 8: [0, 1],
                 9: [1, 2, 3, 4, 5, 6],
                 10: [0, 1],
                 11: [0, 1],
                 12: [0, 1],
                 13: [0, 1],
                 14: [0, 1],
                 15: [0, 1],
                 16: [0, 1]}

coef = genfromtxt('coefficients.csv', delimiter=',')
print('Running with coef:', coef)

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

def validate_request(r):
    response = ''
    values = []
    for variable in valid_levels:
        if type(r) == str:
            if variable <= len(r):
                level = r[variable-1]
            else:
                level = None
        else:
            level = r.args.get(str(variable))
        if level:
            if level.isnumeric:
                level = int(level)
                if level in valid_levels[variable]:
                    response += f'{level},'
                    values.append(level)
                else:
                    response += (
                        f'{variable}: must be in
                        [{" ".join(valid_levels[variable])}],'
                    )
            else:
                response += f'{variable}: must be numeric,'
        else:
            response += f'{variable}: no data received,'
    if len(values) == len(valid_levels.keys()):
        return values, response
    return None, response

def get_segment(resp):
    resp.append(1)
    resp = np.array(resp)
    print(resp)
    return (coef @ resp).argmax()+1


@app.route('/<r>')
#@auth.login_required
def api(r=None):
    if r is None:
        values, response = validate_request(request)
    else:
        values, response = validate_request(r)
    if values:
        return str(get_segment(values))
    else:
        return response
