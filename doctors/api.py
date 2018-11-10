""" EventsAPI """
import logging
from flask.views import MethodView
from flask import jsonify, request
import users.handle_users as USERS

class DoctorAPI(MethodView):
    """ Main API Body """
    logger = logging.getLogger(__name__)

    #def __init__(self):
    #    if (request.method != 'GET') and not request.json:
    #        abort(400)

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
        response = "Null"


        data = request.json
        self.logger.info("########## Events API Called")
        self.logger.info(data)

        testing_param = data.get('type')

        return jsonify({
            'users': response
        }), 201
