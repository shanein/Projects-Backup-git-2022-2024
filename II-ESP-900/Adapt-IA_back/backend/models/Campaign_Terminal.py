import datetime
import jwt
from sqlalchemy import (
    ARRAY,
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Boolean,
    UUID,
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Table
from database.database import Base, engine
import uuid
from models.Cible import Cible
from sqlalchemy.types import JSON
from sqlalchemy.dialects.postgresql import UUID as pgUUID

terminal_campaign_association = Table(
    "terminal_campaign",
    Base.metadata,
    Column(
        "terminal_id", UUID(as_uuid=True), ForeignKey("terminal.id"), primary_key=True
    ),
    Column(
        "campaign_id", UUID(as_uuid=True), ForeignKey("campaign.id"), primary_key=True
    ),
)


class Campaign(Base):
    __tablename__ = "campaign"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    budget = Column(Integer)
    is_smart = Column(Boolean)
    address = Column(String)
    postal_code = Column(String)
    is_active = Column(Boolean, default=True)
    is_valid = Column(Boolean, default=True)
    advertiser_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    advertiser = relationship("User", back_populates="campaigns")
    cible = relationship("Cible", back_populates="campaign")
    videos = relationship("Video", back_populates="campaign")
    terminals = relationship(
        "Terminal", secondary=terminal_campaign_association, back_populates="campaigns"
    )

    def to_dict(self):
        cibles_data = [cible.to_dict() for cible in self.cible]
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "budget": self.budget,
            "is_smart": self.is_smart,
            "address": self.address,
            "postal_code": self.postal_code,
            "is_active": self.is_active,
            "is_valid": self.is_valid,
            "advertiser_id": self.advertiser_id,
            "cible": cibles_data,
        }

    def to_dict_for_config(self):
        cibles_data = [cible.to_dict() for cible in self.cible]
        return {
            "id": self.id,
            "is_smart": self.is_smart,
            "cible": cibles_data,
        }


class Terminal(Base):
    __tablename__ = "terminal"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    place_type = Column(String)
    description = Column(String)
    localisation = Column(String)
    lat = Column(Float)
    long = Column(Float)
    start_date = Column(String)
    last_update = Column(Date)
    unavailable_dates = Column(JSON)
    week_schedule = Column(JSON)
    is_active = Column(Boolean, default=False)
    distributor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    distributor = relationship("User", back_populates="terminals")
    secret_key = Column(String)
    version = Column(String, default=None)
    ip_address = Column(String, default=None)
    campaigns = relationship(
        "Campaign", secondary=terminal_campaign_association, back_populates="terminals"
    )


Base.metadata.create_all(bind=engine)
