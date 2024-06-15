from configparser import ConfigParser
import json
import mysql.connector
import uuid
import hashlib
import random


def generateAccuntNumber():
    account_number = ""

    for i in range(1, 2, 1):
        account_number = account_number + str(random.randint(0, 9))
    account_number = account_number + "20434589"
    for i in range(1, 16, 1):
        account_number = account_number + str(random.randint(0, 9))

    return account_number


def checkAuthString(authStringFromDevice):
    config = ConfigParser()
    config.read('config.ini')
    authStringSaved = config['Authorization']['authString']

    if authStringFromDevice == authStringSaved:
        return True
    else:
        return False


def generateUuid():
    nameSpace = uuid.NAMESPACE_DNS
    name = "session"
    return str(uuid.uuid5(nameSpace, name))


def hashPassword(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verifyPin(cardID, pin):
    db = DataUpdate()
    pnFromDb = db.getPin(cardID)

    if pnFromDb == pin:
        return True
    else:
        return False


def getAction(jsonDic):
    return jsonDic['action']


def getData(jsonDict):
    return jsonDict['data']


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

    # create user session
    def createSession(self, cardID, sessionId):
        sql = "INSERT INTO RaspBank.sessions (uuid, cardid) VALUES (%s, %s);"
        val = (sessionId, cardID)
        self.cursor.execute(sql, val)
        self.connection.commit()

        if self.cursor.rowcount == 1:
            return True
        else:
            return False

    # delete user session
    def deleteSession(self, token):
        sql = "DELETE FROM RaspBank.sessions WHERE uuid = %s;"
        val = [token]
        self.cursor.execute(sql, val)
        self.connection.commit()

        if self.cursor.rowcount == 1:
            return True
        else:
            return False

    # create new user
    def checkSession(self, cardID):
        sql = "SELECT sessions.uuid FROM RaspBank.sessions WHERE cardId = %s;"
        val = [cardID]
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()

        if self.cursor.rowcount == 1:
            return True
        else:
            return False

    # get pin form database
    def getPin(self, cardID):
        sql = "SELECT Users.pin FROM RaspBank.Users WHERE cardId=%s;"
        val = [cardID]
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()

        if self.cursor.rowcount == 1:
            return result[0][0]
        else:
            return ""

    # change pin
    def changePin(self, cardID, pin):
        sql = "UPDATE RaspBank.Users SET Users.pin=%s WHERE cardId=%s;"
        val = [pin, cardID]
        self.cursor.execute(sql, val)
        self.connection.commit()

    # create new account (name, surname, pin, carId, phone, balance)
    def createAccount(self, data):
        sql = "INSERT INTO RaspBank.Users (name, surname, pin, cardId, phone, balance) VALUES (%s, %s, %s, %s, %s, %s);"
        val = data
        self.cursor.execute(sql, val)
        self.connection.commit()

        if self.cursor.rowcount == 1:
            return True
        else:
            return False


class RaspBank:
    _action = {}
    _data = {}

    def __init__(self, requestJson):
        self._action = getAction(json.loads(requestJson))
        self._data = getData(json.loads(requestJson))

    def loginUser(self):
        db = DataUpdate()

        carId = self._data['cardId']
        pin = self._data['pin']

        response = {"action": "login-resp"}

        if not verifyPin(carId, pin):
            dataJson = {"ACK": "false", "reason": "Invalid PIN"}
            responseJson = {"action": "login-resp", "data": dataJson}
            return json.dumps(responseJson)

        if db.checkSession(carId):
            dataJson = {"ACK": "false", "reason": "session exists"}
            responseJson = {"action": "login-resp", "data": dataJson}
            return json.dumps(responseJson)

        token = generateUuid()
        if db.createSession(carId, token):
            dataJson = {"ACK": "true", "token": token}
            responseJson = {"action": "login-resp", "data": dataJson}
            return json.dumps(responseJson)

        dataJson = {"ACK": "false", "reason": "unknow error"}
        responseJson = {"action": "login-resp", "data": dataJson}
        return json.dumps(responseJson)

    def logoutUser(self):
        db = DataUpdate()

        token = self._data['token']

        response = {"action": "logout-resp"}

        if db.deleteSession(token):
            dataJson = {"ACK": "true", "reason": "session deleted"}
            responseJson = {"action": "logout-resp", "data": dataJson}
            return json.dumps(responseJson)

        dataJson = {"ACK": "false", "reason": "no session"}
        responseJson = {"action": "logout-resp", "data": dataJson}
        return json.dumps(responseJson)
