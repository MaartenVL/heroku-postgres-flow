import src.orm as orm_file
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import psycopg2
import pandas as pd
import os
import json

logger = logging.getLogger(__name__)

class dbclass(object):
    """Communication tool for the data base

    Parameters
    ----------
    dbase : str
        database name of the tsdb
    user: str
        username of the tsdb
    password: str
        password of the tsdb
    port: int
        port number of the tsdb
    host: str
        hostname of the tsdb
    """
    __conn = None

    def __init__(self, dbase, user, password, port, host):

        self.dbase = dbase
        self.user = user
        self.password = password
        self.port = port
        self.host = host
        self.__connect()
        self.__sqlalchely_engine_handle()

    def __connect(self):
        """ Reconnect to the database if there is no connection or if the connection was closed or broken
        """
        try:
            self.__conn = psycopg2.connect(host=self.host,
                                           port=self.port,
                                           database=self.dbase,
                                           user=self.user,
                                           password=self.password)

            logger.debug(self.__conn.get_dsn_parameters())

        except (Exception, psycopg2.Error) as e:
            logging.error(e)
            raise  # defer handling ?
        finally:
            logging.info('tsdb connection opened successfully.')

    def connected(self):
        """ TODO Does not do a check if the server link has been severed, should perform a simple
                 SQL query for this
        """
        if (self.__conn == None) or (self.__conn.closed != 0):
            return False
        else:
            return True

    def connection_handle(self):
        """ Returns the connection handle
        """
        if not self.connected():
            self.__connect()

        return self.__conn

    def __sqlalchely_engine_handle(self):
        """ returns the sqlalchemy connection handle
        """
        engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(self.user,
                                                                    self.password,
                                                                    self.host,
                                                                    self.port,
                                                                    self.dbase))
        self.sqla_engine = engine
        return self.sqla_engine

    def commit(self):
        self.__conn.commit()


def get_sessionmaker(config):
    engine = sqlalchemy.create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        config['user'], config['passwd'], config['host'], config['port'], config['db']))
    return sessionmaker(bind=engine)


def nat_check(nat):
    """

    :param nat:
    :return:
    """
    if pd.isna(nat):
        return None

    return nat





def add_sensors(db,data):
    """

    :return:
    """
    Session = sessionmaker(bind=db.sqla_engine)
    session = Session()
    # loop over data to add and check if data is already in the db. If not ==> add
    for index, item in data.iterrows():
        exists = session.query(sqlalchemy.exists().where(orm_file.Sensor.name == item['name'])).scalar()
        if not exists:
            print('table: "Sensor" with column: "name" and value: {value} does not exist,  adding data'.format(
                value=item['name']))

            sensor_to_add = orm_file.Sensor()
            sensor_to_add.name = item['name']
            sensor_to_add.type = item['type']
            id_to_add = session.query(orm_file.Location.id).filter(orm_file.Location.name == item["location"]).scalar()
            sensor_to_add.location_id = id_to_add
            sensor_to_add.installation_date = item['installatie_datum']
            print(sensor_to_add)
            session.add(sensor_to_add)
            session.commit()
        else:
            print(
                'table: "Sensor" with column: "name" and value: {value} already existed, skip adding of data'.format(
                    value=item['name']))
    session.close()


def add_measurements(db,data):
    """

    :return:
    """
    Session = sessionmaker(bind=db.sqla_engine)
    session = Session()
    # loop over data to add and check if data is already in the db. If not ==> add
    for index, item in data.iterrows():

            measurement_to_add = orm_file.Measurement()
            measurement_to_add.value = item['value']
            measurement_to_add.unit = item['unit']
            id_to_add = session.query(orm_file.Sensor.id).filter(orm_file.Sensor.name == item["sensor"]).scalar()
            measurement_to_add.sensor_id = id_to_add
            measurement_to_add.timestmp = item["timestamp"]
            print(measurement_to_add)
            session.add(measurement_to_add)
            session.commit()
    session.close()


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