""" Views form flask framework """
from flask import Blueprint
from patients.api import PatientsAPI

PATIENTS_APP = Blueprint('users_app', __name__)
PATIENTS_VIEW = PatientsAPI.as_view('users_api')

PATIENTS_APP.add_url_rule('/patients/',
                          view_func=PATIENTS_VIEW,
                          methods=['GET', ])

PATIENTS_APP.add_url_rule('/patients/search_patients',
                          view_func=PATIENTS_VIEW,
                          methods=['POST', ])
