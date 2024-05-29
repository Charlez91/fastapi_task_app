from typing import Type, Annotated
from typing_extensions import Doc
from datetime import datetime, UTC
from fastapi import Depends, HTTPException, status
from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .auth import (
    ALGORITHM,
    JWT_SECRET_KEY
)

from jose import jwt
from pydantic import ValidationError, EmailStr
from sqlalchemy.orm import Session

from schemas.user_schemas import TokenPayload, IUser
from config.database import get_db
from models.user_model import User

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/v1/user/login",
    scheme_name="JWT"
)

class UserAuthRequestForm(OAuth2PasswordRequestForm):

    def __init__(self, *args, Email: Annotated[
            EmailStr,
            Form(),
            Doc(
                """
                `email` string. The OAuth2 spec requires the exact field name
                `email`.
                """
            ),
        ], **kwargs):
        super().__init__(*args **kwargs)
        self.email = Email


async def get_current_user(session:Session= Depends(get_db), token: str = Depends(reuseable_oauth)) -> IUser:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        print(payload)
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user: Type[User] | None = session.query(User).filter_by(email=token_data.sub).first()
    
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return IUser(**user.__dict__)