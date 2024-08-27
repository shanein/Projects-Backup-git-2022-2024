from datetime import timedelta
from controllers.authController import *
from core.auth import create_access_token
from database.database import get_db
from core.settings import settings
from fastapi import APIRouter, Depends, HTTPException, status, APIRouter, Body
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import Token, UserAndToken
from schemas.userSchema import ShowUser, UserCreate
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, Response
import json

router = APIRouter(prefix="/auth", tags=["Users"])


@router.post(
    "/register",
    response_model=ShowUser,
    description="Crée un nouvel utilisateur, le user_type doit être soit 'distributor' ou 'advertiser'",
)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = await create_new_user(user=user, db=db)
    return user


@router.post("/login")
def login(user: Login, db: Session = Depends(get_db)):
    authenticated_user = authenticate_user(user.email, user.password, db)

    if not authenticated_user:
        raise HTTPException(
            status_code=422,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": authenticated_user.email}, expires_delta=access_token_expires
    )

    myuser = ShowUser.from_orm(authenticated_user)
    user_json = myuser.json()
    response = JSONResponse(
        content={
            "user": json.loads(user_json),  # Deserialize to ensure correct format
            "token": access_token,
        }
    )

    response.set_cookie(
        key="access_token",
        value="Bearer " + access_token,
        httponly=True,
    )

    return response


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=422,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/test")
def test_permission(current_user: UserCreate = Depends(get_current_user_from_token)):
    return {"message": "You are allowed to access this route"}


# @jwt_required()
@router.get("/info")
def my_infos(
    current_user: UserCreate = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    """
    Returns info on account
    """
    user = get_user(current_user.email, db)
    myuser = ShowUser.from_orm(user)
    user_json = myuser.json()
    return {
        "user": json.loads(user_json),
    }


# delete user by id
@router.delete("/delete/{id}")
def delete_user(id: str, db: Session = Depends(get_db)):
    user = delete_user_by_id(id, db)
    return {"message": "User deleted successfully"}


@router.patch("/update/{id}")
def update_user_by_id(id: str, userUpdate: UserUpdate, db: Session = Depends(get_db)):
    user = update_user(id, userUpdate, db)
    return {"message": "User updated successfully", "user": user}
