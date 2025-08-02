from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True  # ✅ required for .from_orm()
