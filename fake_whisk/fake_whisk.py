import uuid
from functools import wraps
import flask
import json
from pop_service.__main__ import main as pop_main
from ga_service.__main__ import main as ga_main

dic = {}
app = flask.Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return flask.Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = flask.request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/api/v1/namespaces/guest/actions/popService', methods=['POST'])
@requires_auth
def pop_service():
    if flask.request.method == 'POST':
        activation_id =  str(uuid.uuid1())
        dic[activation_id] = pop_main(flask.request.get_json())
        return json.dumps({ "activationId":  activation_id })

@app.route('/api/v1/namespaces/guest/actions/gaService', methods=['POST'])
@requires_auth
def ga_service():
    if flask.request.method == 'POST':
        activation_id =  str(uuid.uuid1())
        dic[activation_id] = ga_main(flask.request.get_json())
        return json.dumps({ "activationId":  activation_id })

@app.route('/api/v1/namespaces/guest/activations/<activation_id>', methods=['GET'])
@requires_auth
def get_activation(activation_id):
    if flask.request.method == 'GET':
        print(activation_id)
        return json.dumps({"response": { "result":  dic[activation_id]}})

app.run()
