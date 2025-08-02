import json
import strawberry
from typing import List
from sqlalchemy.orm import Session
from strawberry.types import Info
from app.models.product import Product as ProductModel
from app.db import get_db
from app.redis_client import redis_client


# ✅ GraphQL Product type
@strawberry.type
class Product:
    id: int
    name: str
    price: int


# ✅ Query with Redis caching
@strawberry.type
class Query:
    @strawberry.field
    def products(self, info: Info) -> List[Product]:
        db: Session = info.context["db"]

        # ✅ Check Redis cache first
        cached_data = redis_client.get("products_cache")
        if cached_data:
            print("✅ GraphQL: Returning cached products")
            try:
                parsed = json.loads(cached_data)
                return [Product(**item) for item in parsed]
            except json.JSONDecodeError:
                print("⚠️ Cache corrupted, falling back to DB")

        # ❌ If not in cache, fetch from DB
        products = db.query(ProductModel).all()
        result = [{"id": p.id, "name": p.name, "price": p.price} for p in products]

        # ✅ Store in cache for 30 seconds
        redis_client.setex("products_cache", 30, json.dumps(result))
        print("✅ GraphQL: DB hit and cache set")

        return [Product(**p) for p in result]


# ✅ Mutation with cache invalidation
@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_product(self, info: Info, name: str, price: int) -> Product:
        db: Session = info.context["db"]
        new_product = ProductModel(name=name, price=price)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        # 🔁 Invalidate Redis cache
        redis_client.delete("products_cache")
        print("🧹 Cache invalidated after create")

        return Product(id=new_product.id, name=new_product.name, price=new_product.price)

    @strawberry.mutation
    def update_product(self, info: Info, id: int, name: str, price: int) -> Product:
        db: Session = info.context["db"]
        product = db.query(ProductModel).filter(ProductModel.id == id).first()
        if product:
            product.name = name
            product.price = price
            db.commit()
            db.refresh(product)

            # 🔁 Invalidate Redis cache
            redis_client.delete("products_cache")
            print("🧹 Cache invalidated after update")

            return Product(id=product.id, name=product.name, price=product.price)
        raise Exception("Product not found")

    @strawberry.mutation
    def delete_product(self, info: Info, id: int) -> bool:
        db: Session = info.context["db"]
        product = db.query(ProductModel).filter(ProductModel.id == id).first()
        if product:
            db.delete(product)
            db.commit()

            # 🔁 Invalidate Redis cache
            redis_client.delete("products_cache")
            print("🧹 Cache invalidated after delete")

            return True
        return False


# ✅ Schema definition
schema = strawberry.Schema(query=Query, mutation=Mutation)
