# import configparser
import os
import freedom_of_speech.utils
import portfolio.utils

from plugins.DataBase.mongo import (
    MongoDataBase
)
from dotenv import load_dotenv

load_dotenv()


class DataBases():

    def __init__(self):
        self.mongodb_client = self.__get_mongodb_client()

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(DataBases, cls).__new__(cls)
    #     return cls.instance

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


class Cache():
    def __init__(self, databases: DataBases):
        self.freedom_of_speech = freedom_of_speech.utils.update_cached_data(databases.mongodb_client)
        self.portfolio = portfolio.utils.update_cached_data(databases.mongodb_client)


dataBases = DataBases()
cache = Cache(dataBases)
# mongoDataBase = dataBases.mongodb_client
