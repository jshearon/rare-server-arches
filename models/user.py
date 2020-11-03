from datetime import datetime

class User():

    def __init__(self, id, firstName, lastName, displayName, email):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.displayName = displayName
        self.email = email
        self.createdOn = datetime.now()
