from typing import Dict, List, Type

from sqlalchemy.orm import Session
from pydantic import UUID4, EmailStr

from models.user_model import User
from schemas.user_schemas import IUser

class UserRepository:

    def __init__(self, session:Session) -> None:
        self._session = session
    
    def find_one(self, userId:UUID4) -> Type[User] | None:
        user = self._session.query(User).get(userId)
        return user
    
    def get_by_email(self, email:EmailStr)->Type[User] | None:
        user = self._session.query(User).filter_by(email=email).first()
        return user
    
    def get_by_username(self, username:str)-> Type[User] | None:
        user = self._session.query(User).filter_by(username=username).first()
        return user
    
    def create(self, data:Dict)->Type[User]:
        user = User(**data)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user
    
    def update(self, user:Type[User], data:Dict)->Type[User]:
        for key, value in data.items():
            setattr(user, key, value)
        self._session.commit()
        self._session.refresh(user)
        return user
    
    def delete(self, user:Type[User])->bool:
        self._session.delete(user)
        self._session.commit()
        return True
