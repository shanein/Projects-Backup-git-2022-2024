from typing import List

from pydantic import BaseModel
from controllers.authController import get_current_user_from_token
from controllers.terminalController import *
from database.database import get_db
from fastapi import APIRouter, Depends, Path, Body
from schemas.terminalSchema import (
    Terminal as TerminalBase,
    TerminalCreate as TerminalCreateSchema,
    TerminalUpdate,
)
from typing import List, Dict

router = APIRouter(tags=["Terminals"])
terminal_create_example = {
    "place_type": "Café",
    "name": "Café Central",
    "description": "Un café confortable au centre-ville",
    "localisation": "123 Rue Principale, Ville",
    "lat": 45.14796,
    "long": 5.72693,
    "last_update": "2023-01-01",
    "week_schedule": {
        "lundi": {"opening": "08:00", "closing": "18:00"},
        "mardi": {"opening": "08:00", "closing": "18:00"},
        "mercredi": {"opening": "08:00", "closing": "18:00"},
        "jeudi": {"opening": "08:00", "closing": "18:00"},
        "vendredi": {"opening": "08:00", "closing": "18:00"},
        "samedi": {"opening": "08:00", "closing": "18:00"},
        "dimanche": {"opening": "08:00", "closing": "18:00"},
    },
    "unavailable_dates": [
        {"start_date": "2023-12-24", "end_date": "2023-12-26"},
        {"start_date": "2024-01-01", "end_date": "2024-01-01"},
    ],
}

availability_example: List[dict] = [
    {"start_date": "2023-12-24", "end_date": "2023-12-26"},
    {"start_date": "2024-01-01", "end_date": "2024-01-01"},
]


class Availability(BaseModel):
    start_date: str
    end_date: str


class OpeningHours(BaseModel):
    lundi: dict
    mardi: dict
    mercredi: dict
    jeudi: dict
    vendredi: dict
    samedi: dict
    dimanche: dict


class DailyHours(BaseModel):
    opening: str
    closing: str


class TerminalAvailability(BaseModel):
    unavailable_dates: List[Availability]
    week_schedule: Dict[str, DailyHours]


@router.post("/terminal", response_model=TerminalBase or str)
def create_new_terminal(
    terminal: TerminalCreateSchema = Body(
        ..., description="Nouveau terminal à ajouter", examples=terminal_create_example
    ),
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    return create_terminal(user, terminal, db)


@router.delete("/terminal/{terminal_id}")
def remove_terminal(
    terminal_id: str = Path(
        ...,
        description="Id du terminal",
        examples="d47da73d-d3a0-43ef-82ea-5f9b3e38d03a",
    ),
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    db_terminal = delete_terminal(db=db, terminal_id=terminal_id)
    if db_terminal is None:
        raise HTTPException(status_code=404, detail="Terminal not found")
    return db_terminal


@router.patch("/terminal/{terminal_id}")
def update_terminal_by_id(
    terminal_id: str, terminalUpdate: TerminalUpdate, db: Session = Depends(get_db)
):
    terminal = update_terminal(terminal_id, terminalUpdate, db)
    return {"message": "Terminal updated successfully", "terminal": terminal}


@router.get("/terminal/{terminal_id}", response_model=TerminalBase)
def get_one_terminal(
    terminal_id: str = Path(
        ...,
        description="ID du terminal",
        examples="d47da73d-d3a0-43ef-82ea-5f9b3e38d03a",
    ),
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    return get_terminal(terminal_id, db)


@router.get("/terminal/{terminal_id}/availability", response_model=TerminalAvailability)
def get_one_terminal_availability(
    terminal_id: str = Path(
        ...,
        description="ID du terminal",
        examples="d47da73d-d3a0-43ef-82ea-5f9b3e38d03a",
    ),
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    return get_terminal_availability(terminal_id, db)


@router.post("/terminal/{terminal_id}/availability")
def add_one_terminal_availability(
    terminal_id: str = Path(
        ...,
        description="ID du terminal",
        examples="d47da73d-d3a0-43ef-82ea-5f9b3e38d03a",
    ),
    new_period: dict = Body(
        ...,
        description="Période d'indisponibilité à ajouter",
        examples={"start_date": "2023-12-24", "end_date": "2023-12-26"},
    ),
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    return add_unavailability_period(terminal_id, new_period, db)


@router.put(
    "/terminal/{terminal_id}/availability/{period_index}",
    response_model=List[Availability],
)
def update_one_terminal_availability(
    terminal_id: str = Path(
        ...,
        description="ID du terminal",
        examples="d47da73d-d3a0-43ef-82ea-5f9b3e38d03a",
    ),
    period_index: int = 0,
    updated_period: dict = Body(
        ...,
        description="Période d'indisponibilité à ajouter",
        examples={"start_date": "2023-12-24", "end_date": "2023-12-26"},
    ),
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    return update_unavailability_period(terminal_id, period_index, updated_period, db)


@router.put("/terminal/{terminal_id}/opening_hours", response_model=OpeningHours)
def update_one_terminal_opening_hours(
    terminal_id: str = Path(
        ...,
        description="ID du terminal",
        examples="d47da73d-d3a0-43ef-82ea-5f9b3e38d03a",
    ),
    new_schedule: dict = Body(
        ...,
        description="Nouvel horaire d'opening",
        examples={
            "lundi": {"opening": "08:00", "closing": "18:00"},
            "mardi": {"opening": "08:00", "closing": "18:00"},
            "mercredi": {"opening": "08:00", "closing": "18:00"},
            "jeudi": {"opening": "08:00", "closing": "18:00"},
            "vendredi": {"opening": "08:00", "closing": "18:00"},
            "samedi": {"opening": "08:00", "closing": "18:00"},
            "dimanche": {"opening": "08:00", "closing": "18:00"},
        },
    ),
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    return update_opening_hours(terminal_id, new_schedule, db)


@router.get("/terminal", response_model=List[TerminalBase])
def get_all_terminals(
    db: Session = Depends(get_db), user=Depends(get_current_user_from_token)
):
    return get_terminals_by_distributor(user.id, db)


@router.get(
    "/terminals-in-radius/{latitude}/{longitude}/{radius}",
    response_model=List[TerminalBase],
)
async def get_terminals_in_radius(
    latitude: float = Path(..., description="Latitude du lieu", examples=45.14796),
    longitude: float = Path(..., description="Longitude du lieu", examples=5.72693),
    radius: float = Path(
        ..., description="Rayon de recherche en metres", examples=1000
    ),
    db: Session = Depends(get_db),
):
    return find_terminals_in_radius(latitude, longitude, radius, db)


@router.delete("/terminal/{terminal_id}", response_model=TerminalBase)
def delete_one_terminal(
    terminal_id: str = Path(
        ...,
        description="ID du terminal",
        examples="d47da73d-d3a0-43ef-82ea-5f9b3e38d03a",
    ),
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    return delete_terminal(terminal_id, db)
