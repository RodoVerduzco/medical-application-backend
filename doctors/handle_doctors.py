from pymongo import MongoClient
import config

CLIENT = MongoClient(config.DB_URI,
                     connectTimeoutMS=30000,
                     socketTimeoutMS=None,
                     socketKeepAlive=True)
DATABASE = CLIENT.get_default_database()
collection = DATABASE.doctor

def login_doctor(user, password):
    """login_patient
    Calls the DBHelper to login the doctor

    Args:
        user     (string):  doctor user (email)
        password (string):  doctor password
    Returns:
        dict: information about the patient
    """
    response = {"Login Failed": "Incorrect Data"}

    print(user)
    print(password)

    data = collection.find_one({'email': user}, {'_id': 0})

    if data.get('password') == password:
        response = {"Successful Login": data}

    return response
