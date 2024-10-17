from typing import Union
from eurekaClient import eurekaConfig
from fastapi import FastAPI,Depends
# from sqlalchemy.orm import Session

from routes import flight as flight_routes

# import models.models

PORT = 8081
eurekaConfig(PORT,'flights-service')
app = FastAPI()


# flight.Base.metadata.create_all(bind=engine)

# class airline(BaseModel):

# db_dependency = Annotated(Session,Depends(get_db))

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

app.include_router(flight_routes.router)


