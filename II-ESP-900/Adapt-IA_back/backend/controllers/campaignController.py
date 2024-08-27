from datetime import date
from sqlalchemy.orm import Session
from controllers.videoController import create_video
from models.Cible import Cible
from schemas.campaignSchema import CampaignCreate, CampaignUpdate, CampaignUpdateIsValid
from typing import List, Optional
from models.Campaign_Terminal import Campaign
from fastapi import HTTPException, UploadFile, logger
from Exception.custom_exceptions import EmailAlreadyExists, UsernameTooShort
from models.User import User
from models.videoModel import Video
from Exception.custom_exceptions import SuccessResponse
import logging

# Créez un logger avec le nom de votre choix
logger = logging.getLogger(__name__)


from sqlalchemy.orm import Session
from fastapi import HTTPException
from controllers.terminalController import get_terminal


def create_campaign(db: Session, campaign: CampaignCreate, user_id: str):
    # Vérifiez si l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=422, detail="L'annonceur n'existe pas")
    if user.user_type != "advertiser" and not user.is_superuser:
        raise HTTPException(
            status_code=422, detail="L'utilisateur n'est pas un annonceur"
        )
    # Créer et ajouter des cibles associées à la campagne
    cibles = []
    for cible_data in campaign.cible:
        # Vérifier que la colonne age contient une liste de deux entiers
        if (
            not isinstance(cible_data.age, list)
            or len(cible_data.age) != 2
            or not all(isinstance(val, int) for val in cible_data.age)
        ):
            raise HTTPException(
                status_code=422, detail="L'âge doit être une liste de deux entiers."
            )

        new_cible = Cible(
            age=cible_data.age,
            genre=cible_data.genre,
            campaign_id=None,  # Notez que campaign_id est temporairement à None
        )
        cibles.append(new_cible)

    new_campaign = Campaign(
        name=campaign.name,
        description=campaign.description,
        start_date=campaign.start_date,
        end_date=campaign.end_date,
        budget=campaign.budget,
        is_smart=campaign.is_smart,
        address=campaign.address,
        postal_code=campaign.postal_code,
        is_active=False,
        is_valid=False,
        advertiser_id=user.id,
        cible=cibles,
    )
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)

    db.commit()
    db.refresh(new_campaign)
    return new_campaign


def create_campaign_draft(
    db: Session,
    campaign: CampaignUpdate,
    video_file: Optional[UploadFile],
    user_id: str,
):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=422, detail="L'annonceur n'existe pas")
        if user.user_type != "advertiser":
            raise HTTPException(
                status_code=422, detail="L'utilisateur n'est pas un annonceur"
            )

        # Créer et ajouter des cibles associées à la campagne
        cibles = []
        if campaign.cible is not None:  # Vérifier si campaign.cible est None
            for cible_data in campaign.cible:
                # Vérifier que la colonne age contient une liste de deux entiers
                if (
                    not isinstance(cible_data.age, list)
                    or len(cible_data.age) != 2
                    or not all(isinstance(val, int) for val in cible_data.age)
                ):
                    raise HTTPException(
                        status_code=422,
                        detail="L'âge doit être une liste de deux entiers.",
                    )

                new_cible = Cible(
                    age=cible_data.age,
                    genre=cible_data.genre,
                    campaign_id=None,  # Notez que campaign_id est temporairement à None
                )
                cibles.append(new_cible)

        new_campaign = Campaign(
            id=campaign.id,
            name=campaign.name,
            description=campaign.description,
            start_date=campaign.start_date,
            end_date=campaign.end_date,
            budget=campaign.budget,
            is_smart=campaign.is_smart,
            address=campaign.address,
            postal_code=campaign.postal_code,
            is_active=False,
            is_valid=False,
            advertiser_id=user.id,
            cible=cibles,
        )
        # Ajouter la campagne dans la base de données
        db.add(new_campaign)
        db.commit()
        db.refresh(new_campaign)

        # Journalisation appropriée
        logger.info("Campaign created successfully.")

        # Vérifier si une vidéo a été fournie
        if video_file is not None:
            # Appeler la fonction pour créer la vidéo avec le lien fourni et l'ID de la campagne
            video_response = create_video(
                video_file, campaign_id=new_campaign.id, db=db
            )
            db.commit()
            db.refresh(new_campaign)
            new_campaign.videoUrl = video_response.path

            # Journalisation appropriée
            logger.info("Video created successfully.")
        else:
            # Journalisation appropriée
            logger.info("No video provided for the campaign.")

        return (new_campaign,)

    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        logger.error(f"Error creating campaign with video: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error creating campaign with video. Check server logs for more details.",
        ) from e


