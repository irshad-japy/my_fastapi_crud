# app/main.py
import json
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.redis_client import redis_client
from app.models.user_model import Base
from app.schemas.user_schema import UserCreate, UserInDB
from app.repository.user_repository import UserRepository

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserInDB)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    db_user = user_repo.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = user_repo.create_user(user)
    # Store user in Redis cache
    await redis_client.set(f"user:{new_user.id}", new_user.json())

    return new_user

@app.get("/users/{user_id}", response_model=UserInDB)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    # Try to fetch user from Redis cache
    cached_user = await redis_client.get(f"user:{user_id}")
    if cached_user:
        return UserInDB.parse_raw(cached_user)
    user_repo = UserRepository(db)
    db_user = user_repo.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Manually convert db_user to a dictionary
    user_dict = {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
        # add other fields as needed
    }
    # Serialize to JSON and store in Redis
    await redis_client.set(f"user:{user_id}", json.dumps(user_dict))

    return db_user
