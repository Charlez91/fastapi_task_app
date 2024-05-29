from typing import Optional, Annotated
from pydantic import UUID4, Field, BaseModel, EmailStr

class IUserData(BaseModel):
    username : str
    email : EmailStr#might make it string

class IUser(IUserData):
    id : UUID4
    password : str

    class Config:
        orm_mode = True

class IUserRO(BaseModel):
    user : IUserData

class CreateUserDTO(BaseModel):
    username : str = Field(min_length=1, max_length=50, description="user username")
    email :EmailStr = Field(description="user email")
    password : str = Field(min_length=8, description="user password")

class LoginUserDTO(BaseModel):
    email :EmailStr
    password : str = Field(min_length=8)

class UpdateUserDTO(BaseModel):
    username : Annotated[Optional[str], Field(..., min_length=1, max_length=50,  description="user username")] = None
    email : Optional[EmailStr] = None
    password : Annotated[Optional[str], Field(min_length=8, description="user password")] = None

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
