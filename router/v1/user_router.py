from typing import Annotated, Dict

from fastapi import APIRouter, Depends, Body, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas.user_schemas import IUserRO, CreateUserDTO, IUser, TokenSchema, LoginUserDTO, UpdateUserDTO
from services.user_service import UserService
from config.database import get_db
from utils.deps import get_current_user
from utils.auth import verify_password, create_access_token, create_refresh_token

router = APIRouter(
    prefix="/user",
    tags= ['user']
)

@router.get("/", summary="Get A User details", response_model=IUserRO, status_code=status.HTTP_200_OK)
async def get_user(user:IUser=Depends(get_current_user), session:Session = Depends(get_db)):
    _service = UserService(session=session)
    return _service.find_one(user.id)


@router.post("/", summary="Create A New User", response_model=IUserRO, status_code=status.HTTP_201_CREATED)
@router.post("/register", summary="Register A New User", response_model=IUserRO)
async def register(data: Annotated[CreateUserDTO, Body()], session:Annotated[Session, Depends(get_db)]):
    _service = UserService(session)
    return _service.create(data)


@router.post("/login", summary="Login User to Obtain Tokens", response_model=TokenSchema)
async def login(data:Annotated[OAuth2PasswordRequestForm, Depends()], session:Annotated[Session, Depends(get_db)]):
    _service = UserService(session)
    user = _service.find_by_username(data.username)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User with Username doesnt exist")
    
    if not verify_password(data.password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Login Unsuccessful. Wrong Password")
    
    tokens = { "access_token":create_access_token(user.email), "refresh_token":create_refresh_token(user.email)}

    return TokenSchema(**tokens)


@router.patch("/", summary="Update User Details", response_model=IUserRO)
@router.put("/", summary="Update User Details", response_model=IUserRO)
def update(
    user : Annotated[IUser, Depends(get_current_user)], 
    data:Annotated[UpdateUserDTO, Body()], session:Annotated[Session, Depends(get_db)]
    ):
    _service = UserService(session)
    return _service.update(user.id, data)


@router.delete("/", summary="Delete A User Profile", status_code=status.HTTP_204_NO_CONTENT)
def delete(user:Annotated[IUser, Depends(get_current_user)], session:Annotated[Session, Depends(get_db)]):
    _service = UserService(session)
    return _service.delete(user.id)
