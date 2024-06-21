# Package Class
class Package:
    def __init__(self, ID = None, info = None, truck = None, status = 'HUB', timeLoaded = None, timeDelivered = None):
        self.ID = ID
        self.info = info  # list that contains all information from package CSV (address, etc)
        self.truck = truck
        self.status = status
        self.timeLoaded = timeLoaded
        self.timeDelivered = timeDelivered
        return

    def __str__(self):
        return f"ID: {self.ID}, Info: {self.info}, Truck: {self.truck}, Status: {self.status}, Time Loaded: {self.timeLoaded}, Time Delivered: {self.timeDelivered}"



