""" EventsAPI """
import logging
from flask.views import MethodView
from flask import jsonify, request
from doctors.handle_doctors import login_doctor
import json

class DoctorsAPI(MethodView):
    """ Main API Body """
    logger = logging.getLogger(__name__)

    @staticmethod
    def get():
        """ Handle the get request

        Returns:
            json: Return the news then accessed
        """
        return jsonify({'doctor': 'Doctor API'}), 200

    def post(self):
        """ Handle the post request

        Call the api when the post request is entered by
        the user

        Returns:
            json: Response from the server with the news
                  result message
        """

        data = request.json
        self.logger.info("########## Doctors API Called")
        self.logger.info(data)

        interaction = data.get('action')

        if not interaction:
            response = {"login": "false"}
        else:
            if interaction == "LOGIN":
                response = login_doctor(data.get('user'), data.get('password'))

        return jsonify(response), 201
