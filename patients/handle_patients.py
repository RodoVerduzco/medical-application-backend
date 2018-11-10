from pymongo import MongoClient
import config

CLIENT = MongoClient(config.DB_URI,
                     connectTimeoutMS=30000,
                     socketTimeoutMS=None,
                     socketKeepAlive=True)
DATABASE = CLIENT.get_default_database()
collection = DATABASE.patients

def register_patient(name, last_name, ss_num, ass_policy):
    """register_patient
    Calls the DBHelper to insert the patient into the database

    Args:
        name           (string):  Name of the patient
        last_name      (string):  Last Name of the patient
        ss_num         (string):  Social Security Number
        ass_policy     (string):  Assurance policy

    Returns:
        string: Confirmation Message
    """

    collection.insert({
        "name": name,
        "last_name": last_name,
        "ss_num": ss_num,
        "ass_policy": ass_policy,
    })

    return {"Patient":"Registered Patient"}

def login_patient(ss_num):
    """login_patient
    Calls the DBHelper to login the patient

    Args:
        ss_num(string):  Social Security Number to be looked for
    Returns:
        dict: information about the patient
    """

    data = collection.find_one({"ss_num": ss_num}, {'_id': 0})

    return data
