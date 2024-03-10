from pymongo import MongoClient
import json


class DataUpdate:
    dbConn = 0
    db = 0

    def __init__(self):
        self.dbConn = MongoClient('localhost', 27017, username='admin', password='AdmiN')
        self.db = self.dbConn["WSO_bank"]
        self.collection = self.db["clients"]

    def __del__(self):
        self.dbConn.close()

    # check if pin for given cardId is valid
    # cardId - int value
    # pin - int value
    def checkId(self, cardId, pin):
        query = self.collection.find_one({"auth.cardId": cardId})
        if query is None:
            return False

        if query["auth"]["pin"] == pin:
            return True
        else:
            return False

    # return client name and current client balance
    # cardId - int value
    def getAccountInfo(self, cardId):
        query = self.collection.find_one({"auth.cardId": cardId})
        if query is None:
            return {"success": False, "error": "Not Found"}
        data = {"success": True, "client": query["client"], "balance": query["balance"]}
        return data

    # return client balance
    # cardId - int value
    def getAccountBalance(self, cardId):
        query = self.collection.find_one({"auth.cardId": cardId})
        if query is None:
            return {"success": False, "error": "Not Found"}
        data = {"success": True, "balance": query["balance"]}
        return data

    # update balance by given value
    # cardId - int value
    # value - int/double value
    def updateBalance(self, cardId, value, opType):
        query = self.collection.find_one({"auth.cardId": cardId})
        if query is None:
            return {"success": False, "error": "Not Found"}

        money = query["balance"]

        if opType == "in":
            money = money + value
        elif opType == "out":
            if money - value > 0:
                money = money - value
            else:
                return {"success": False, "error": "low balance"}
        else:
            return {"success": False, "error": "unknown operation"}

        self.collection.update_one({"auth.cardId": cardId}, {"$set": {"balance": money}})

        return {"success": True, "error": "no"}
