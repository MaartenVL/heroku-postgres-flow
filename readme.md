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

Sensors            |  Locations          | Measurements
:-------------------------:|:-------------------------:|:-------------------------:
![](readme_images/51-fill-data-1.PNG?raw=true)  |  ![](readme_images/51-fill-data-2.PNG?raw=true)|  ![](readme_images/51-fill-data-3.PNG?raw=true)

## Python and SQLalchemy

## Consult your data inside the database