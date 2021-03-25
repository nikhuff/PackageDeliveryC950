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
        self.speed = 18.0 # mph
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

    def reload(self):
        self.destination = 0
        self.deliver()
        # if you're here before packages arrive, wait
        if self.time < 9.09:
            self.time = 9.10

    def start_route(self, package_status):
        # deliver the packages in the list
        while self.packages:
            package = self.packages.pop(0)
            if package == 0:
                self.reload()
                continue
            if package.get_id() == 9:
                if self.time > 10.4:
                    package_status.update_address(9, '410 S State St')
                if package_status.get_package(9).get_address() == '300 State St':
                    self.time +=.05
                    self.packages.insert(0, package)
                    continue
            next_address = package.get_address()
            self.destination = maps.get_address_index(next_address)
            self.deliver()
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

    def check_notes(self, package_notes):
        return {
            'Wrong address listed': 1,
            'Delayed on flight---will not arrive to depot until 9:05 am': 2,
            'Can only be on truck 2': 3,
            'Must be delivered with 15, 19': 4,
            'Must be delivered with 13, 19': 5,
            'Must be delivered with 13, 15': 6
        }.get(package_notes, 0)

    def load_trucks(self):
        truck1_packages = list()
        truck2_packages = list()
        all_packages = list()
        inital_position = 0
        # initialize closest to random highest
        closest1 = (100.0, 0)
        closest2 = (100.0, 0)
        for i in range(1, self.package_status.get_num_packages() + 1):
            all_packages.append(package_status.get_package(i))

        # split lists into zip codes
        # list of all possible zip codes we deliver to
        # zip_codes = [[84104], [84106], [84123], [84115], [84103], [84118], [84119], [84111], [84117], [84107], [84105], [84121]]
        
        # and find initial two closest packages
        for package in all_packages:
            # find closest packages
            address_index = self.maps.get_address_index(package.get_address())
            distance = self.maps.get_distance(inital_position, address_index)
            if distance < closest1[0]:
                closest2 = closest1
                closest1 = (distance, package.get_id())

        # start with the two closest packages
        truck2_packages.append(package_status.get_package(closest1[1]))
        truck1_packages.append(package_status.get_package(closest2[1]))

        # remove the two packages that have already been put in the delivery queue
        all_packages[:] = [package for package in all_packages if not package.get_id() == closest1[1]]
        all_packages[:] = [package for package in all_packages if not package.get_id() == closest2[1]]

        # helper variable for measuring distance from HQ
        at_hq1 = False
        at_hq2 = False
        has_refilled1 = False
        has_refilled2 = False


        while all_packages:
            # reset closest tuples
            closest1 = (100.0, 0)
            closest2 = (100.0, 0)
            # find next for truck 1
            for package in all_packages:
                # find closest packages
                address_index = self.maps.get_address_index(package.get_address())
                if at_hq1:
                    truck_index = 0
                else:
                    truck_index = self.maps.get_address_index(truck1_packages[-1].get_address())
                distance = self.maps.get_distance(truck_index, address_index)
                if distance < closest1[0]:
                    closest1 = (distance, package.get_id())
            
            # helper variable to determine if truck has stopped at HQ
            # look at special notes and change package if needed
            notes = self.check_notes(package_status.get_package(closest1[1]).get_notes())
            if notes == 0:
                # print("1.0")
                if len(truck1_packages) < 17 or has_refilled1:
                    truck1_packages.append(package_status.get_package(closest1[1]))
                    at_hq1 = False
                    all_packages[:] = [package for package in all_packages if not package.get_id() == closest1[1]]
                else:
                    truck1_packages.append(0)
                    has_refilled1 = True
                    at_hq1 = True
            elif notes == 1:
                # print("1.1")
                # don't add package until the very end
                if has_refilled1:
                    truck1_packages.append(package_status.get_package(closest1[1]))
                    at_hq1 = False
                    all_packages[:] = [package for package in all_packages if not package.get_id() == closest1[1]]
            elif notes == 2:
                # print("1.2")
                # don't add package until after truck goes back to refill
                if has_refilled1:
                    truck1_packages.append(package_status.get_package(closest1[1]))
                    at_hq1 = False
                    all_packages[:] = [package for package in all_packages if not package.get_id() == closest1[1]]
                # print("1.3")
            elif notes == 4:
                # print("1.4")
                # add package 13 14 15 16 19 20 with it
                for package in all_packages:
                    # find and add all associated packages
                    if package.get_id() in [13, 14, 15, 16, 19, 20] and (len(truck1_packages) < 11 or has_refilled1):
                        truck1_packages.append(package_status.get_package(package.get_id()))
                        at_hq1 = False
                        all_packages[:] = [extra for extra in all_packages if not extra.get_id() == package.get_id()]
                    else:
                        truck1_packages.append(0)
                        has_refilled1 = True
                        at_hq1 = True
            elif notes == 5:
                # print("1.5")
                # add package 13 14 15 16 19 20 with it
                for package in all_packages:
                    # find and add all associated packages
                    if package.get_id() in [13, 14, 15, 16, 19, 20] and (len(truck1_packages) < 11 or has_refilled1):
                        truck1_packages.append(package_status.get_package(package.get_id()))
                        at_hq1 = False
                        all_packages[:] = [extra for extra in all_packages if not extra.get_id() == package.get_id()]
                    else:
                        truck1_packages.append(0)
                        has_refilled1 = True
                        at_hq1 = True
            elif notes == 6:
                # print("1.6")
                # print(len(truck1_packages))
                # add package 13 14 15 16 19 20 with it
                for package in all_packages:
                    # find and add all associated packages
                    if package.get_id() in [13, 14, 15, 16, 19, 20] and (len(truck1_packages) < 11 or has_refilled1):
                        truck1_packages.append(package_status.get_package(package.get_id()))
                        at_hq1 = False
                        all_packages[:] = [extra for extra in all_packages if not extra.get_id() == package.get_id()]
                    else:
                        truck1_packages.append(0)
                        has_refilled1 = True
                        at_hq1 = True

            # find next for truck 2
            for package in all_packages:
                # find closest packages
                address_index = self.maps.get_address_index(package.get_address())
                if at_hq2:
                    truck_index = 0
                else:
                    truck_index = self.maps.get_address_index(truck2_packages[-1].get_address())
                distance = self.maps.get_distance(truck_index, address_index)
                if distance < closest2[0]:
                    closest2 = (distance, package.get_id())

            # helper variable to determine if truck has stopped at HQ
            # look at special notes and change package if needed
            notes = self.check_notes(package_status.get_package(closest2[1]).get_notes())
            if notes == 0:
                # print(2.0)
                if len(truck2_packages) < 17 or has_refilled2:
                    truck2_packages.append(package_status.get_package(closest2[1]))
                    at_hq2 = False
                    all_packages[:] = [package for package in all_packages if not package.get_id() == closest2[1]]
                else:
                    truck2_packages.append(0)
                    has_refilled2 = True
                    at_hq2 = True
            elif notes == 1:
                # print(2.1)
                # don't add package until address is updated
                # print(package_status.get_package(9).get_address())
                if has_refilled2:
                    truck2_packages.append(package_status.get_package(closest2[1]))
                    at_hq2 = False
                    all_packages[:] = [package for package in all_packages if not package.get_id() == closest2[1]]
            elif notes == 2:
                # print(2.2)
                # don't add package until after truck goes back to refill
                if has_refilled2:
                    truck2_packages.append(package_status.get_package(closest2[1]))
                    at_hq2 = False
                    all_packages[:] = [package for package in all_packages if not package.get_id() == closest2[1]]
            elif notes == 3:
                # print(2.3)
                # add package to this truck
                if len(truck2_packages) < 17 or has_refilled2:
                    truck2_packages.append(package_status.get_package(closest2[1]))
                    at_hq2 = False
                    all_packages[:] = [package for package in all_packages if not package.get_id() == closest2[1]]
                else:
                    truck2_packages.append(0)
                    has_refilled2 = True
                    at_hq2 = True
            elif notes == 4:
                # print(2.4)
                # add package 13 14 15 16 19 20 with it
                for package in all_packages:
                    # find and add all associated packages
                    if package.get_id() in [13, 14, 15, 16, 19, 20] and (len(truck2_packages) < 11 or has_refilled2):
                        truck2_packages.append(package_status.get_package(package.get_id()))
                        at_hq2 = False
                        all_packages[:] = [extra for extra in all_packages if not extra.get_id() == package.get_id()]
                    else:
                        truck2_packages.append(0)
                        has_refilled1 = True
                        at_hq2 = True
            elif notes == 5:
                # print(2.5)
                # add package 13 14 15 16 19 20 with it
                for package in all_packages:
                    # find and add all associated packages
                    if package.get_id() in [13, 14, 15, 16, 19, 20] and (len(truck2_packages) < 11 or has_refilled2):
                        truck2_packages.append(package_status.get_package(package.get_id()))
                        at_hq2 = False
                        all_packages[:] = [extra for extra in all_packages if not extra.get_id() == package.get_id()]
                    else:
                        truck2_packages.append(0)
                        has_refilled1 = True
                        at_hq2 = True
            elif notes == 6:
                # print(2.6)
                # print(len(truck2_packages))
                # add package 13 14 15 16 19 20 with it
                for package in all_packages:
                    # find and add all associated packages
                    if package.get_id() in [13, 14, 15, 16, 19, 20] and (len(truck2_packages) < 11 or has_refilled2):
                        truck2_packages.append(package_status.get_package(package.get_id()))
                        at_hq2 = False
                        all_packages[:] = [extra for extra in all_packages if not extra.get_id() == package.get_id()]
                    else:
                        truck2_packages.append(0)
                        has_refilled1 = True
                        at_hq2 = True

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
    print("Total Distance Traveled: %.2f" % total_distance)
    
