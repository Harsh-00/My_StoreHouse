from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from models import Product 
 

app=FastAPI() 


origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"My":"Store"}


@app.post("/product")
def create_product(product:Product):
    return product.save()


@app.get("/product/all")
def get_all_products():
    return [detailed_product(pk) for pk in Product.all_pks()]
def detailed_product(pk:str):
    product= Product.get(pk)
    return product.dict()


@app.get("/product/{pk}")
def get_product(pk:str):
    return Product.get(pk)


@app.delete("/product/{pk}")
def delete_product(pk:str):
    return Product.delete(pk)


