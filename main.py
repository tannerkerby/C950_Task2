# STUDENT ID: 011044210
# Tanner Kerby
# C950 Task 2

from Package import Package
from Truck import Truck
from CSVReader import *
from HashTable import HashTable
from datetime import datetime, timedelta

# Creating empty HashMap for packages data
myHashTable = HashTable()

# Initiating truck speed.
truck_speed = 18/60  # Speed is miles per minute from 18 mph.

today = datetime.now()

# Truck 1 start time
start = datetime(today.year, today.month, today.day, 8, 0, 0, 0)

# Truck 2 starts at 9:05am to consider some packages not arriving to the HUB until that time.
truck2Departure = datetime(today.year, today.month, today.day, 9, 5, 0, 0)

# Truck 3 Departure is set to leave at 10:15:20, which is when Truck 1 is finished delivering its packages.
truck3Departure = datetime(today.year, today.month, today.day, 10, 15, 20, 0)

distances = load_distance_data('DistanceTable.csv')
addresses = load_address_data('Addresses.csv')


'''
FUNCTION to automatically parse the package data
and insert each package into the hash table
'''
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
            pTruck = None
            pInfo = [str.strip(x) for x in package[1::]]
            pStatus = 'HUB'
            pTimeDelivered = None
            # Package object assembly for each row in the CSV
            p = Package(package_ID, pInfo, pTruck, pStatus, pTimeDelivered)
            # Insert each package object into hash table
            myHashTable.insert(package_ID, p)
    return myHashTable


load_package_data('Package_Data_File.csv')


'''
Function to calculate the distance between 2 nodes in the distance table CSV file.
'''
def distanceBetween(address1, address2, listAddresses, list2DDistances):
    if address1 not in listAddresses or address2 not in listAddresses:
        print("One or both locations is invalid.")
        return
    else:
        i = listAddresses.index(address1)
        j = listAddresses.index(address2)
        if i > j:
            return list2DDistances[i][j]
        else:
            return list2DDistances[j][i]


'''
Below is a function to calculate the minimum distance by calling the distanceBetween function in a for loop to determine the smallest number.
This is used in the NN algorithm
'''
def minDistanceFrom(truck, listAddresses, list2DDistances, hTable):
    dictPackageDistance = dict()
    for pack in truck.packages:
        if pack.status != 'DELIVERED' and pack.info[0] != truck.location:
            dictPackageDistance[pack.ID] = float(distanceBetween(truck.location, pack.info[0], listAddresses, list2DDistances))
    if len(dictPackageDistance) > 0:
        return hTable.search(int(min(dictPackageDistance.items(), key=lambda x: x[1])[0]))
    else:
        return None


'''
Below I instantiate 3 truck objects and assign the packages to each one via a list.
'''
truck1 = Truck()
truck2 = Truck()
truck3 = Truck()
truck1Packages = [1, 13, 5, 14, 15, 16, 19, 20, 29, 30, 31, 37, 40]
truck2Packages = [2, 3, 4, 7, 8, 18, 6, 25, 32, 34, 28, 36, 38]
truck3Packages = [9, 10, 11, 12, 17, 21, 35, 22, 23, 24, 26, 27, 33, 39]


'''
Below I create 3 instances of assigning the packages to each truck.
I assign the current time to when that truck leaves the HUB
I use a for loop to search the Hash Table for the specific package using the package's KEY
'''
truck1.packages = truck1.loadPackages(truck1Packages, myHashTable)
truck1.current_time = start
truck1.time_left_hub = start
for i in truck1Packages:
    package = myHashTable.search(i)
    package.timeLoaded = truck1.time_left_hub
    package.truck = "Truck1"
    myHashTable.update(i, package)
truck1.location = addressData[0]

truck2.packages = truck2.loadPackages(truck2Packages, myHashTable)
truck2.current_time = truck2Departure
truck2.time_left_hub = truck2Departure
truck2.location = addressData[0]
for i in truck2Packages:
    package = myHashTable.search(i)
    package.timeLoaded = truck2.time_left_hub
    package.truck = "Truck2"
    myHashTable.update(i, package)

truck3.packages = truck3.loadPackages(truck3Packages, myHashTable)
truck3.current_time = truck3Departure
truck3.time_left_hub = truck3Departure
truck3.location = addressData[0]
for i in truck3Packages:
    package = myHashTable.search(i)
    package.timeLoaded = truck3.time_left_hub
    package.truck = "Truck3"
    myHashTable.update(i, package)

