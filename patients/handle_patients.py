from pymongo import MongoClient
import config

CLIENT = MongoClient(config.DB_URI,
                     connectTimeoutMS=30000,
                     socketTimeoutMS=None,
                     socketKeepAlive=True)
DATABASE = CLIENT.get_default_database()
collection = DATABASE.patients

def register_patient(name, ss_num, ass_policy):
    """register_patient
    Calls the DBHelper to insert the patient into the database

    Args:
        name           (string):  Name of the patient
        ss_num         (string):  Social Security Number
        ass_policy     (string):  Assurance policy

    Returns:
        string: Confirmation Message
    """

    collection.insert({
        "name": name,
        "ss_num": ss_num,
        "ass_policy": ass_policy,
        "status": "ACTIVE",
        "prescriptions": []
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

def add_prescription(date, patient_name, doctor_name, sickness,
                     diagnose, drug, p_card, interval, duration):
    """ Add the prescription to the selected patient

    Args:
        ss_num(string):  Social Security Number to be looked for
    Returns:
        dict: information about the patient
    """

    prescription_info = {
        "date": date,
        "doctor": doctor_name,
        "professional_card": p_card,
        "sickness": sickness,
        "diagnose": diagnose,
        "drug": drug,
        "duration": duration,
        "interval": interval,
        "symptoms": []
    }
    data = collection.find_one({"name": patient_name}, {'_id': 0})
    if data:
        collection.update({'name': patient_name}, {'$push': {'prescriptions': prescription_info}})
        response = {"Patient": "Added prescription correctly"}
    else:
        response = {"Patient": "Patient not registered"}

    return response

def get_active():
    data = list(collection.find({"status":"ACTIVE"}, {'_id': 0}))
    return data

def get_inactive():
    data = list(collection.find({"status":"INACTIVE"}, {'_id': 0}))
    return data

def update_status(ss_num, status):
    data = collection.find_one({"ss_num": ss_num}, {'_id': 0})
    if data:
        collection.update({'ss_num': ss_num}, {"$set":{'status': status.upper()}})
        response = {"Patient": "Updated Status"}
    else:
        response = {"Patient": "Patient not registered"}
    return response

def get_prescriptions_patient(ss_num):
    data = collection.find_one({"ss_num": ss_num}, {'_id': 0})

    return data["prescriptions"]
