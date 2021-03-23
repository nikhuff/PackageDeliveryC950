from hash import HashTable

class Package:
    """Package class used to define the notion of a package"""
    def __init__(self, id, address, city, state, zip, deadline, mass, notes, timestamp):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.notes = notes
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
        for i in self.num_packages:
            self.packages.insert(package_list[i].get_id, package_list[i])
        

    def add_timestamp(self, id, time):
        package = self.packages.search(id)
        package.set_timestamp(time)
        self.packages.insert(id, package)

    def display_package_status(self, time):
        print("Package ID\tStatus")
        for i in self.num_packages:
            current_package = self.packages.search(i)
            print(current_package.get_id() + "\t", end="")
            # if current package timestamp is less than time given, it has been delivered
            if current_package.get_timestamp() < time:
                print("Delivered at " + self.packages.search(i).get_timestamp())
            else:
                print("Undelivered")
            