from configparser import ConfigParser
import json
import mysql.connector


def checkAuthString(authStringFromDevice):
    config = ConfigParser()
    config.read('config.ini')
    authStringSaved = config['Authorization']['authString']

    if authStringFromDevice == authStringSaved:
        return True
    else:
        return False


class DataUpdate:
    connection = None
    cursor = None

    def __init__(self):
        config = ConfigParser()
        config.read('config.ini')
        db_host = config['Database']['host']
        db_user = config['Database']['user']
        db_password = config['Database']['password']
        db_database = config['Database']['database']

        self.connection = mysql.connector.connect(host=db_host, user=db_user, passwd=db_password, database=db_database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        del self.cursor
        del self.connection

    def userLogin(self):
        pass

    def userLogout(self):
        pass

    def userNew(self):
        pass

    def accountBalance(self):
        pass

    def accountUpdateBalance(self):
        pass

    def accountChangePin(self):
        pass