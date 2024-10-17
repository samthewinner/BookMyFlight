import os
import py_eureka_client.eureka_client as eureka_client
from fastapi import HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.flight import Flight
from schemas.flight import FlightCreate,FlightSearch
import redis
from sqlalchemy import delete
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta,date
from dateutil.relativedelta import relativedelta
import time
import uuid

async def create_flight(flight: FlightCreate, db: AsyncSession):
    db_flight = Flight(**flight.dict())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight

async def get_flights(data:FlightSearch,db: AsyncSession):
    result = db.execute(text(f"SELECT * FROM flightData WHERE source='{data.source}' AND destination='{data.destination}' AND departureDate='{data.departureDate}'"))
    ret = result.mappings().all()
    for idx in range(len(ret)):
        row = dict(ret[idx])
        row['seats'] = await eureka_client.do_service_async("seats-service",f"/view?flightId={row['flightId']}")
        ret[idx] = row
    return ret

async def update_flight(flight: Flight, db: AsyncSession):
    data = db.get(Flight,flight.flightId)
    if not data:
        raise HTTPException(status_code=404, detail="Flight not found")
    data.source = flight.source
    data.destination = flight.destination
    data.departureTime = flight.departureTime
    data.arrivalTime = flight.arrivalTime
    data.departureDate = flight.departureDate
    data.arrivalDate = flight.arrivalDate
    data.capacity = flight.capacity
    data.airline = flight.airline

    db.commit()
    return flight

async def delete_flight(flightId:int,db:AsyncSession):

    # flightId = int(str(flightId).split('=')[1])
    data = db.execute(text(f"SELECT flightId FROM flightData as f WHERE f.flightId = {flightId}")).fetchone()
    # print(data)
    # # data = db.get(Flight,flightId)
    if not data:
        raise HTTPException(status_code=404, detail="Flight not found")
    # print(39)
    # data = db.query(Flight).filter(Flight.flightId == flightId).first()
    # print(flightId)
    # query =  delete(Flight).where(Flight.flightId == flightId)
    # data = db.execute(select(Flight).where(Flight.flightId == flightId))
    # data = data.sc
    # db.execute(query)
    
    db.execute(text(f"DELETE FROM flightData  WHERE flightData.flightId = {flightId}"))
    # db.delete(data)
    db.commit()

async def dataMigration():
    def acquire_lock_with_expiration(conn, lockname, acquire_timeout=10, lock_timeout=10):
    
        identifier = str(uuid.uuid4())

        lock_key = 'lock:' + lockname

        end = time.time() + acquire_timeout

        while time.time() < end:

            if conn.set(lock_key, identifier,ex=lock_timeout):

                return identifier

            time.sleep(0.001)

        return False


    def release_lock(conn, lockname, identifier):

        lock_key = 'lock:' + lockname

        pipe = conn.pipeline(True)

        while True:

            try:

                pipe.watch(lock_key)

                if pipe.get(lock_key) == identifier:

                    pipe.multi()

                    pipe.delete(lock_key)

                    pipe.execute()

                    return True

                pipe.unwatch()

                break

            except redis.exceptions.WatchError:

                pass

        return False


    async def transfer_data():

        # conn with redis   ✔
        REDIS_HOST = REDIS_HOST = os.getenv('REDIS_HOST',"localhost")
        REDIS_PORT = 6379  
        print(REDIS_HOST)
        # REDIS_PASSWORD = 'your-redis-password'  
        client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=1,decode_responses=True)
        # client.lock()
        #check for the job_status , it tells whether today's data migration has occured or not 
        job_status = client.get('job-status')

        # job_status is true means today's migration task is complete , do nothing
        if job_status is True :
            return 

        # aquire the lock
        lockname = 'data-migration-lock'


        # if lock exists , then wait until either lock gets unset or job is done
        while (client.exists(lockname)) and (client.get('job-status') is False):
            pass 

        #today's job is done , do nothing
        if client.get('job-status'):
            return 
            
        # check redis for lock on today's date
        identifier = acquire_lock_with_expiration(client,lockname,acquire_timeout=10,lock_timeout=10)

        if identifier is None:
            return 

        #handle sql logic
        await transfer_sql_to_redis()

        release_lock(client,lockname,identifier)
        print("Today's migration done")

    async def transfer_sql_to_redis():
        #connect with mysql db

        async def get_sql_data():
            

            DATABASE_URL = os.getenv('DATABASE_URL','mysql+mysqlconnector://root:root@localhost:3306/test')
            print(DATABASE_URL)
            engine = create_engine(DATABASE_URL)
            Session = sessionmaker(bind=engine)
            session = Session()
            # Calculate next month + 1 day from today
            target_date = datetime.now() + relativedelta(months=1)
            formatted_date = target_date.strftime('%Y-%m-%d')

            # formatted_date = '2024-09-15'
            # yesterday_formatted_date = ''
        
            print(formatted_date)

            today = datetime.today()

            # Add 1 month to today's date
            next_month_date = today + relativedelta(months=1,days=1)

            filter_date = next_month_date.strftime('%Y-%m-%d')
            print(filter_date)
            # Create the raw SQL query using the text() function
            query = text("SELECT flightId,capacity FROM flightData WHERE departureDate = :filter_date")

            # Execute the query and pass in the parameter
            result = session.execute(query, {'filter_date': filter_date})

            yesterday = today - timedelta(days=1)

            # Fetch all results
            flights = result.fetchall()

            new_data = [list(i) for i in flights]

            filter_date = yesterday.strftime('%Y-%m-%d')

            # Create the raw SQL query using the text() function
            query = text("SELECT flightId,capacity FROM flightData WHERE departureDate = :filter_date")

            # Execute the query and pass in the parameter
            result = session.execute(query, {'filter_date': filter_date})

            # Fetch all results
            flights = result.fetchall()
            
            old_data = [list(i) for i in flights]

            return new_data,old_data
            # return [engine.connect().execute(text(f"SELECT flightId FROM flightData as f WHERE f.departureDate = {formatted_date}")).fetchall(),
            #         engine.connect().execute(text(f"SELECT flightId FROM flightData as f WHERE f.departureDate = {yesterday_formatted_date}")).fetchall()]
        
        new_data,old_data = await get_sql_data()
        print("SQL_DATA: ",new_data," - " ,old_data)
        # print(new_data)
        #TODO:verify sql data type

        if len(new_data) == 0:
            return
        
       
        data = {
            "flights": new_data
        }

        response = await eureka_client.do_service_async('seats-service',
                                            service='/add',
                                            method='POST',
                                            data=data)

        data = {
            "flights": old_data
        }

        
        response = await eureka_client.do_service_async('seats-service',
                                            service='/delete',
                                            method='POST',
                                            data=data)
    
    await transfer_data()

async def deactivateLock():
    REDIS_HOST = REDIS_HOST = os.getenv('REDIS_HOST',"localhost")
    REDIS_PORT = 6379  
    # REDIS_PASSWORD = 'your-redis-password'  
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=1,decode_responses=True)
    client.set('job-status',False)