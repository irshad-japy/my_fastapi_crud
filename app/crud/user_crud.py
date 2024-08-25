# app/crud/user_crud.py
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# def create_user(db: Session, user: UserCreate):
#     db_user = User(
#         email=user.email,
#         hashed_password=user.hashed_password,  # Assuming you're hashing the password before this
#         full_name=user.full_name
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user