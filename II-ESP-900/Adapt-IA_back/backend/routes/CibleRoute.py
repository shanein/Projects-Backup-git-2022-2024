from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from controllers.cibleController import *
from schemas.cibleSchema import CibleCreate, Cible
from database.database import get_db
from controllers.authController import get_current_user_from_token

router = APIRouter()


@router.post("/cibles/", response_model=Cible)
def create_cible(
    cible: CibleCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    return create_cible(db=db, cible=cible)


@router.get("/cibles/", response_model=List[Cible])
def read_cibles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    return get_cibles(db, skip=skip, limit=limit)


@router.get("/cibles/{cible_id}", response_model=Cible)
def read_cible(
    cible_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    db_cible = get_cible(db=db, cible_id=cible_id)
    if db_cible is None:
        raise HTTPException(status_code=404, detail="Cible not found")
    return db_cible


@router.delete("/cibles/{cible_id}", response_model=Cible)
def delete_cible(
    cible_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    db_cible = delete_cible(db=db, cible_id=cible_id)
    if db_cible is None:
        raise HTTPException(status_code=404, detail="Cible not found")
    return db_cible
