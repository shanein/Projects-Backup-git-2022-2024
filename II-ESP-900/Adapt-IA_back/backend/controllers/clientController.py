from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime as date
from controllers.videoController import get_videos_by_campaign_id
from schemas.clientSchema import ClientConfig
from database.database import get_db
from sqlalchemy.orm import Session
from controllers.campaignController import get_campaign, get_campaign_by_terminal_id
from models.Campaign_Terminal import Terminal


def get_client_config(
    terminal_id: str,
    secret_key: str,
    version: str,
    ip: str,
    db: Session = Depends(get_db),
):
    terminal = db.query(Terminal).filter(Terminal.id == terminal_id).first()
    if terminal is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Terminal not found"
        )
    if terminal.secret_key != secret_key:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid secret key"
        )
    if version == terminal.version:
        return 204
    if terminal.ip_address is None:
        terminal.ip_address = ip
        db.commit()
    else:
        if terminal.ip_address != ip:
            print(f"IP address mismatch: {terminal.ip_address} != {ip}")
    campaigns = get_campaign_by_terminal_id(db, terminal_id)
    campaigns2 = []
    for campaign in campaigns:
        campaign_info = get_campaign(campaign.id, db)
        campaign = {"info": campaign_info.to_dict_for_config()}
    return {"version": terminal.version, "campaigns": campaigns}
