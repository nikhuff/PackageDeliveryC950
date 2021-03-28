from maps import *

# Global variables to simulate database
maps = Maps()

class Route:
    def __init__(self, size):
        self.packages = list()
        self.size = size

    def add_package(self, package):
        if self.get_size() < self.size:
            self.packages.append(package)
            return True
        else:
            return False

    def remove_package(self, id):
        self.packages[:] = [keep for keep in self.packages if not keep.get_id() == id]

    def add_front(self, package):
        self.packages.insert(0, package)

    def get_size(self):
        return len(self.packages)

    def get_last_address(self):
        return self.packages[-1].get_address()

    def get_packages(self):
        return self.packages

class Truck:
    """Truck class used to carry information regarding the trucks"""
    def __init__(self, capacity, truck_num, time):
        global maps
        self.truck_num = truck_num
        self.capacity = capacity
        self.distance_traveled = 0
        self.route = list()
        self.speed = 18.0 # mph
        self.time = time
        self.location = 0 # start at WGU 
        self.destination = 0 # not going anywhere yet

    def get_distance_traveled(self):
        return self.distance_traveled

    def get_distance_next(self):
        return maps.get_distance(self.location, self.destination)

    def get_capacity(self):
        return self.capacity

    def set_route(self, route):
        self.route.append(route)

    def deliver(self):
        # add distance traveled
        distance = self.get_distance_next()
        self.distance_traveled += distance
        # increment time
        time_traveled = distance / self.speed
        self.time += time_traveled
        # previous destination is now location
        self.location = self.destination

    def wait(self):
        # if you're here before packages arrive, wait
        if self.time < 9.09:
            self.time = 9.10

    def set_next_destination(self, route, package_status):
        closest = (100.0, 0)
        for package in route.get_packages():
            address_index = maps.get_address_index(package.get_address())
            distance = maps.get_distance(self.location, address_index)
            if distance < closest[0]:
                closest = (distance, address_index, package.get_id())
        self.destination = closest[1]
        route.remove_package(closest[2])
        return package_status.get_package(closest[2])

    def start_route(self, package_status):
        # deliver the packages in the list
        for route in self.route:
            for package in route.get_packages():
                package_status.add_truck_timestamp(package.get_id(), self.time)
            while route.get_size() > 0:
                package = self.set_next_destination(route, package_status)
                if package.get_id() == 9:
                    if self.time > 10.4:
                        package_status.update_address(9, '410 S State St')
                    if package_status.get_package(9).get_address() == '300 State St':
                        self.time +=.05
                        route.add_front(package)
                        continue
                self.deliver()
                package_status.add_timestamp(package.get_id(), self.time)
                package_status.add_delivery_truck(package.get_id(), self.truck_num)
            # after current route is over, go back to WGU
            self.destination = 0
            self.deliver()

class RoutingStation:
    """Class used for all things routing"""
    def __init__(self, package_status):
        global maps
        self.package_status = package_status
        self.route1 = Route(16)
        self.route2 = Route(16)
        self.route3 = Route(16)
        self.truck1 = Truck(16, 1, 8)
        self.truck2 = Truck(16, 2, 9.1)
        self.all_packages = list()
        self.deadline_packages = list()

    def load_trucks(self):
        route_1 = [14, 15, 16, 34, 20, 21, 19, 1, 7, 29, 37, 30, 13, 39, 27, 35]
        route_2 = [25, 26, 22, 24, 28, 4, 40, 31, 32, 17, 6, 36, 12, 18, 23, 11]
        route_3 = [2, 33, 10, 5, 38, 8, 9, 3]

        for i in route_1:
            self.route1.add_package(self.package_status.get_package(i))
        for i in route_2:
            self.route2.add_package(self.package_status.get_package(i))
        for i in route_3:
            self.route3.add_package(self.package_status.get_package(i))

        self.truck1.set_route(self.route1)
        self.truck2.set_route(self.route2)
        self.truck2.set_route(self.route3)

    def start(self):
        total_distance = 0
        self.truck1.start_route(self.package_status)
        self.truck2.start_route(self.package_status)
        total_distance = self.truck1.get_distance_traveled() + self.truck2.get_distance_traveled()
        return total_distance

if __name__ == '__main__':
    package_status = data.create_package_table()
    route = RoutingStation(package_status)
    route.load_trucks()
    total_distance = route.start()
    package_status.display_package_status(20)
    print("Total Distance Traveled: %.2f" % total_distance)
    
