# create a new database

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date, MetaData
from db.session import engine
from sqlalchemy.ext.declarative import declarative_base

# from db import engine
# class Flights(Base):
#     __tablename__ = 'flights'

#     id = Column(Integer,primary_key=True,index=True)
#     source = Column(String(50))
#     destination = Column(String(50))
#     departure_date = Column()

# Define the flights table model
Base = declarative_base()

class Flight(Base):
    __tablename__ = 'flightData'
    flightId = Column(Integer, primary_key=True, index=True,autoincrement=True)
    source = Column(String(50), nullable=False)
    destination = Column(String(50), nullable=False)
    departureTime = Column(DateTime, nullable=False)
    arrivalTime = Column(DateTime, nullable=False)
    departureDate = Column(Date, nullable=False)
    arrivalDate = Column(Date, nullable=False)
    capacity = Column(Integer, nullable=False)
    airline = Column(String(100), nullable=False)

Base.metadata.create_all(engine)