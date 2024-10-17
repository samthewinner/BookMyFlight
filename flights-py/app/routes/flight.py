from fastapi import APIRouter, Depends , Request
from sqlalchemy.ext.asyncio import AsyncSession
from controllers import flight as flight_controller
from schemas.flight import Flight, FlightCreate ,FlightSearch
from middlewares.middleware import checkRole
from db.session import get_db
from json import *

router = APIRouter()

@router.get("/flights/search")
async def read_flights(data:FlightSearch,db: AsyncSession = Depends(get_db)):
    return await flight_controller.get_flights(data,db)

@router.post("/flights/create", response_model=Flight)
async def create_flight(req:Request ,flight: FlightCreate, db: AsyncSession = Depends(get_db),role = Depends(checkRole)):
    # print("In post")
    return await flight_controller.create_flight(flight, db)

@router.post("/flights/update",response_model=Flight)
async def update_flight(req:Request ,flight: Flight, db: AsyncSession = Depends(get_db),role = Depends(checkRole)):
    # print(flight)
    return await flight_controller.update_flight(flight,db)

@router.post("/flights/delete",status_code=204)
async def delete_flight(req:Request ,flightId:int,db:AsyncSession = Depends(get_db),role = Depends(checkRole)):
    # print("From router: ",flightId)
    print(f"Data: {flightId}\nType: {type(flightId)}")
    return await flight_controller.delete_flight(flightId,db)

@router.get("/flights/migrate",status_code=200)
async def migrateData():
    return await flight_controller.dataMigration()