'''
Below I create a Nearest Neighbor Algorithm. 
A while loop starts as long as the minimum distance isn't 'None'. 
In this loop, the trucks find the nearest address based on the address CSV data as well as the Distance CSV data, which uses the minDistance function.
The package is chosen based on what is closest to the truck and is then set to DELIVERED
The distance is added to a totalDistance variable, as well as the time it took to deliver, added to a timeDelivered package variable.
The truck's location then is updated to the packages address that it delivered.
After this is over, the totalDistance, truck's current time, and the distance to Hub are returned.

Time complexity for this algorithm: 
Since the minDistanceFrom is O(n^2), and there are m addresses to deliver the packages to, this is O(m*n^2)
'''
# Nearest Neighbor Algorithm Function
def deliverPackages(truck, listAddresses, list2DDistances, hTable):
    running = True
    totalDistance = 0.0
    while running:
        x = minDistanceFrom(truck, listAddresses, list2DDistances, hTable)
        if x is None:
            running = False
            break
        else:
            x.status = 'DELIVERED'
            dist = distanceBetween(truck.location, x.info[0], listAddresses, list2DDistances)
            truck.current_time += timedelta(minutes=float(dist/truck_speed))
            # print("Truck Time: %s" % truck.current_time)
            x.timeDelivered = truck.current_time
            totalDistance += dist
            truck.location = x.info[0]
            hTable.update(x.ID, x)
    disToHub = distanceBetween(truck.location, listAddresses[0], listAddresses, list2DDistances)
    truck.current_time += timedelta(minutes=float(disToHub/truck_speed))
    # print("Final Truck Time: %s" % truck.current_time)
    return [disToHub, totalDistance, truck.current_time]


'''
This will give 3 variables for each truck. The totalDistance variable calculates the total miles driven.
'''
disToHub1, totalDistanceTruck1, returnTimeTruck1 = deliverPackages(truck1, addressData, distanceData, myHashTable)
disToHub2, totalDistanceTruck2, returnTimeTruck2 = deliverPackages(truck2, addressData, distanceData, myHashTable)
disToHub3, totalDistanceTruck3, returnTimeTruck3 = deliverPackages(truck3, addressData, distanceData, myHashTable)


############################################## User Interface When Program Starts #################################################
if __name__ == '__main__':
    print("\nWelcome to the WGUPS Delivery Service System!")
    print("\nAbove is the data of all the packages at the end of delivery day.")

    runProgram = True
    while runProgram:
        print("\nMain Menu:")
        print("1. Get specific information based on a requested time")
        print("2. Get all information & Truck mileage")
        print("3. Display the return times for the trucks")
        print("4. Exit the program")
        option = input("Choose (1, 2, 3, or 4): ")

        if option == "1":
            hour = input("\nEnter Hour in military time. (0-23) For example, 14 = 2pm.: ")
            hour = int(str.strip(hour))
            minute = input("\nEnter Minute (0-60): ")
            minute = int(str.strip(minute))
            timeInputByUser = datetime(today.year, today.month, today.day, hour, minute, 0, 0)
            print("\nTime entered:", timeInputByUser)
            numOfPackages = input("\nEnter number of packages to view (1-40): ")
            numOfPackages = int(str.strip(numOfPackages))

            def packageStatus(givenTime, hTab, numberOfPackages):
                for i in range(1, numberOfPackages + 1):
                    p = hTab.search(i)
                    if p.timeLoaded > givenTime:
                        print("Package %d is still at the HUB" % i)
                    elif givenTime >= p.timeLoaded and givenTime < p.timeDelivered:
                        print("Package %d is ENROUTE on %s. ETA = %s" % (i, p.truck, p.timeDelivered))
                    elif timeInputByUser >= p.timeDelivered:
                        print("Package %d was DELIVERED via %s at %s" % (i, p.truck, p.timeDelivered))
                return

            packageStatus(timeInputByUser, myHashTable, numOfPackages)

        elif option == "2":
            for i in range(len(myHashTable.table)):
                print('{}'.format(myHashTable.search(i + 1)))
            print("Total miles driven for Truck 1:", totalDistanceTruck1)
            print("Total miles driven for Truck 2:", totalDistanceTruck2)
            print("Total miles driven for Truck 3:", totalDistanceTruck3)
            totalMilesDriven = totalDistanceTruck1 + totalDistanceTruck2 + totalDistanceTruck3
            print("Total miles driven:", totalMilesDriven)

        elif option == "3":
            # Times when trucks are done delivering
            print("\nReturn Time for Truck 1 = %s" % returnTimeTruck1)
            print("Return Time for Truck 2 = %s" % returnTimeTruck2)
            print("Return Time for Truck 3 = %s" % returnTimeTruck3)

        elif option == "4":
            print("Exiting...")
            runProgram = False

        else:
            print("Please enter a valid number.")