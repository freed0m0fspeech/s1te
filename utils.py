# import configparser
import os

from plugins.DataBase.mongo import (
    MongoDataBase
)


class DataBases:
    def __init__(self):
        self.mongodb_client = self.__get_mongodb_client()

    @staticmethod
    def __get_mongodb_client():
        # configParser = configparser.ConfigParser()
        # configParser.read('config.ini')

        # MONGODATABASE_USER = configParser['mongodb']['MONGODATABASE_USER']
        # MONGODATABASE_PASSWORD = configParser['mongodb']['MONGODATABASE_PASSWORD']
        # MONGODATABASE_HOST = f"{configParser['mongodb']['MONGODATABASE_HOST']}?retryWrites=true&w=majority"

        MONGODATABASE_USER = os.getenv('MONGODATABASE_USER', '')
        MONGODATABASE_PASSWORD = os.getenv('MONGODATABASE_PASSWORD', '')
        MONGODATABASE_HOST = os.getenv('MONGODATABASE_HOST', '')

        # 'host': "mongodb+srv://%s:%s@%s" % (quote_plus(configParser['mongodb']['MONGODATABASE_USER']),
        # quote_plus(configParser['mongodb']['MONGODATABASE_PASSWORD']),
        # configParser['mongodb']['MONGODATABASE_HOST'])

        # db_handle = client['db_name']

        # client
        return MongoDataBase(host=MONGODATABASE_HOST, user=MONGODATABASE_USER, passwd=MONGODATABASE_PASSWORD)


dataBases = DataBases()
mongoDataBase = dataBases.mongodb_client
