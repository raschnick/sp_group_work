import json
import os

from pymongo import MongoClient
from pymongo.database import Database


class DbService:
    db: Database

    def __init__(self):
        self.connect_db()
        self.setup_db()

    def connect_db(self) -> None:
        client = MongoClient(
            "mongodb://eglisi1:sEjNOlADMCVRNwmb@cluster0-shard-00-00.mkt3y.mongodb.net:27017,cluster0-shard-00-01.mkt3y.mongodb.net:27017,cluster0-shard-00-02.mkt3y.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-46zapx-shard-0&authSource=admin&retryWrites=true&w=majority")
        self.db = client['portfolio_management']

    def setup_db(self):
        if self.get_amount_documents() == 0:
            self.insert_sample_data()

    def get_amount_documents(self, collection: str = 'depot') -> int:
        return self.db[collection].find().count()

    def insert_sample_data(self):
        collections = ['currency', 'depot', 'transaction']
        dirname = os.path.dirname(__file__)
        for collection in collections:
            filename = os.path.join(dirname, f'../unit_tests/data/{collection}.json')
            f = open(filename)
            data = json.load(f)
            f.close()
            self.db[collection].insert_many(data)