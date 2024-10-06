from models import Book,Cancel,View,Delete,Add
import json
from fastapi import HTTPException
import py_eureka_client.eureka_client as eureka_client


# use pessimistic locking / mutex 
# if a user selects a seat(resource) , it will be reserved/locked until either the payment is confirmed or the timer expires
# during the resource is locked , no other user can book the seat
async def book_flights(data:Book,db,userId:int):
    print('inside book flights')
    seats = db.get(data.flightId)
    # requested for wrong seat
    if seats is None:
        raise HTTPException(status_code=404, detail="Flight with given id not found")
    
    seats = json.loads(seats)

    if data.seat_no  >= len(seats):
        raise HTTPException(status_code=404, detail="Given seat does not exist in flight")
    
    if seats[data.seat_no] is not None:
        raise HTTPException(status_code=404, detail="This seat seems to be booked currently , please refresh the page or try again in a few minutes ")

    # make the below operation atomic 
    seats[data.seat_no] = userId
    db.set(data.flightId,json.dumps(seats))
    print('Before making call to node-service')
    # TODO: make an API call to the user-service to update the user's flight history
    try:
        print(f"Calling user-service API with userId: {userId}, flight_id: {data.flightId}")
        resp = await eureka_client.do_service_async(
            "node-service",
            f"/user/updateFlightHistory?user_id={userId}&flight_id={data.flightId}",
            method="POST"
        )
        print(f"Response from user-service: {resp}")
    except Exception as api_error:
        print(f"Error calling user service: {api_error}")
        raise HTTPException(status_code=500, detail="Error updating user flight history")
    
    return {"msg": "Seat booked successfully"}


async def view_flight(flightId, db):
    print(f"Type of data: {type(flightId)}")
    # print(data)
    seats =  db.get(flightId)
    if seats is None:
        return {'msg':f'No flight with id {flightId}'}
    seats = json.loads(seats)
    print(f"seats for flightid: {flightId} are : {seats} and type of seats : {type(seats)}")
    print(f"Seat 0 : {seats[0]}")
    return seats
    # return 0

def cancel_flight(data:Cancel,db):
    seats = db.get(data.flightId)
    if seats is None:
        raise HTTPException(status_code=404, detail="Flight with given id not found")
    seats = json.loads(seats)

    if seats[data.seat_no] == None:
        raise HTTPException(status_code=401,detail="Seat hasn't been booked")
    
    seats[data.seat_no] = None

    db.set(data.flightId,json.dumps(seats))


def delete_flights(data:Delete,db):
    
    with db.pipeline() as pipe:
        for flightId in data.flightIds:
            pipe.delete(flightId)
        pipe.execute()

def add_flights(data:Add,db):
    with db.pipeline() as pipe:
        for flightId,capacity in data.flights:
                empty_list = json.dumps([None] * (capacity+1))
                pipe.set(flightId, empty_list)
        pipe.execute()