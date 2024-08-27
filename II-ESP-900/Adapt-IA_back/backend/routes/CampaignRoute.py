from datetime import timedelta
from typing import List
from schemas.cibleSchema import CibleCreateInCampaign

from controllers.authController import get_current_user_from_token
from controllers.campaignController import *
from core.auth import create_access_token
from core.settings import settings
from database.database import get_db
from json.decoder import JSONDecodeError
from pydantic import ValidationError

from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    HTTPException,
    Path,
    UploadFile,
    status,
    Form,
)
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import Token
from schemas.campaignSchema import (
    BodyCreateNewCampaignWithVideo,
    Campaign as CampaignSchema,
    CampaignCreate,
    CampaignNew,
    CampaignUpdate,
    CampaignUpdateIsValid,
)
from schemas.campaignSchema import CampaignCreate
from schemas.targetSchema import Target
from sqlalchemy.orm import Session
import json
import uuid

router = APIRouter(tags=["Campaign"])
Campaign_create_example = {
    "name": "Campagne 1",
    "description": "Une campagne",
    "start_date": "2023-01-01",
    "end_date": "2023-01-01",
    "budget": 1000,
    "is_smart": True,
    "address": "123 Rue Principale, Ville",
    "postal_code": "75000",
    "cible": [
        {
            "age": 18,
            "genre": "Female",
        },
        {
            "age": 15,
            "genre": "Male",
        },
    ],
}


# @router.post(
#     "/campaigns/",
#     description="Crée une nouvelle campagne. Seuls les utilisateurs de type 'advertiser' sont autorisés à effectuer cette opération.",
#     response_description="Détails de la campagne créée",
# )
# def create_new_campaign(
#     campaign: CampaignCreate = Body(
#         ..., description="Nouvelle campagne à ajouter", examples=Campaign_create_example
#     ),
#     db: Session = Depends(get_db),
#     user=Depends(get_current_user_from_token),
# ):
#     # Vérifiez si l'utilisateur est un annonceur avant de créer la campagne

#     return create_campaign(db=db, campaign=campaign, user_id=user.id)


