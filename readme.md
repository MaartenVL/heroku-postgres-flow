# Intro

In this tutorial we will set up a postgres database, hosted in the cloud via Heroku.
We design the database model in dbdiagram.io, and handle the import of data from an excel file using python and sqlalchemy.

# Installation

Some preperation is necessary!

* conda environment

We first need to set up a python environment in conda, for this tutoriual we're using python 3.8. Packages can be installed from
the command line using:

```conda install --file requirements.txt```

* register for an heroku account: https://signup.heroku.com/

Unfortunatly, heroku won't offer free credits anymore as of end November 2022:

![alt text](readme_images/nofreelunch.PNG?raw=true)

* after registering, you can create your first app

![alt text](readme_images/10-create-new-app.PNG?raw=true)

* You can choose the app name, and your region. Click "Create app":

 ![alt text](readme_images/11-app-name.PNG?raw=true)


# Setting up postgres using Heroku in the could

* Head over to resources, and select "Heroku postgres". You can go for the "hobby-dev" plan:

![alt text](readme_images/21-heroku-postgress-resources.PNG?raw=true)

* Clicking on your newly created service, go over to "Settings" to consult your db credentials. You need these to connect to the database:

![alt text](readme_images/22-check-credentials-Capture.PNG?raw=true)

# Connecting to your new database

There a couple of options to connect to the database.

## Heroku CLI

* head over to https://devcenter.heroku.com/articles/heroku-cli and follow the steps to get the heroki CLI up and running for your command line

* However, for this tutorial, we will be doing some more db management using dbeaver.

## Dbeaver

Dbeaver is a Free multi-platform database tool for developers, database administrators, analysts and all people who need to work with databases. 
It Supports all popular databases, and the one we'll be using it for in this tutorial.

* to use Dbeaver, you need to have a version of Postgres already installed on your local machine: https://www.postgresql.org/download/
* head over to https://dbeaver.io/ to download dbeaver
* Open dbeaver once installed. You can click the top-left "new database connection" icon to make a connection to the heroku db:

![alt text](readme_images/32-db-conn1.PNG?raw=true)

* For now, our database doesn't contain any tables, we'll take care of that in the next step.

# Database model

## Create database model

We' ll use  [dbdiagram.io](https://dbdiagram.io/home) to create a database model. Once designed, we can export it into SQL code, that we then launch
in dbeaver to create the tables and relations between the tables.

* For this example, we create 3 tables that allow us to store data coming from sensors, and add addtional metadata about the sensor en it's location:

![alt text](readme_images/41-database-dbdiagram.PNG?raw=true)

* once created click "export to PostgreSQL" to have it create a .sql file we can run to set up the tables and relationships:

![alt text](readme_images/42-database-dbdiagram-export.PNG?raw=true)

## Create tables in dbeaver

You could choose you fire up the sal query using the Heroku CLI, a python script,... but for this tutorial we'll launch it from dbeaver.

* open dbeaver and connect to the database.
* Open up a new script, and past the .sql file we created from dbdiagram.io in here
* Run this script (stored in `src/10-create-tables.sql`):
![alt text](readme_images/43-database-sql-script.PNG?raw=true)

* this created the tables, you can view them by clicking the public scheme, and then "ER Diagram":
![alt text](readme_images/43-database-sql-creation.PNG?raw=true)

# Migrate data from data sheets to heroku

## The sample csv dataset

With the database and empty tables in place, it's time to have a look at the excel sheet, `data/sample_data.xlsx` we want to import.

* There are 3 sheets inside the excel:

- Locations, listing some extra info on the locations where the sensors are placed
- Sensors, listing the different sensors
- Measurements, listing the data collected by the sensors

The images below show the dummy data that were inserted in each of the sheets.
These data we want to insert into our database.

Sensors            |  Locations          | Measurements
:-------------------------:|:-------------------------:|:-------------------------:
![](readme_images/51-fill-data-1.PNG?raw=true)  |  ![](readme_images/51-fill-data-2.PNG?raw=true)|  ![](readme_images/51-fill-data-3.PNG?raw=true)

## Python and SQLalchemy

We will be using the python in tandem with the SQLalchemy package to migrate the data in the excel sheets into the database.
The following scipts were created for this:

* **excel_parser.py**: parses the excel sheets, and transforms them in such a way they are ready to be fitted into the database model.
* **orm.py**: contains the sqlalchemy orm, so that we can easily work with out database structure in python
* **push-data-db.py**: launch this file to read the data, transform it, and push it into the database!

You will need to update the credentials inside `push-data-db.py`:

```python
DBASE = 'd2hto0sg05etiq'
USER = 'itwgxojqwqnqwl'
PASSWORD = ';-)'
HOST = 'ec2-34-248-169-69.eu-west-1.compute.amazonaws.com'
PORT = 5432
SCHEMA = 'public'
```

Then we make the connection to the Heroku hosted postgres database:
The dbclass class is found in dbutils.py, and contains some utilities to work with your python-db-connection to the postgres database.
```python
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
```
Next, we import our data from the excel sheets:

```python
sensors,measurements,locations = import_excel_data()
```

Then, we call push the data to the database.
```python
add_locations(db, data=locations)
add_sensors(db, data=sensors)
add_measurements(db, data=measurements)
```

the functionalities of these 3 methods are very basic, but it's a start. It's important they are ran in that sequence, because we needs locations in place to be bale to refer to them when adding `sensors`.
Here below we'll go over `add_locations`

* in `sessionmaker` we create a handle to be able to connect to the heroku database.
* next we iterate over each row inside `data`, containing the locations from the excel sheet.
```python
...    
for index, item in data.iterrows():
...
```
* Next we check if these locations were already added (look for them in the database):
```python
...
exists = session.query(sqlalchemy.exists().where(orm_file.Location.name == item['locatie'])).scalar()
...
```
* Next, if the data was not added yet, we create a `Location` instance from the orm file to which we add the fields (or columns):
* `item` refers here to the current row in the excel sheet

```python
...
location_to_add = orm_file.Location()
location_to_add.name = item['locatie']
location_to_add.description = item['beschrijving']
location_to_add.x = item['x']
location_to_add.y = item['y']
location_to_add.z = item['z']
...
```
* finally, we add the data to the database, and close our session after looping over each row.
```python
...
session.add(location_to_add)
session.commit()
...
session.close()
```
* full code below:

```python
def add_locations(db,data):
    """

    :return:
    """
    Session = sessionmaker(bind=db.sqla_engine)
    session = Session()
    # loop over data to add and check if data is already in the db. If not ==> add
    for index, item in data.iterrows():
        exists = session.query(sqlalchemy.exists().where(orm_file.Location.name == item['locatie'])).scalar()
        if not exists:
            print('table: "Location" with column: "name" and value: {value} does not exist,  adding data'.format(
                value=item['locatie']))

            location_to_add = orm_file.Location()
            location_to_add.name = item['locatie']
            location_to_add.description = item['beschrijving']
            location_to_add.x = item['x']
            location_to_add.y = item['y']
            location_to_add.z = item['z']
            print(location_to_add)
            session.add(location_to_add)
            session.commit()
        else:
            print(
                'table: "Location" with column: "name" and value: {value}  already existed, skip adding of data'.format(
                    value=item['locatie']))
    session.close()
```
## Consult your data inside the database

We use dbeaver again to check if the data was correctly added into the database!

