import redis
import os

async def connect_with_redis(redis_config={}):
    if len(redis_config ) == 0:
        REDIS_HOST = os.getenv('REDIS_HOST',"localhost")
        return redis.Redis(host=REDIS_HOST,db=1,decode_responses=True)    
    return redis.Redis(**redis_config)