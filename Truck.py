# Truck class
class Truck:
    def __init__(self, location = None, packages = None, current_time = None, time_left_hub = None):
        self.location = location
        self.packages = packages
        self.current_time = current_time
        self.time_left_hub = time_left_hub
        return

    def loadPackages(self, packageList, hTable):
        packages = []
        for i in packageList:
            i = int(i)
            hTable.search(i).status = 'EN ROUTE'
            packages.append(hTable.search(i))
        return packages



