import uuid

from flask import Flask, abort, request
from flask_cors import CORS

from database.DatabaseDAO import DatabaseDAO
from database.MockUserGenerator import generate_mock_users
from NotificationProxy import send_sms
from credentials.Twilio import TEST_SMS_NUMBER

app = Flask(__name__, static_folder="static", static_url_path='')  
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

    # NOTIFY USER
    str(send_sms(TEST_SMS_NUMBER, 'You have bee added to to PREPARE. Visit http://prepare.org/user/' + user_id))


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
    advice_map = {'4301-4499 Eastview Dr New Orleans, LA 70126': 'SHELTER IN PLACE',
                  '501 Robert E Lee Blvd New Orleans, LA 70124': 'EVACUATE NOW',
                  '405 Livingston Ave Arabi, LA 70032': 'PREPARE TO EVACUATE',
                  '2816-2714 Deer Creek Dr Violet, LA 70092': 'YOU ARE SAFE'}
    if request.args is None or request.args.get("address") is None:
        advice = None
    else:
        advice = advice_map.get(request.args.get("address"))

    if advice is None:
        return "PREPARE TO EVACUATE"
    else:
        return advice

@app.route('/shelteradvice/', methods=["GET"])                                                                    
def get_shelter_advice():                                                                                         
    print("get_shelter_advice_called, request.args is:")                                                          
    print(request.args)                                                                                           
    shelteradvice_map = {'4301-4499 Eastview Dr New Orleans, LA 70126': 'Planet Fitness',                         
                         '501 Robert E Lee Blvd New Orleans, LA 70124': 'Ochsner Health Center',                  
                         '405 Livingston Ave Arabi, LA 70032': 'Walmart Supercenter',                             
                         '2816-2714 Deer Creek Dr Violet, LA 70092': 'St. Bernard Parish Hospital'}               
    if request.args is None or request.args.get("address") is None:                                               
        shelteradvice = None                                                                                      
    else:                                                                                                         
        shelteradvice = shelteradvice_map.get(request.args.get("address"))                                        
                                                                                                                  
    if shelteradvice is None:                                                                                     
        return "Ochsner Health Center"                                                                            
    else:                                                                                                         
        return shelteradvice                                                                                      


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

@app.route('/send_test_message/', methods=["GET"])
def send_test_sms():
    return str(send_sms(TEST_SMS_NUMBER, 'TEST MESSAGE'))
