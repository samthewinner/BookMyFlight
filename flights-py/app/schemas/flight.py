from pydantic import BaseModel
from datetime import datetime, date

class FlightCreate(BaseModel):
    source: str
    destination: str
    departureTime: datetime
    arrivalTime: datetime
    departureDate: date
    arrivalDate: date
    capacity: int
    airline: str

class Flight(FlightCreate):
    flightId: int
    
class FlightDelete(BaseModel):
    flightId: int

class FlightSearch(BaseModel):
    source:str 
    destination:str
    departureDate:date

    class Config:
        orm_mode = True
