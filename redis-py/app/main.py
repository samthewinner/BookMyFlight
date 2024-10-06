from fastapi import FastAPI
import routes
from eurekaClient import eurekaConfig
# from controller_ import router

app = FastAPI()
PORT = 8082
eurekaConfig(PORT,'seats-service')

app.include_router(routes.router)

