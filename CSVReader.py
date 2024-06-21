import csv

distanceData = []
addressData = []


############################## DISTANCE CSV DATA PARSING ##############################################
def load_distance_data(filename):
    with open(filename) as CSV_Distance:
        reader = csv.reader(CSV_Distance)
        next(reader)
        for row in reader:
            floats_row = [float(value) for value in row[1:]]  # this converts the numbers to floats
            distanceData.append(floats_row)
    return distanceData


############################## ADDRESS CSV DATA PARSING ##############################################
def load_address_data(filename):
    with open(filename) as CSV_Addresses:
        reader = csv.reader(CSV_Addresses)
        for row in reader:
            addressData.append(str.strip(row[2]))
    return addressData

































# def load_package_data(filename):
#     with open(filename) as package_info:
#         package_data = csv.reader(package_info, delimiter=',')
#         next(package_data)
#         for package in package_data:
#
#             if package[0]:  # Check if package_ID is not empty
#                 package_ID = int(package[0])
#             else:
#                 # Handle empty package_ID
#                 continue    # Skip this row and move to the next one
#
#             pAddress = package[1]
#             pCity = package[2]
#             pState = package[3]
#             pZipcode = package[4]
#             pDeadline_time = package[5]
#             pWeight = package[6]
#             pSpecialNotes = package[7]
#             pStatus = "At Hub"
#             # print(package)
#
#             # Package object
#             p = Package(package_ID, pAddress, pCity, pState, pZipcode, pDeadline_time, pWeight, pSpecialNotes, pStatus)
#
#             # Insert data into hash table
#             myHashTable.insert(package_ID, p)
#
#
# ################### TESTING ############################################
# myHashTable = HashTable()
# load_package_data('Package_Data_File.csv')
# for i in range(len(myHashTable.table)):
#     print('ID: {} and info: {}'.format(i+1, myHashTable.search(i+1)))
