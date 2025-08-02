import strawberry

@strawberry.type
class ProductType:
    id: int
    name: str
    price: int