# Update campaign_draft with video or without video (campaign_draft)
def update_is_active_campaignby_id(
    db: Session, campaign_id: str, is_active: bool, user_id: str
):
    try:
        # Vérifier si la campagne existe et appartient à l'utilisateur
        existing_campaign = (
            db.query(Campaign)
            .filter(Campaign.id == campaign_id, Campaign.advertiser_id == user_id)
            .first()
        )
        if existing_campaign is None:
            raise HTTPException(
                status_code=404,
                detail="La campagne n'existe pas ou n'appartient pas à l'utilisateur",
            )

        # Mettre à jour le champ is_active de la campagne
        existing_campaign.is_active = is_active

        # Enregistrez les modifications dans la base de données
        db.commit()
        db.refresh(existing_campaign)

        # Journaliser la mise à jour de la campagne
        logger.info("Campaign updated successfully.")
        return existing_campaign

    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        logger.error(f"Error updating campaign: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error updating campaign. Check server logs for more details.",
        ) from e


def update_is_valid_campaignby_id(
    db: Session, campaign_id: str, is_valid: bool, user_id: str
):
    try:
        # Vérifier si la campagne existe et appartient à l'utilisateur
        existing_campaign = (
            db.query(Campaign)
            .filter(Campaign.id == campaign_id, Campaign.advertiser_id == user_id)
            .first()
        )
        if existing_campaign is None:
            raise HTTPException(
                status_code=404,
                detail="La campagne n'existe pas ou n'appartient pas à l'utilisateur",
            )

        # Mettre à jour le champ is_active de la campagne
        existing_campaign.is_valid = is_valid

        # Enregistrez les modifications dans la base de données
        db.commit()
        db.refresh(existing_campaign)

        # Journaliser la mise à jour de la campagne
        logger.info("Campaign updated successfully.")
        return existing_campaign

    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        logger.error(f"Error updating campaign: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error updating campaign. Check server logs for more details.",
        ) from e


def update_draft_campaign(
    db: Session,
    campaign_id: str,
    campaign_update: CampaignCreate,
    video_file: Optional[UploadFile],
    user_id: str,
):
    try:
        # Vérifier si la campagne existe et appartient à l'utilisateur
        existing_campaign = (
            db.query(Campaign)
            .filter(Campaign.id == campaign_id, Campaign.advertiser_id == user_id)
            .first()
        )
        if existing_campaign is None:
            raise HTTPException(
                status_code=404,
                detail="La campagne n'existe pas ou n'appartient pas à l'utilisateur",
            )

        # Mettre à jour les champs de la campagne
        for field, value in campaign_update.dict().items():
            if value is not None:
                setattr(existing_campaign, field, value)

        # Enregistrez les modifications dans la base de données
        db.commit()
        db.refresh(existing_campaign)

        # Journaliser la mise à jour de la campagne
        logger.info("Campaign updated successfully.")

        # Vérifier si une vidéo a été fournie
        if video_file is not None:
            # Vérifier si une vidéo existe déjà pour la campagne
            existing_video = (
                db.query(Video).filter(Video.campaign_id == campaign_id).first()
            )

            if existing_video:
                # Mettre à jour la vidéo existante avec le lien fourni et l'ID de la campagne
                video_response = create_video(
                    video_file, campaign_id=campaign_id, db=db
                )
            else:
                # Créer une nouvelle vidéo avec le lien fourni et l'ID de la campagne
                video_response = create_video(
                    video_file, campaign_id=campaign_id, db=db
                )

            # Mettre à jour l'URL de la vidéo dans la campagne
            existing_campaign.videoUrl = video_response.path
            db.commit()
            db.refresh(existing_campaign)

            # Journaliser la mise à jour de la vidéo
            logger.info("Video updated/created successfully.")

        return existing_campaign

    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        logger.error(f"Error updating campaign: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error updating campaign. Check server logs for more details.",
        ) from e


def create_campaign_with_video(
    db: Session, campaign: CampaignCreate, video_file: UploadFile, user_id: str
):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=422, detail="L'annonceur n'existe pas")
        if user.user_type != "advertiser" and not user.is_superuser:
            raise HTTPException(
                status_code=422, detail="L'utilisateur n'est pas un annonceur"
            )
        # Traitement des cibles
        cibles = []
        if campaign.is_smart and not campaign.cible:
            raise HTTPException(status_code=422, detail="Cible is required")
        if campaign.is_smart:
            for cible_data in campaign.cible:
                if (
                    not isinstance(cible_data.age, list)
                    or len(cible_data.age) != 2
                    or not all(isinstance(val, int) for val in cible_data.age)
                ):
                    raise HTTPException(
                        status_code=422,
                        detail="L'âge doit être une liste de deux entiers.",
                    )
                new_cible = Cible(
                    age=cible_data.age, genre=cible_data.genre, campaign_id=None
                )
                cibles.append(new_cible)
                try:
                    campaign.budget = calc_price(
                        campaign.address, campaign.start_date, campaign.end_date
                    )
                except Exception as e:
                    raise HTTPException(
                        status_code=422,
                        detail="Error calculating price for smart campaign. Check server logs for more details.",
                    ) from e
        new_campaign = Campaign(
            name=campaign.name,
            description=campaign.description,
            start_date=campaign.start_date,
            end_date=campaign.end_date,
            budget=campaign.budget,
            is_smart=campaign.is_smart,
            address=campaign.address,
            postal_code=campaign.postal_code,
            is_active=False,
            is_valid=False,
            advertiser_id=user.id,
            cible=cibles,
            terminals=[],
        )
        db.add(new_campaign)
        db.flush()
        video_response = create_video(video_file, campaign_id=new_campaign.id, db=db)
        new_campaign.video_url = video_response.path
        if campaign.terminals:
            terminal_ids = campaign.terminals[0].split(",")
            for terminal_id in terminal_ids:
                terminal_id = terminal_id.strip()
                terminal = get_terminal(terminal_id, db)
                new_campaign.terminals.append(terminal)
        db.commit()
        db.refresh(new_campaign)
        return new_campaign.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating campaign with video: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error creating campaign with video. Check server logs for more details.",
        ) from e


