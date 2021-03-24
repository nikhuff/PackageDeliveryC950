from hash import HashTable
import datetime

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
        self.timestamp = None

    # set the timestamp only when the package is delivered
    def set_timestamp(self, time):
        self.timestamp = time

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
        return self.timestamp



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

    def get_package(self, key):
        return self.packages.search(key)

    def display_package_status(self, time):
        print("Package ID\tAddress\t\tStatus")
        for i in range(1, self.num_packages + 1):
            current_package = self.packages.search(i)
            print(str(current_package.get_id()) + "\t\t" + current_package.get_address() + "\t", end="")
            # if timestamp is none, undelivered
            if not current_package.get_timestamp():
                print("Undelivered")
            # if current package timestamp is less than time given, it has been delivered
            elif current_package.get_timestamp() < time:
                print("Delivered at " + str(datetime.timedelta(hours=current_package.get_timestamp()))[:-3])
            else:
                print("Undelivered")
            