class DepotDbo:
    depot_id: int
    depot_holder_name: str

    def __init__(self, depot_dict):
        if len(depot_dict) > 0:
            for key in depot_dict:
                setattr(self, key, depot_dict[key])
        else:
            self.depot_id = -1
            self.depot_holder_name = 'None'

    def __repr__(self):
        return f"Depot (depot_id: {self.depot_id}, depot_holder_name: '{self.depot_holder_name}')"