# @router.get("/campaigns/", response_model=List[Campaign])
# def read_campaigns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user = Depends(get_current_user_from_token)):
#     return get_campaigns(db, skip=skip, limit=limit)
@router.post("/campaigns/")
async def create_new_campaign_with_video(
    name: str = Form(...),
    description: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    budget: int = Form(...),
    is_smart: bool = Form(...),
    address: str = Form(...),
    postal_code: str = Form(...),
    cibles_json: str = Form(...),
    video_file: UploadFile = File(...),
    terminals: List[str] = Form(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    # Convertir les cibles JSON en objets Python
    # cibles = json.loads(cibles_json)
    cibles = json.loads(cibles_json)
    # Créer une instance de CampaignCreate
    campaign_data = CampaignCreate(
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        is_smart=is_smart,
        address=address,
        postal_code=postal_code,
        cible=cibles,
        terminals=terminals,
    )

    # Passer les données à votre fonction de contrôleur
    result = create_campaign_with_video(
        db=db, campaign=campaign_data, video_file=video_file, user_id=user.id
    )
    return result


@router.get("/campaigns/{campaign_id}")
def read_campaign(
    campaign_id: str = Path(
        ...,
        description="Id de la campagne",
        examples="d47da73d-d3a0-43ef-82ea-5f9b3e38d03a",
    ),
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    db_campaign = get_campaign(db=db, campaign_id=campaign_id)
    if db_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return db_campaign


@router.get("/campaigns/price/")
def get_price(
    address: str,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    return 1500


@router.delete("/campaigns/{campaign_id}")
def remove_campaign(
    campaign_id: str = Path(
        ...,
        description="Id de la campagne",
        examples="d47da73d-d3a0-43ef-82ea-5f9b3e38d03a",
    ),
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    db_campaign = delete_campaign_by_id(db=db, campaign_id=campaign_id)
    if db_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return db_campaign


@router.get("/campaign/targets", response_model=Target)
def get_target_info():
    # Simulation de données pour l'exemple
    target_data = Target(
        age=[
            "Children (0-12 years)",
            "Teenagers (13-19 years)",
            "Adults (20-60 years)",
            "Seniors (60+ years)",
        ],
        gender=["Males", "Females", "Other"],
        clothing_Style=["Casual", "Professional", "Sporty", "Elegant"],
        clothing_Color=[
            "Black",
            "White",
            "Red",
            "Blue",
            "Green",
            "Yellow",
            "Orange",
            "Purple",
            "Pink",
            "Brown",
            "Grey",
        ],
    )
    return target_data


@router.get("/campaigns/")
def read_campaigns(
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    return get_campaigns(advertiser_id=user.id, db=db)


# New route to update a campaign


@router.post("/campaignsdraft")
async def create_draft_campaign_with_video(
    name: str = Form(None),
    description: str = Form(None),
    start_date: str = Form(None),
    end_date: str = Form(None),
    budget: int = Form(None),
    is_smart: bool = Form(None),
    address: str = Form(None),
    postal_code: str = Form(None),
    cibles_json: str = Form(None),
    video_file: UploadFile = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    try:
        # Convert the JSON string to a list of objects
        cibles = json.loads(cibles_json) if cibles_json else None
    except json.JSONDecodeError as e:
        # Handle invalid JSON
        raise HTTPException(status_code=422, detail="Invalid JSON for 'cibles'.")

    try:
        # Create an instance of CampaignNew
        campaign_data = CampaignNew(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            is_smart=is_smart,
            address=address,
            postal_code=postal_code,
            cible=cibles,
        )

        # Pass the data to your controller function
        result = create_campaign_draft(
            campaign=campaign_data, video_file=video_file, db=db, user_id=user.id
        )

        return result

    except ValidationError as e:
        # Handle validation errors from CampaignNew model
        raise HTTPException(status_code=422, detail=str(e))


@router.patch("/campaigndraft/{campaign_id}")
def update_draft_campaign_with_video(
    campaign_id: str,
    name: str = Form(None),
    description: str = Form(None),
    start_date: str = Form(None),
    end_date: str = Form(None),
    budget: int = Form(None),
    is_smart: bool = Form(None),
    address: str = Form(None),
    postal_code: str = Form(None),
    cibles_json: str = Form(None),
    video_file: UploadFile = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    # Convertir les cibles JSON en objets Python
    try:
        # Convert the JSON string to a list of objects
        cibles = json.loads(cibles_json) if cibles_json else None
    except json.JSONDecodeError as e:
        # Handle invalid JSON
        raise HTTPException(status_code=422, detail="Invalid JSON for 'cibles'.")

    campaign_update_data = CampaignUpdate(
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        is_smart=is_smart,
        address=address,
        postal_code=postal_code,
        cible=cibles,
    )

    # Passer les données à votre fonction de contrôleur
    result = update_draft_campaign(
        campaign_id=campaign_id,
        campaign_update=campaign_update_data,
        video_file=video_file,
        db=db,
        user_id=user.id,
    )

    return result


@router.patch("/updateCampaignIsValid/{campaign_id}")
def update_draft_campaign_is_valid(
    campaign_id: str,
    update_data: CampaignUpdateIsValid,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    campaign_update_data = CampaignUpdateIsValid(
        name=update_data.name,
        description=update_data.description,
        budget=update_data.budget,
    )
    # Passer les données à votre fonction de contrôleur
    result = update_campaignIsValid(
        campaign_id=campaign_id,
        campaign_update=campaign_update_data,
        db=db,
        user_id=user.id,
    )
    return result


# update_draft_campaign_with_video avec path params campaign_id


@router.patch("/updateisactive/{campaign_id}")
def update_is_active(
    campaign_id: str,
    is_active: bool,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    return update_is_active_campaignby_id(
        db=db, campaign_id=campaign_id, is_active=is_active, user_id=user.id
    )


@router.patch("/updateisValid/{campaign_id}")
def update_is_valid(
    campaign_id: str,
    is_valid: bool,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    return update_is_valid_campaignby_id(
        db=db, campaign_id=campaign_id, is_valid=is_valid, user_id=user.id
    )
