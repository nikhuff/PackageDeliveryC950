from data import *

# Global variables to simulate database
data = DataProcessing('assets/DistanceCSV.csv', 'assets/PackageCSV.csv')

class Maps:
    def __init__(self):
        global data
        self.distance_table = data.create_distance_table()
        self.address_dict = data.create_address_dict()

    def get_address_index(self, address):
        return self.address_dict.get(address)
    
    def get_distance(self, location, destination):
        # get distance between two points
        distance = self.distance_table[location][destination]
        # because of how data is stored, might need to swap
        if not distance:
            distance = self.distance_table[destination][location]

        return distance