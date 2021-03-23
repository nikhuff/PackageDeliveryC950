# Nicholas Huff 003860221

if __name__ == '__main__':
    # process data from csv
    distances = DataProcessing.createDistanceTable()
    addresses = DataProcessing.createAddressList()
    packageStatus = DataProcessing.createPackageHash()

    # route trucks
    truck1, truck2 = RoutingStation.routeTrucks()

    # start delivery
    truck1.startRoute()
    truck2.startRoute()

    # display total mileage
    totalDistance = truck1.getDistanceTraveled() + truck2.getDistanceTraveled()

    # display package data at given time
    displayPackageStatus(time)
