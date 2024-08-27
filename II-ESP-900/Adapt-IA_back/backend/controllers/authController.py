from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from controllers.mailController import EmailSchema, simple_send, send_welcome_email
from core.auth import Hasher
from schemas.userSchema import UserCreate, UserUpdate
from models.User import User
from core.auth import Hasher, oauth2_scheme
from fastapi import Depends, HTTPException, status, Depends, Header
from database.database import get_db
from jose import JWTError, jwt
from core.settings import settings
from schemas.auth import Login
from datetime import timedelta
from core.auth import create_access_token
from typing import Optional, Dict
from jwt import decode, ExpiredSignatureError
from datetime import datetime, timedelta


async def create_new_user(user: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    if user.user_type not in ["distributor", "advertiser"]:
        raise HTTPException(
            status_code=400,
            detail="user_type must be either 'distributor' or 'advertiser'",
        )
    user = User(
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active=False,
        is_superuser=False,
        user_type=user.user_type,
        company_name=user.company_name,
        firstname=user.firstname,
        lastname=user.lastname,
        birthdate=user.birthdate,
        phone_number=user.phone_number,
        last_login=datetime.now(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    if user.id == 1:
        user.is_superuser = True
        db.commit()
        db.refresh(user)
    await send_welcome_email(email=user.email)
    return user


def update_user(user_id: int, user_update: UserUpdate, db: Session):
    # Recherchez l'utilisateur dans la base de données en fonction de son ID
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Mettez à jour les champs d'utilisateur nécessaires
    if user_update.firstname:
        user.firstname = user_update.firstname
    if user_update.lastname:
        user.lastname = user_update.lastname
    if user_update.phone_number:
        user.phone_number = user_update.phone_number
    db.commit()
    db.refresh(user)

    return user


def login(user: Login, db: Session):
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

    response = JSONResponse(
        content={
            "id": str(authenticated_user.id),  # Convert UUID to string
            "email": authenticated_user.email,
            "is_active": authenticated_user.is_active,
            "access_token": access_token,
        }
    )

    response.set_cookie(
        key="access_token",
        value="Bearer " + access_token,
        httponly=True,
    )

    return response


def get_user(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def authenticate_user(email: str, password: str, db: Session):
    user = get_user(email=email, db=db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


def authenticate_admin(email: str, password: str, db: Session):
    user = get_user(email=email, db=db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    if not user.is_superuser:
        return False
    return user


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        print("username/email extracted is ", username)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(email=username, db=db)
    if user is None:
        raise credentials_exception
    return user


def delete_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
