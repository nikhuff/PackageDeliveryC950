# Nicholas Huff 003860221

from package import *
from routing import *
from data import *

if __name__ == '__main__':
    package_status = data.create_package_table()
    routing_station = RoutingStation(package_status)
    routing_station.load_trucks()
    total_distance = routing_station.start()
    print("Total Distance Traveled: %.2f" % total_distance)
    while True:
        time = input('What time would you like to view (military)? (type "quit" to quit):')
        if time == 'quit':
            break
        else:
            try:
                time = float(time)
            except:
                print("Please enter a valid input")
                continue
            package_status.display_package_status(time)
