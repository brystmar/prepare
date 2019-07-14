import uuid

from flask import Flask, abort, request
from flask_cors import CORS

from database.DatabaseDAO import DatabaseDAO
from database.MockUserGenerator import generate_mock_users


app = Flask(__name__)
CORS(app)

DATABASE_FLAT_FILE_PATH = "./database/DatabaseFlatFile.json"
DATABASE_DUMP_CSV_FILEPATH = "./database/DatabaseFlatFile.csv"
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

    print("POST to /user/<id>")
    print(request.json)

    user = request.json
    user["id"] = user_id

    database_dao.put_user(user_id, user)


@app.route('/user/', methods=["POST"])
def generate_id_and_put_public_user_data():
    print("POST to /user")
    print(request.json)

    new_random_user_id = str(uuid.uuid4())
    put_public_user_data(new_random_user_id)
    return new_random_user_id


@app.route('/evacadvice/', methods=["GET"])
def get_evac_advice():
    print("get_evac_advice_called, request.args is:")
    print(request.args)
    advice_map = {'421 Harmony Street New Orleans, LA 70115': 'SHELTER IN PLACE',
                  '711 Congress St, New Orleans, LA 70117': 'EVACUATE NOW',
                  '140 Oakmont Dr, New Orleans, LA 70128': 'PREPARE TO EVACUATE',
                  '937 France St, New Orleans, LA 70117': 'YOU ARE SAFE'}
    if request.args is None or request.args.get("address") is None:
        advice = None
    else:
        advice = advice_map.get(request.args.get("address"))

    if advice is None:
        return "PREPARE TO EVACUATE"
    else:
        return advice


@app.route('/generate_mock_user/<int:number_of_users>', methods=["GET"])
def generate_users(number_of_users):
    mocked_users = generate_mock_users(number_of_users)
    for user_id in mocked_users:
        database_dao.put_user(user_id, mocked_users.get(user_id))
    return "Generate Users: " + str(number_of_users)


@app.route('/export_database/', methods=["GET"])
def dump_database_to_csv():
    database_dao.export_to_csv(DATABASE_DUMP_CSV_FILEPATH)
    return "Database Dumped to" + DATABASE_DUMP_CSV_FILEPATH
