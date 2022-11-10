from src.dbutils import dbclass, add_sensors,add_measurements, add_locations
from src.excel_parser import import_excel_data

DBASE = 'd2hto0sg05etiq'
USER = 'itwgxojqwqnqwl'
PASSWORD = ';-)'
HOST = 'ec2-34-248-169-69.eu-west-1.compute.amazonaws.com'
PORT = 5432
SCHEMA = 'public'


# Database connection for queries
#---------------------------------
# get instance of class
db = dbclass(dbase=DBASE,
            user=USER,
            password=PASSWORD,
            port=PORT,
            host=HOST)

# test connection
concheck = db.connected()
print(concheck)

# get the data
sensors,measurements,locations = import_excel_data()

# add sensors, measurements and locations
add_locations(db, data=locations)
add_sensors(db, data=sensors)
add_measurements(db, data=measurements)
