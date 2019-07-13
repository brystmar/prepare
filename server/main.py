import uuid

from flask import Flask, abort, request

from database.DatabaseDAO import DatabaseDAO

app = Flask(__name__)

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

