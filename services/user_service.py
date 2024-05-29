from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pydantic import UUID4, EmailStr

from repository.user_repository import UserRepository
from models.user_model import User
from schemas.user_schemas import CreateUserDTO, IUserRO, IUserData, UpdateUserDTO, IUser
from utils.auth import get_hashed_password

class UserService:

    def __init__(self, session:Session) -> None:
        self._session = session
        self.user_repository = UserRepository(session)
    
    def find_one(self, userId:UUID4)->IUserRO:
        user = self.user_repository.find_one(userId)#no need to await cos we need to run synchronously to throw exception
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User Not Found")
        return self._build_userRO(user)
    
    def find_by_email(self, email:EmailStr)->IUserRO:
        user = self.user_repository.get_by_email(email)#no need to await cos we need to run synchronously to throw exception
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User Not Found")
        return self._build_userRO(user)
    
    def find_by_username(self, email:EmailStr)->IUser:
        user = self.user_repository.get_by_username(email)#no need to await cos we need to run synchronously to throw exception
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User Not Found")
        return IUser(**user.__dict__)
    
    def create(self, data:CreateUserDTO)->IUserRO:
        if self.user_repository.get_by_email(data.email):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "User with email already exists")
        if self.user_repository.get_by_username(data.username):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "User with Username already exist")
        data.password = get_hashed_password(data.password)
        new_user = self.user_repository.create(data.model_dump(exclude_none=True))#.dict() is deprecated in this version of pydantic
        return self._build_userRO(new_user)
    
    def update(self, userId:UUID4, data:UpdateUserDTO)->IUserRO:
        user = self.user_repository.find_one(userId)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User does not exist")
        updated_user = self.user_repository.update(user, data.model_dump(exclude_none=True))
        return self._build_userRO(updated_user)
    
    def delete(self, userId:UUID4)->bool:
        user = self.user_repository.find_one(userId)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User does not exist")
        return self.user_repository.delete(user)
    
    @staticmethod
    def _build_userRO(user:Type[User])->IUserRO:
        _user_data : IUserData = IUserData(**user.__dict__)
        return IUserRO(user = _user_data)