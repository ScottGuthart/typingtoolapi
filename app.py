from flask import Flask, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "apiuser": "typingtool"
}


inputs = {
    "s9" : {
        'valid': [1,2,3,4,5]
    }
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username


@app.route('/')
#@auth.login_required
def hello_world():
    response = ''
    valid_submission = True
    for variable in inputs:
        level = request.args.get(variable)
        if level:
            if level.isnumeric:
                level = int(level)
                if level in inputs[variable]['valid']:
                    response += f'{variable}={level},'
                else:
                    response += (
                        f'{variable}: must be in {inputs[variable]["valid"]},'
                    )
                    valid_submission = False
            else:
                response += f'{variable}: must be numeric,'
                valid_submission = False
        else:
            response += f'{variable}: no data received,'
            valid_submission = False
    return response
