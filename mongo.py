import json
from collections import namedtuple
from dataclasses import dataclass
from random import randint
from types import SimpleNamespace

from pymongo import MongoClient
from pymongo.database import Database


@dataclass
class Rating:
    name: str
    rating: int


def connect(db: str) -> Database:
    client = MongoClient(
        "mongodb://eglisi1:sEjNOlADMCVRNwmb@cluster0-shard-00-00.mkt3y.mongodb.net:27017,cluster0-shard-00-01.mkt3y.mongodb.net:27017,cluster0-shard-00-02.mkt3y.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-46zapx-shard-0&authSource=admin&retryWrites=true&w=majority")
    return client[db]


def insert_sample_data(db: Database, amount: int = 500) -> None:
    names = ['Kitchen', 'Animal', 'State', 'Tastey', 'Big', 'City', 'Fish', 'Pizza', 'Goat', 'Salty', 'Sandwich',
             'Lazy', 'Fun']
    company_type = ['LLC', 'Inc', 'Company', 'Corporation']
    company_cuisine = ['Pizza', 'Bar Food', 'Fast Food', 'Italian', 'Mexican', 'American', 'Sushi Bar', 'Vegetarian']
    for x in range(1, amount + 1):
        business = {
            'name': names[randint(0, (len(names) - 1))] + ' ' + names[randint(0, (len(names) - 1))] + ' ' +
                    company_type[
                        randint(0, (len(company_type) - 1))],
            'rating': randint(1, 5),
            'cuisine': company_cuisine[randint(0, (len(company_cuisine) - 1))]
        }

        # Step 3: Insert business object directly into MongoDB via insert_one
        result = db.reviews.insert_one(business)

        # Step 4: Print to the console the ObjectID of the new document
        print(f'Created {x} of 500 as {result.inserted_id}')

        # Step 5: Tell us that you are done
        print(f'finished creating {amount} business reviews')


def get_amount_documents(db: Database) -> int:
    return db.reviews.find().count()


def get_example(db) -> None:
    fivestar = db.reviews.find_one({'rating': 5})
    print(fivestar)

    x = json.loads(fivestar, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    print(f'name: {x.name}, rating: {x.rating}')


if __name__ == '__main__':
    db = connect('business')
    amount_documents = get_amount_documents(db)
    print(amount_documents)
    if amount_documents < 500:
        insert_sample_data(db, 500)
    get_example(db)
