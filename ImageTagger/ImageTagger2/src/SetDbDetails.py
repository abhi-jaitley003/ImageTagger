
class SetDbDetails :

    def __init__(self):
        self.dbString= ''

    def setDatabaseConnectionString(self):
        dbName = input('Enter the name of the database')
        username = input('Enter the username for the connection')
        # if there are no username and password
        if (len(username) == 0):
            self.dbString = 'postgresql://localhost/'+dbName
        else:
            password = input('Enter your password')
            self.dbString = 'postgresql://'+username+':'+password+'@localhost/'+dbName

    def getDatabaseConnectionString(self):
        return self.dbString

def main() :

    dbDetails = SetDbDetails()
    dbDetails.setDatabaseConnectionString()
    print (dbDetails.getDatabaseConnectionString())


if __name__ == '__main__':
    main()