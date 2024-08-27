from sqlalchemy import Column, Integer, String, Boolean, Date, UUID
from database.database import Base, engine
from sqlalchemy.orm import relationship
import uuid


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    birthdate = Column(Date)
    phone_number = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    user_type = Column(String)
    last_login = Column(Date, nullable=True)
    company_name = Column(String)
    campaigns = relationship("Campaign", back_populates="advertiser")
    terminals = relationship("Terminal", back_populates="distributor")

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "birthdate": self.birthdate,
            "phone_number": self.phone_number,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "user_type": self.user_type,
            "last_login": self.last_login,
            "company_name": self.company_name,
        }


Base.metadata.create_all(bind=engine)
