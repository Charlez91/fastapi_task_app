import os
from datetime import datetime, timedelta, UTC
from typing import Union, Any, Optional

from jose import jwt
from passlib.context import CryptContext

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ.get('SECRET_KEY', "SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.environ.get('JWT_REFRESH_SECRET_KEY', "JWT_REFRESH_SECRET_KEY")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: Optional[int] = None) -> str:
    if expires_delta is not None:
        expires_delta = int((datetime.now(UTC) + timedelta(minutes=expires_delta)).timestamp())
    else:
        expires_delta = int((datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: Optional[int] = None) -> str:
    if expires_delta is not None:
        expires_delta = int((datetime.now(UTC) + timedelta(minutes=expires_delta)).timestamp())
    else:
        expires_delta = int((datetime.now(UTC) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)).timestamp())
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt