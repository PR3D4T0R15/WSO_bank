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
        for x in self.collection.find({"auth.cardId": cardId}):
            if x['auth']['pin'] == pin:
                return True
            else:
                return False

    def updateBalance(self, balance):
        pass
