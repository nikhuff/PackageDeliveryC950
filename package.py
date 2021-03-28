from hash import HashTable
import datetime
from tabulate import tabulate

class Package:
    """Package class used to define the notion of a package"""
    def __init__(self, id, address, city, state, zip, deadline, mass, notes):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.notes = notes
        # all packages start undelivered, minimum time can leave is 8am
        self.delivery_timestamp = None
        self.truck_timestamp = None
        self.delivery_truck = None

    # set the timestamp only when the package is delivered
    def set_timestamp(self, time):
        self.delivery_timestamp = time

    def set_truck_timestamp(self, time):
        self.truck_timestamp = time

    def set_delivery_truck(self, truck):
        self.delivery_truck = truck

    def set_address(self, address):
        self.address = address

    def get_id(self):
        return self.id
    
    def get_address(self):
        return self.address
    
    def get_city(self):
        return self.city
    
    def get_state(self):
        return self.state
    
    def get_zip(self):
        return self.zip
    
    def get_deadline(self):
        return self.deadline

    def get_mass(self):
        return self.mass

    def get_notes(self):
        return self.notes

    def get_timestamp(self):
        return self.delivery_timestamp

    def get_truck_timestamp(self):
        return self.truck_timestamp

    def get_delivery_truck(self):
        return self.delivery_truck


class PackageStatus:
    """Class used to track status of packages throughout the simulation"""
    def __init__(self, package_list):
        # initialize hash table to size of amount of packages
        self.num_packages = len(package_list)
        self.packages = HashTable(self.num_packages)
        for package in package_list:
            self.packages.insert(package.get_id(), package)

    def add_timestamp(self, id, time):
        package = self.packages.search(id)
        package.set_timestamp(time)
        self.packages.insert(id, package)

    def add_truck_timestamp(self, id, time):
        package = self.packages.search(id)
        package.set_truck_timestamp(time)
        self.packages.insert(id, package)
   
    def add_delivery_truck(self, id, delivery_truck):
        package = self.packages.search(id)
        package.set_delivery_truck(delivery_truck)
        self.packages.insert(id, package)

    def update_address(self, id, new_address):
        package = self.packages.search(id)
        package.set_address(new_address)
        self.packages.insert(id, package)

    def get_package(self, key):
        return self.packages.search(key)

    def get_num_packages(self):
        return self.num_packages

    def display_package_status(self, time):
        data = []
        for i in range(1, self.num_packages + 1):
            current_package = self.packages.search(i)
            delivery_status = str()
            if not current_package.get_timestamp():
                delivery_status = "Undelivered"
            # if current package timestamp is less than time given, it has been delivered
            elif current_package.get_timestamp() < time:
                delivery_status = "delivered at " + str(datetime.timedelta(hours=current_package.get_timestamp()))[:-3]
            elif current_package.get_truck_timestamp() < time:
                delivery_status = "en route"
            else:
                delivery_status = "at the hub"
            data.append([current_package.get_id(), current_package.get_address(), current_package.get_delivery_truck(), delivery_status])
            # if timestamp is none, undelivered
        print (tabulate(data, headers=["Package ID", "Address", "Truck #", "Status"], numalign="left"))
            