import PyMySQL

# Open database connection
print('logging into database')
try:
    db = PyMySQL.connect("localhost","root","raspberry","weather" )
raise Exception:
    print('error connecting to database')

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print ("Database version : %s " % data)

# disconnect from server
db.close()