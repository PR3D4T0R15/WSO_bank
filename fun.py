from pymongo import MongoClient


class DataUpdate:
    dbConn = 0
    db = 0

    def __init__(self):
        self.dbConn = MongoClient('localhost', 27017, username='admin', password='AdmiN')
        self.db = self.dbConn['WSO_bank']
        self.collection = self.db['clients']

    def __del__(self):
        self.dbConn.close()

    def checkId(self, cardId, pin):
        query = self.collection.find_one({"auth.cardId": cardId})
        if query['auth']['pin'] == pin:
            return True
        else:
            return False

    def getInfo(self, cardId):
        query = self.collection.find_one({"auth.cardId": cardId})
        data = {'client': query['client'], 'balance': query['balance']}
        return data

    def updateBalance(self, cardId, value):
        query = self.collection.find_one({"auth.cardId": cardId})

        money = query['balance']
        money = money + value

        self.collection.update_one({"auth.cardId": cardId}, {"$set": {"balance": money}})
