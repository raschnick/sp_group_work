from pymongo.database import Database


class DepotRepository:
    db: Database

    def __init__(self, db: Database):
        self.db = db

    def get_depot_by_depot_id(self, depot_id: str) -> dict:
        try:
            depot_cursor = self.db.depot.aggregate([
                {
                    '$match': {
                        'depot_id': int(depot_id)
                    }
                }, {
                    '$lookup': {
                        'from': 'transaction',
                        'localField': 'depot_id',
                        'foreignField': 'depot_id',
                        'as': 'transactions'
                    }
                }
            ])
            try:
                return depot_cursor.next()
            except StopIteration:
                return dict()
        except (ValueError, TypeError):
            return dict()
