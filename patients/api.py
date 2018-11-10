""" Patients API """
import logging
from flask.views import MethodView
from flask import jsonify, request
from patients.handle_patients import register_patient, login_patient

class PatientsAPI(MethodView):
    """ Main API Body """
    logger = logging.getLogger(__name__)

    @staticmethod
    def get():
        """ Handle the get request

        Returns:
            json: Return the news then accessed
        """
        return jsonify({'patients': 'Patients API'}), 200

    @staticmethod
    def get_patient_data(patient_info):
        """ Get the main information from the patient

            Args:
                patient_info(dict): Information of the patient
        """
        name = patient_info.get("name")
        last_name = patient_info.get("last_name")
        ss_num = patient_info.get("ss_num")
        ass_policy = patient_info.get("ass_policy")

        return name, last_name, ss_num, ass_policy

    def post(self):
        """ Handle the post request

        Call the api when the post request is entered by
        the user

        Returns:
            json: Response from the server with the news
                  result message
        """
        data = request.json
        self.logger.info("########## Patients API Called")
        self.logger.info(data)

        interaction = data.get("action")

        if not interaction:
            response = "Incorrect Information"
        else:
            if interaction == "REGISTER":
                name, last_name, ss_num, ass_policy = self.get_patient_data(data)

                if not name or not last_name or not ss_num or not ass_policy:
                    response = "Missing Information"
                else:
                    response = register_patient(name, last_name, ss_num, ass_policy)

            if interaction == "LOGIN":
                response = login_patient(data.get("ss_num"))


        return jsonify(response), 201
