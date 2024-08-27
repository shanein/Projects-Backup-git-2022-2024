from sqlalchemy.orm import Session
from schemas.terminalSchema import TerminalCreate, TerminalUpdate
from models.Campaign_Terminal import Terminal
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import math
import random


def create_terminal(user, terminal_data: TerminalCreate, db: Session):
    if user.user_type != "distributor" and not user.is_superuser:
        raise HTTPException(
            status_code=403, detail="You are not allowed to create a terminal"
        )
    # Vérifier si un terminal avec le même nom existe déjà
    existing_terminal_name = (
        db.query(Terminal).filter(Terminal.name == terminal_data.name).first()
    )
    if existing_terminal_name:
        raise HTTPException(
            status_code=400, detail="A terminal with this name already exists"
        )
    existing_terminal_localisation = (
        db.query(Terminal)
        .filter(Terminal.localisation == terminal_data.localisation)
        .first()
    )
    if existing_terminal_localisation:
        raise HTTPException(
            status_code=400, detail="A terminal with this localisation already exists"
        )
    try:
        secret_key = "".join(random.choice("0123456789ABCDEF") for i in range(16))
        week_schedule = terminal_data.week_schedule
        unavailable_dates = terminal_data.unavailable_dates
        terminal = Terminal(
            place_type=terminal_data.place_type,
            name=terminal_data.name,
            description=terminal_data.description,
            localisation=terminal_data.localisation,
            start_date=terminal_data.start_date,
            last_update=datetime.utcnow(),
            lat=terminal_data.lat,
            long=terminal_data.long,
            unavailable_dates=unavailable_dates,
            week_schedule=week_schedule,
            distributor_id=user.id,
            is_active=False,
            secret_key=secret_key,
        )
        db.add(terminal)
        db.commit()
        db.refresh(terminal)
        terminal.version = generate_version_number(terminal.id, terminal.last_update)
        db.commit()

        return terminal
    except IntegrityError as e:
        db.rollback()
        if "unique constraint" in str(e):
            raise HTTPException(
                status_code=400, detail="A terminal with this name already exists"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"An unexpected error occurred: {str(e)}"
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


def update_terminal(terminal_id: str, terminal_update: TerminalUpdate, db: Session):
    # Recherchez le terminal dans la base de données en fonction de son ID
    terminal = db.query(Terminal).filter(Terminal.id == terminal_id).first()
    if terminal is None:
        raise HTTPException(status_code=404, detail="Terminal non trouvé")

    # Mettez à jour les champs du terminal nécessaires
    if terminal_update.name:
        terminal.name = terminal_update.name
    if terminal_update.description:
        terminal.description = terminal_update.description
    if terminal_update.place_type:
        terminal.place_type = terminal_update.place_type
    if terminal_update.unavailable_dates is not None:
        terminal.unavailable_dates = terminal_update.unavailable_dates
    db.commit()
    db.refresh(terminal)

    return terminal


def get_all_terminals(db: Session):
    terminals = db.query(Terminal).all()
    return terminals


def get_terminals_by_distributor(distributor_id: int, db: Session):
    terminals = (
        db.query(Terminal).filter(Terminal.distributor_id == distributor_id).all()
    )
    return terminals


def add_unavailability_period(terminal_id: str, new_period: dict, db: Session):
    terminal = db.query(Terminal).filter(Terminal.id == terminal_id).first()
    if not terminal:
        raise HTTPException(status_code=404, detail="Terminal not found")
    else:
        new_dates = list(terminal.unavailable_dates)
        new_dates.append(new_period)
        terminal.unavailable_dates = new_dates
        db.commit()
        return terminal.unavailable_dates


def update_unavailability_period(terminal_id, period_index, updated_period, db):
    terminal = db.query(Terminal).filter(Terminal.id == terminal_id).first()
    if terminal and 0 <= period_index < len(terminal.unavailable_dates):
        new_dates = list(terminal.unavailable_dates)
        new_dates[period_index] = updated_period
        terminal.unavailable_dates = new_dates
        db.commit()
        db.refresh(terminal)
        return terminal.unavailable_dates
    else:
        raise HTTPException(
            status_code=404, detail="Terminal not found or invalid period index"
        )


def update_opening_hours(terminal_id: str, new_schedule: dict, db):
    terminal = db.query(Terminal).filter(Terminal.id == terminal_id).first()
    if terminal:
        terminal.week_schedule = new_schedule
        db.commit()
        return terminal.week_schedule
    else:
        raise HTTPException(status_code=404, detail="Terminal not found")


def get_terminal_availability(terminal_id: str, db: Session):
    terminal = db.query(Terminal).filter(Terminal.id == terminal_id).first()
    if terminal:
        return {
            "unavailable_dates": terminal.unavailable_dates,
            "week_schedule": terminal.week_schedule,
        }
    else:
        raise HTTPException(status_code=404, detail="Terminal not found")


def get_terminal(terminal_id: str, db: Session):
    terminal = db.query(Terminal).filter(Terminal.id == terminal_id).first()
    if not terminal:
        raise HTTPException(status_code=404, detail="Terminal not found")
    return terminal


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (
        math.sin(dLat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dLon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def find_terminals_in_radius(latitude, longitude, radius, db):
    terminals = db.query(Terminal).all()
    nearby_terminals = []
    radius_in_km = radius / 1000
    for terminal in terminals:
        distance = haversine(latitude, longitude, terminal.lat, terminal.long)
        if distance <= radius_in_km:
            nearby_terminals.append(terminal)
    return nearby_terminals


def delete_terminal(terminal_id: int, db: Session):
    terminal = db.query(Terminal).filter(Terminal.id == terminal_id).first()
    if terminal is None:
        raise HTTPException(status_code=404, detail="Terminal not found")
    db.delete(terminal)
    db.commit()
    return True


SECRET_KEY = "pipouKey"
from sqlalchemy import event
import hashlib
import time


# def generate_jwt_token(terminal_id, last_update):
#     payload = {
#         "tid": str(terminal_id),  # Utilisation d'abréviations
#         "lu": str(last_update),
#     }
#     token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
#     return token


def generate_version_number(terminal_id, last_update):
    timestamp = int(time.time() * 1000)
    unique_string = f"{terminal_id}-{last_update}-{timestamp}"
    hash_object = hashlib.sha256(unique_string.encode())
    short_hash = hash_object.hexdigest()[:10]
    return short_hash


# def decode_jwt_token(token):
#     try:
#         decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         return decoded
#     except jwt.ExpiredSignatureError:
#         return "Token expired."
#     except jwt.InvalidTokenError:
#         return "Invalid token."


def terminal_update_listener(mapper, connection, target):
    token = generate_version_number(target.id, target.last_update)
    target.version = token


event.listen(Terminal, "before_update", terminal_update_listener)
