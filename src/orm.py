# coding: utf-8
from sqlalchemy import ARRAY, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Table, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB, UUID, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata
metadata.schema = 'public'




class Measurement(Base):
    __tablename__ = 'measurement'

    id = Column(Integer, primary_key=True, server_default=text("nextval('contact_id_seq'::regclass)"))
    value = Column(Float(53))
    unit = Column(String)
    sensor_id = Column(ForeignKey('sensor.id'))
    timestmp = Column(DateTime)


class Sensor(Base):
    __tablename__ = 'sensor'

    id = Column(Integer, primary_key=True, server_default=text("nextval('deployment_id_seq'::regclass)"))
    name = Column(String, nullable=False, unique=True)
    type = Column(String)
    location_id = Column(ForeignKey('location.id'))
    installation_date = Column(DateTime)


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, server_default=text("nextval('location_id_seq'::regclass)"), comment='A unique id for the location')
    name = Column(String, nullable=False, unique=True, comment='A unique name for the location')
    description = Column(String)
    x = Column(Float(53))
    y = Column(Float(53))
    z = Column(Float(53))
