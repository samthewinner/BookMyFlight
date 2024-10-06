from pydantic import BaseModel
from typing import List,Tuple

class Book(BaseModel):
    flightId : int  
    seat_no : int 

class View(BaseModel):
    flightId : int 

class Cancel(View):
    seat_no : int 

class Delete(BaseModel):
    flightIds : List[int]

class Add(BaseModel):
    flights : List[List[int]]