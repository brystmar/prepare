import uuid

from flask import Flask, abort, request
from flask_cors import CORS

from database.DatabaseDAO import DatabaseDAO

app = Flask(__name__)
CORS(app)

DATABASE_FLAT_FILE_PATH = "./database/DatabaseFlatFile.json"
database_dao = DatabaseDAO(DATABASE_FLAT_FILE_PATH)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/user/<string:user_id>', methods=["GET"])
def get_public_user_data(user_id):
    return database_dao.get_user(user_id)


@app.route('/user/<string:user_id>', methods=["POST"])
def put_public_user_data(user_id):
    if not request.json:
        abort(400)

    print(request.json)

    user = request.json
    user["id"] = user_id

    database_dao.put_user(user_id, user)


@app.route('/user/', methods=["POST"])
def generate_id_and_put_public_user_data():
    new_random_user_id = str(uuid.uuid4())
    put_public_user_data(new_random_user_id)
    return str(uuid.uuid4())

@app.route('/evacadvice/', methods=["GET"])
def get_evac_advice():
    print("get_evac_advice_called, request.args is:")
    print(request.args);
    advice_map = {'421 Harmony Street New Orleans, LA 70115': 'SHELTER IN PLACE',
                  '711 Congress St, New Orleans, LA 70117': 'EVACUATE NOW',
                  '140 Oakmont Dr, New Orleans, LA 70128': 'PREPARE TO EVACUATE',
                  '937 France St, New Orleans, LA 70117': 'YOU ARE SAFE'}
    if request.args is None or request.args.get("address") is None:
        advice = None
    else:
        advice = advice_map.get(request.args.get("address"))

    if advice == None:
        return "PREPARE TO EVACUATE"
    else:
        return advice
