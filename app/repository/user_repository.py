# app/repository/user_repository.py
from sqlalchemy.orm import Session
from app.crud import user_crud
from app.schemas.user_schema import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int):
        return user_crud.get_user(self.db, user_id)

    def get_user_by_email(self, email: str):
        return user_crud.get_user_by_email(self.db, email)

    def create_user(self, user: UserCreate):
        return user_crud.create_user(self.db, user)
