from sqlalchemy.orm import Session
from models.Cible import Cible
from schemas.cibleSchema import CibleCreate
import uuid


def create_cible(db: Session, cible: CibleCreate):
    db_cible = Cible(**cible.dict())
    db.add(db_cible)
    db.commit()
    db.refresh(db_cible)
    return db_cible


def get_cible(db: Session, cible_id: uuid.UUID):
    return db.query(Cible).filter(Cible.id == cible_id).first()


def get_cibles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Cible).offset(skip).limit(limit).all()


def delete_cible(db: Session, cible_id: uuid.UUID):
    db_cible = db.query(Cible).filter(Cible.id == cible_id).first()
    if db_cible:
        db.delete(db_cible)
        db.commit()
    return db_cible
