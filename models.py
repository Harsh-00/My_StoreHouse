from redis_om import HashModel
from database import redis
from pydantic import Field

class Product(HashModel):
    name:str=Field(...,min_length=1,max_length=100)
    price:float=Field(...,ge=0)
    quantity:int=Field(...,ge=0)
    class Meta:
        database= redis