def get_campaign(campaign_id: int, db: Session):
    try:
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        campaign.videoUrl = (
            db.query(Video).filter(Video.campaign_id == campaign_id).first().path
        )
        return campaign
    except:
        raise HTTPException(status_code=404, detail="Campaign not found")


def calc_price(address: str, start_date: date, end_date: date):
    fixed_daily_price = 15
    nbDays = (end_date - start_date) / (3600 * 24)
    return nbDays * fixed_daily_price


# def get_campaigns(db: Session):
#     campaigns = db.query(Campaign).all()
#     return campaigns

from controllers.campaignController import *


def update_campaign(campaign_id: int, campaign: CampaignCreate, db: Session):
    db.query(Campaign).filter(Campaign.id == campaign_id).update(campaign.dict())
    db.commit()

    updated_campaign = db.query(Campaign).get(campaign_id)

    if updated_campaign is None:
        pass  # Ajoutez une instruction pass si nécessaire

    response_data = SuccessResponse(
        message="La campagne a été mise à jour avec succès",
        data=updated_campaign.__dict__,
    )

    return response_data


def update_campaignIsValid(
    campaign_id: int, campaign_update: CampaignUpdateIsValid, db: Session, user_id: int
):
    # Récupération de la campagne existante dans la base de données
    existing_campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    # Vérification si la campagne existe
    if existing_campaign is None:
        raise HTTPException(status_code=404, detail="La campagne n'a pas été trouvée")

    # Vérification si la campagne est valide pour la mise à jour
    if not existing_campaign.is_valid:
        raise HTTPException(
            status_code=422, detail="La campagne n'est pas valide pour la mise à jour"
        )

    # Préparez le dictionnaire pour la mise à jour
    update_dict = {}
    if campaign_update.name:
        update_dict["name"] = campaign_update.name
    if campaign_update.description:
        update_dict["description"] = campaign_update.description

    # Mise à jour du budget si is_smart est True
    if existing_campaign.is_smart and campaign_update.budget is not None:
        update_dict["budget"] = campaign_update.budget

    # Mise à jour de la campagne dans la base de données
    if update_dict:
        db.query(Campaign).filter(Campaign.id == campaign_id).update(update_dict)
        db.commit()

    # Récupération de la campagne mise à jour
    updated_campaign = db.query(Campaign).get(campaign_id)

    # Convertir l'objet SQLAlchemy en un dictionnaire Python
    updated_campaign_dict = updated_campaign.__dict__

    # Supprimer les clés internes spécifiques à SQLAlchemy
    updated_campaign_dict.pop("_sa_instance_state", None)

    # Créez une instance de SuccessResponse pour la réponse
    response_data = SuccessResponse(
        message="La campagne a été mise à jour avec succès",
        data=updated_campaign_dict,
    )

    return response_data


def delete_campaign_by_id(campaign_id: int, db: Session):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    db.delete(campaign)
    db.commit()
    return True


def get_campaigns(advertiser_id: str, db: Session) -> List[Campaign]:
    try:
        campaigns = (
            db.query(Campaign).filter(Campaign.advertiser_id == advertiser_id).all()
        )
        if not campaigns:
            raise HTTPException(
                status_code=404,
                detail="Aucune campagne n'a été trouvée pour cet utilisateur.",
            )

        # Récupérer les URL des vidéos associées à chaque campagne
        for campaign in campaigns:
            video = db.query(Video).filter(Video.campaign_id == campaign.id).first()
            if video:
                campaign.videoUrl = video.path

        return campaigns

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des campagnes : {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Une erreur s'est produite lors de la récupération des campagnes. Veuillez consulter les journaux du serveur pour plus de détails.",
        ) from e


def get_campaign_by_terminal_id(db: Session, terminal_id: str):
    campaigns = db.query(Campaign).filter(Campaign.terminals.any(id=terminal_id)).all()
    if campaigns is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaigns
