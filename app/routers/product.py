from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.redis_client import redis_client
import json

router = APIRouter()

@router.get("/products", response_model=list[ProductOut])
def index(db: Session = Depends(get_db)):
    try:
        cached_data = redis_client.get("products_cache")
        if cached_data:
            print("✅ Returning cached products")
            return json.loads(cached_data)

        products = db.query(Product).all()

        # ✅ Serialize safely using Pydantic
        serialized = [ProductOut.from_orm(p).dict() for p in products]

        redis_client.setex("products_cache", 30, json.dumps(serialized))
        print("✅ DB hit and cache set")
        return serialized
    except SQLAlchemyError as e:
        print("❌ DB Error (GET all):", str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch products")

@router.get("/products/{id}", response_model=ProductOut)
def get(id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except SQLAlchemyError as e:
        print("❌ DB Error (GET by ID):", str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch product")

@router.post("/products", response_model=ProductOut, status_code=201)
def create(payload: ProductCreate, db: Session = Depends(get_db)):
    try:
        product = Product(**payload.dict())
        db.add(product)
        db.commit()
        db.refresh(product)
        redis_client.delete("products_cache")  # 🔁 Invalidate cache
        return product
    except SQLAlchemyError as e:
        print("❌ DB Error (POST):", str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create product")

@router.put("/products/{id}", response_model=ProductOut)
def update(id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product.name = payload.name
        product.price = payload.price
        db.commit()
        db.refresh(product)
        redis_client.delete("products_cache")  # 🔁 Invalidate cache
        return product
    except SQLAlchemyError as e:
        print("❌ DB Error (PUT):", str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update product")

@router.delete("/products/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        db.delete(product)
        db.commit()
        redis_client.delete("products_cache")  # 🔁 Invalidate cache
        return {"message": "Product deleted"}
    except SQLAlchemyError as e:
        print("❌ DB Error (DELETE):", str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete product")
