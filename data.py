import csv
from package import *

class DataProcessing:
    """Class used to read data from CSV tables"""
    def __init__(self, distances_url, packages_url):
        self.distances_url = distances_url
        self.packages_url = packages_url

    def create_distance_table(self):
        # create table to return
        distance_table = list()

        # open the csv where data is
        with open(self.distances_url) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # count which row we are in
            row_count = 0
            for row in csv_reader:
                # create the row to append to distance list
                distance_table_row = list()
                # we don't want anything in the first row
                if row_count > 0:
                    # the string in each column
                    for string in row:
                        # we only want the data starting in column 2
                        if row.index(string) > 1:
                            # convert the data to a double only if there is data to convert
                            if string:
                                distance_table_row.append(float(string))
                            # if the string is empty, put a None type as placeholder
                            else:
                                distance_table_row.append(None)
                    # append the row to the table
                    distance_table.append(distance_table_row)
                # keep track of the row we're in
                row_count += 1
        # return the completed distance table
        return distance_table

    def create_address_dict(self):
        # create list to return
        address_list = dict()

        # open the csv where data is
        with open(self.distances_url) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            row_count = 0
            for row in csv_reader:
                # we don't want anything in the first two rows
                if row_count > 1:
                    # the string in each column
                    for string in row:
                        # we only want the data in column 1
                        if row.index(string) == 1:
                            # assign address values for lookup later
                            address_list.update({string.strip().split('\n')[0]: row_count - 1})
                # keep track of the row we're in
                row_count += 1
        # return the completed address list
        return address_list

    def create_package_table(self):
        # create list to return
        package_list = list()

        # open csv where data is
        with open(self.packages_url) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # package id, address, city, state, zip, deadline, mass, notes
            for row in csv_reader:
                # change EOD to 0.0 so all same data type
                if row[5] == 'EOD':
                    deadline = 0.0
                else:
                    deadline = float(row[5])
                # create package object from row data
                package = Package(int(row[0]), row[1], row[2], row[3], int(row[4]), deadline, int(row[6]), row[7])
                # insert package object to list
                package_list.append(package)

        # create PackageStatus hash
        package_status = PackageStatus(package_list)

        # return PackageStatus
        return package_status

if __name__ == '__main__':
    data = DataProcessing('assets/DistanceCSV.csv', 'assets/PackageCSV.csv')
    distance_table = data.create_distance_table()
    address_dict = data.create_address_dict()
    print(address_dict)
    package_status = data.create_package_table()
    package_status.display_package_status(17)

