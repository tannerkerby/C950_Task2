# Package Class with status update function
class Package:
    def __init__(self, ID, address, city, state, zipcode, Deadline_time, weight, specialNotes, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.Deadline_time = Deadline_time
        self.weight = weight
        self.specialNotes = specialNotes
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        return (f"{self.ID}, {self.address}, {self.city}, {self.state}, {self.zipcode}, "
                f"{self.Deadline_time}, {self.weight}, {self.specialNotes}, {self.status}")

    def update_status(self, convert_timedelta):
        if self.delivery_time < convert_timedelta:
            self.status = "Delivered"
        elif self.departure_time > convert_timedelta:
            self.status = "En route"
        else:
            self.status = "At Hub"


