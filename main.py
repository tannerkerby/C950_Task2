# ALGORITHM
from Package import Package
from Truck import Truck
from CSVReader import *
from HashTable import HashTable
from datetime import datetime, timedelta


# Creating empty HashMap for packages
myHashTable = HashTable()


def load_package_data(filename):
    with open(filename) as package_info:
        package_data = csv.reader(package_info, delimiter=',')
        next(package_data)
        for package in package_data:

            if package[0]:  # Check if package_ID is not empty
                package_ID = int(package[0])
            else:
                # Handle empty package_ID
                continue    # Skip this row and move to the next one

            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDeadline_time = package[5]
            pWeight = package[6]
            pSpecialNotes = package[7]
            pStatus = "At Hub"

            # Package object assembly for each row in the CSV
            p = Package(package_ID, pAddress, pCity, pState, pZipcode, pDeadline_time, pWeight, pSpecialNotes, pStatus)

            # Insert each package object into hash table
            myHashTable.insert(package_ID, p)
        return myHashTable


# Instantiating the 3 truck loads with their respective packages.
truck1_packages = []
truck2_packages = []
truck3_packages = []

truck1 = Truck("HUB", truck1_packages, timedelta(hours = 8, minutes = 0), "8:00 AM")

print(truck1.package)


# Function to calculate the distance between 2 nodes in the distance table CSV file.
def distanceBetween(address1, address2):
    load_distance_data('DistanceTable.csv')
    distance = data[address1][address2]
    return distance


# User Interface When Program Starts
if __name__ == '__main__':
    print("\nWGUPS Delivery Service System")

    isExit = True
    while isExit:
        print("\nMain Menu:")
        print("1. Get a single package's information")
        print("2. Get all packages information")
        print("3. Exit the program")
        option = input("Choose (1, 2, or 3): ")

############ TESTING ####################################################
        if option == "2":
            load_package_data('Package_Data_File.csv')
            for i in range(len(myHashTable.table)):
                print('ID: {} and info: {}'.format(i + 1, myHashTable.search(i + 1)))

        elif option == "3":
            print("Exiting...")
            isExit = False