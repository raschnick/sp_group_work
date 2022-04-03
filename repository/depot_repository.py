import json
from collections import namedtuple

from pymongo.database import Database

from model.depot_dbo import DepotDbo


class DepotRepository:
    db: Database

    def __init__(self, db: Database):
        self.db = db

    def get_depot_by_depot_id(self, depot_id: int) -> dict:
        try:
            depot_dict = self.db.depot.find_one({"depot_id": int(depot_id)})
            if depot_dict is not None:
                return depot_dict
            else:
                return dict()
        except (ValueError, TypeError):
            return dict()
