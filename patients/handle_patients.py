from pymongo import MongoClient
import config
from datetime import datetime
from bson.json_util import dumps
from flask import jsonify

CLIENT = MongoClient(config.DB_URI,
                     connectTimeoutMS=30000,
                     socketTimeoutMS=None,
                     socketKeepAlive=True)
DATABASE = CLIENT.get_default_database()
collection = DATABASE.patients

def check_previous_prescriptions(ss_num):
    prescriptions = []
    data_found = collection.find({"ss_num":ss_num}, { '_id':0})
    #prescs = jsonify(data_found)
    #print(data_found['prescriptions'])
    #print(prescs)
    for individual in data_found:
        prescriptions = individual["prescriptions"]

    if(not prescriptions):
        print("No prescriptions")
    else:
        for element in prescriptions:
            element["status"] = "INACTIVE"

    #pres_ordered =[]
    sorted_date = sorted(prescriptions, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d-%H-%M-%S'),reverse=True)
  
    collection.update({"ss_num":ss_num},{"$set":{"prescriptions":sorted_date}})
            
        #if individual['status']

   

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
    if data:
            return {
                "login": "true",
                "data": data
            }
    elif not data:
        return {"login": "false"}

def add_prescription(ssn,patient_name, doctor_name, sickness,
                     diagnose, drug, p_card, interval, duration):

    check_previous_prescriptions(ssn)
    """ Add the prescription to the selected patient

    Args:
        ss_num(string):  Social Security Number to be looked for
    Returns:
        dict: information about the patient
    """

    prescription_info = {
        "date": datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),
        "doctor": doctor_name,
        "professional_card": p_card,
        "sickness": sickness,
        "diagnose": diagnose,
        "drug": drug,
        "duration": duration,
        "interval": interval,
        "status": "ACTIVE",
        "symptoms": []
    }
    #print(prescription_info['date'])
    data = collection.find_one({"name": patient_name}, {'_id': 0})
    if data:
        collection.update({'name': patient_name}, {'$push': {'prescriptions': prescription_info}})
        
        data_found = collection.find({"ss_num":ssn}, { '_id':0})
        prescriptions =[]
        for individual in data_found:
            prescriptions = individual["prescriptions"]
        sorted_date = sorted(prescriptions, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d-%H-%M-%S'),reverse=True)
        collection.update({"ss_num":ssn},{"$set":{"prescriptions":sorted_date}})
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

def terminate_treatment(ss_num):
    prescriptions = []
    data_found = collection.find({"ss_num":ss_num}, { '_id':0})
    for individual in data_found:
        prescriptions = individual["prescriptions"]

    if(not prescriptions):
        print("No prescriptions")
    else:
        for element in prescriptions:
            element["status"] = "INACTIVE"

    #pres_ordered =[]
    sorted_date = sorted(prescriptions, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d-%H-%M-%S'), reverse=False)   
    collection.update({"ss_num":ss_num},{"$set":{"prescriptions":prescriptions}})

    return "Treatment ended"

def get_patient(ss_num):
    data = collection.find_one({"ss_num": ss_num}, {'_id': 0})

    return data

def find_prescription_patient(ss_num,date):
    data = collection.find_one({"ss_num": ss_num}, {'_id': 0})
    prescriptions = data['prescriptions']

    for element in prescriptions:
        if element['date'] ==date:
            return element
    return "not_found"

def modify_prescription(ssn,sickness, diagnose, drug, interval, duration,date):
    
    data = collection.find_one({"ss_num": ssn}, {'_id': 0})
    prescriptions = data['prescriptions']

    for element in prescriptions:
        if element['date'] ==date:
            element['duration'] = duration
            element['interval'] = interval
            element['drug'] = drug
            element['diagnose'] = diagnose
            element['sickness'] = sickness

    collection.update({"ss_num":ssn},{"$set":{"prescriptions":prescriptions}})

    return "success"

def get_prescriptions_patient(ss_num):
    data = collection.find_one({"ss_num": ss_num}, {'_id': 0})
    
    return data["prescriptions"]
