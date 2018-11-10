"""DBHelper

This dbhelper is in charge of every interaction to be done with the database in mongo
"""
from pymongo import MongoClient
import config

class DBHelper:
    """ DBHelper Class """

    def __init__(self):
        CLIENT = MongoClient(config.DB_URI,
                             connectTimeoutMS=30000,
                             socketTimeoutMS=None,
                             socketKeepAlive=True)
        DATABASE = CLIENT.get_default_database()
        self.collection = DATABASE    
