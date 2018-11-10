""" Views form flask framework """
from flask import Blueprint
from doctors.api import DoctorsAPI

DOCTORS_APP = Blueprint('doctors_app', __name__)
DOCTORS_VIEW = DoctorsAPI.as_view('doctors_api')

DOCTORS_APP.add_url_rule('/doctors/',
                         view_func=DOCTORS_VIEW,
                         methods=['GET', ])

DOCTORS_APP.add_url_rule('/doctors/search_doctors',
                         view_func=DOCTORS_VIEW,
                         methods=['POST', ])
