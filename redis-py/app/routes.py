from fastapi import APIRouter,Depends,status,Header,Request
from db import connect_with_redis
from models import Book,Cancel,View,Delete,Add
from typing import Optional
import controller

router = APIRouter()

@router.post('/book',status_code=status.HTTP_200_OK)
async def book_flight(data:Book  ,req:Request,db = Depends(connect_with_redis)):
    userId = req.headers.get('userId')
    # print(req.headers)
    # print()
    # print('userId' in req.headers)
    # print(f"User id : {userId}")
    return await controller.book_flights(data,db,userId)

@router.get('/view',status_code=status.HTTP_200_OK)
async def view_flight(flightId:int,db=Depends(connect_with_redis)):
    print (f"data from seats-{flightId}")
    return await controller.view_flight(flightId,db)

@router.post('/cancel',status_code=status.HTTP_200_OK)
async def cancel_flight(data:Cancel,db=Depends(connect_with_redis)):
    return controller.cancel_flight(data,db)

@router.post('/delete',status_code=status.HTTP_200_OK)
async def delete_flights(data:Delete,db=Depends(connect_with_redis)):
    # print(flight_ids.flight_ids)
    return controller.delete_flights(data,db)

@router.post('/add',status_code=status.HTTP_200_OK)
async def add_flights(data : Add,db = Depends(connect_with_redis)):
    return controller.add_flights(data,db)


