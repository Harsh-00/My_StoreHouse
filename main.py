from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis_om.model.model import NotFoundError
from models import Product 
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
import os

load_dotenv()
app=FastAPI() 


origins = [f'{os.getenv("FRONT_URL_1")}', f'{os.getenv("FRONT_URL_2")}']
# origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"My":"Warehouse"}


@app.post("/product")
def create_product(product:Product):
    logger.info(f"Creating product: {product}")
    try:
        product.save()
        logger.info(f"Product created: {product.pk}")
    except Exception as e:
        logger.error(f"Failed to create product: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    return product


@app.get("/product/all")
def get_all_products():
    logger.info("Getting all products")
    try:
        result= [detailed_product(pk) for pk in Product.all_pks()]
        logger.info(f"Got all products: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to get all products: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
def detailed_product(pk:str):
    try:
        product = Product.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Product not found") 
    return product.dict()


@app.get("/product/{pk}")
def get_product(pk:str):
    logger.info(f"Getting product: {pk}")
    try:
        product = Product.get(pk)
    except NotFoundError:
        logger.error(f"Product not found: {pk}")
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/product/{pk}")
def update_product(pk:str, product:Product):
    logger.info(f"Updating product: {pk}")
    try:
        Product.get(pk)
    except NotFoundError:
        logger.error(f"Product not found: {pk}")
        raise HTTPException(status_code=404, detail="Product not found")

    product.pk=pk

    try: 
        product.save()
    except Exception as e:
        logger.error(f"Failed to update product: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save product: {str(e)}")
    
    logger.info(f"Product updated: {product}")
    return product


@app.delete("/product/{pk}")
def delete_product(pk:str): 
    logger.info(f"Deleting product: {pk}")
    try:
        Product.get(pk)
    except NotFoundError:
        logger.error(f"Product not found: {pk}")
        raise HTTPException(status_code=404, detail="Product not found")

    logger.info(f"Product deleted: {pk}")
    Product.delete(pk)
    return {"message": "Product deleted", "product_id": pk}

