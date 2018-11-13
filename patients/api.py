""" Patients API """
import logging
from flask.views import MethodView
from flask import jsonify, request
from patients.handle_patients import register_patient, login_patient, add_prescription, get_active,\
                                    get_inactive, update_status, get_prescriptions_patient, get_patient, \
                                    check_previous_prescriptions, terminate_treatment, find_prescription_patient, \
                                    modify_prescription

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
        ss_num = patient_info.get("ss_num")
        ass_policy = patient_info.get("ass_policy")

        return name, ss_num, ass_policy

    @staticmethod
    def get_prescription_data(prescription_info):
        """ Get the main information from the patient

            Args:
                prescription_info(dict): Information of the prescription and patient
        """
        ssn = prescription_info.get("ssn")
        patient_name = prescription_info.get("patient_name")
        doctor_name = prescription_info.get("doctor_name")
        sickness = prescription_info.get("sickness")
        diagnose = prescription_info.get("diagnose")
        drug = prescription_info.get("drug")
        p_card = prescription_info.get("p_card")
        interval = prescription_info.get("interval")
        duration = prescription_info.get("duration")

        return ssn, patient_name, doctor_name, sickness, diagnose, drug, p_card, interval, duration


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

        if not interaction or not data:
            response = "Incorrect Information"
        else:
            # Register a new patient
            if interaction == "REGISTER":
                name, ss_num, ass_policy = self.get_patient_data(data)

                if not name or not ss_num or not ass_policy:
                    response = "Missing Information"
                else:
                    response = register_patient(name, ss_num, ass_policy)

            # Login the Patient
            if interaction == "LOGIN":
                ssn = data.get('user')
                if ssn :
                    response = {"Patient": login_patient(ssn)}
                else:
                    response = {"Patient": "Missing data"}

            if interaction == "TERMINATE":
                ssn = data.get("ssn")
                if ssn:
                    response = {"Patient": terminate_treatment(ssn)}
                else:
                    response = {"Patient":"Missing Information"}

            if interaction == "MODIFY_PRESCRIPTION":
                ssn = data.get("ssn")
                date = data.get("date")
                sickness = data.get("sickness")
                diagnose = data.get("diagnose")
                drug = data.get("drug")
                interval = data.get("interval")
                duration = data.get("duration")

                if not ssn or not sickness or not diagnose\
                   or not drug  or not interval or not duration:
                    response = "Missing Information"
                else:
                    response = {"Patient": modify_prescription(ssn,  sickness,
                                                diagnose, drug,  interval, duration,date)}

            # Add a medical prescription
            if interaction == "ADD_PRESCRIPTION":
                # Get the prescription data
                ssn, patient_name, doctor_name, sickness \
                , diagnose, drug, p_card, interval, duration = self.get_prescription_data(data)

                # Add the prescription
                if not ssn or not patient_name or not doctor_name or not sickness or not diagnose\
                   or not drug or not p_card or not interval or not duration:
                    response = "Missing Information"
                else:
                    response = add_prescription(ssn, patient_name, doctor_name, sickness,
                                                diagnose, drug, p_card, interval, duration)

            # Get the active/inactive
            if interaction == "GET":
                if data.get("user_type") == "active":
                    response = get_active()
                elif data.get("user_type") == "inactive":
                    response = get_inactive()
                else:
                    response = "Invalid Option"
            
            if interaction == "TERMINATE_TREATMENT":
                ss_num = data.get("ss_num")
                if ss_num is None:
                    response = {"Patient":"Missing information"}
                else:
                    response = jsonify(terminate_treatment(ss_num))

            # Update status
            if interaction == "UPDATE_STATUS":
                ss_num = data.get('ss_num')
                status = data.get('status')

                if ss_num and status:
                    response = update_status(ss_num, status)
                else:
                    response = {"Patient": "Missing Information"}
            
            if interaction == "SELECT_PRESCRIPTION":
                ss_num = data.get('ss_num')
                date = data.get("date")
                if ss_num and date:
                    response = find_prescription_patient(ss_num, date)
                else:
                    response = {"Patient":"Missing Information"}

            if interaction == "GET_PRESCRIPTION":
                ss_num = data.get('ss_num')
                #date = data.get("date")
                if ss_num:
                    response = get_prescriptions_patient(ss_num)
                else:
                    response = {"Patient": "Missing Information"}
            if interaction == "GET_PATIENT":
                ss_num = data.get('ss_num')
                if ss_num:
                    response = get_patient(ss_num)
                else:
                    response = {"Patient": "Missing Information"}

        return jsonify(response), 201
