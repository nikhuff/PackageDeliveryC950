class Package:
    "Package class used to define the notion of a package"
    def __init__(self, id, address, city, state, zip, deadline, mass, notes, timestamp):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.notes = notes
        self.timestamp = None

    # set the timestamp only when the package is delivered
    def setTimeStamp(self, time):
        self.timestamp = time

    def getId(self):
        return self.id
    
    def getAddress(self):
        return self.address
    
    def getCity(self):
        return self.city
    
    def getState(self):
        return self.state
    
    def getZip(self):
        return self.zip
    
    def getDeadline(self):
        return self.deadline

    def getMass(self):
        return self.mass

    def getNotes(self):
        return self.notes

    def getTimeStamp(self):
        return self.timestamp
