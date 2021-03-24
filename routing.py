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
    

class Truck:
    """Truck class used to carry information regarding the trucks"""
    def __init__(self, packages, maps):
        self.distance_traveled = 0
        self.maps = maps
        self.packages = packages
        self.speed = 18 # mph
        self.time = 8.0 # am
        self.location = 0 # start at WGU 
        self.destination = 0 # not going anywhere yet

    def get_distance_traveled(self):
        return self.distance_traveled

    def get_distance_next(self):
        return maps.get_distance(self.location, self.destination)

    def deliver(self):
        # add distance traveled
        distance = self.get_distance_next()
        self.distance_traveled += distance
        # increment time
        time_traveled =  distance / self.speed
        self.time += time_traveled
        # previous destination is now location
        self.location = self.destination

    def start_route(self, package_status):
        # deliver the packages in the list
        while self.packages:
            self.deliver()
            package = self.packages.pop()
            next_address = package.get_address()
            self.destination = maps.get_address_index(next_address)
            package_status.add_timestamp(package.get_id(), self.time)
        # one more delivery to return to WGU
        self.destination = 0
        self.deliver()



class RoutingStation:
    """Class used for all things routing"""
    def __init__(self, package_status, maps):
        self.maps = maps
        self.package_status = package_status
        self.truck1 = None
        self.truck2 = None

    def load_trucks(self):
        truck1_packages = list()
        truck2_packages = list()
        for i in range(1, 21):
            truck1_packages.append(package_status.get_package(i))
        for i in range(21, 41):
            truck2_packages.append(package_status.get_package(i))
        self.truck1 = Truck(truck1_packages, self.maps)
        self.truck2 = Truck(truck2_packages, self.maps)

    def start(self):
        self.truck1.start_route(self.package_status)
        self.truck2.start_route(self.package_status)
        total_distance = self.truck1.get_distance_traveled() + self.truck2.get_distance_traveled()
        return total_distance

if __name__ == '__main__':
    package_status = data.create_package_table()
    maps = Maps()
    route = RoutingStation(package_status, maps)
    route.load_trucks()
    total_distance = route.start()
    package_status.display_package_status(20)
    print("Total Distance Traveled: " + str(total_distance))
    
