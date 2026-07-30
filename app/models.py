from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

from .database import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from .database import Base



class Company(Base):

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    company_name = Column(String(150))

    industry = Column(String(100))

    employees = Column(Integer)

    annual_revenue = Column(Float)

    country = Column(String(80))

    created_at = Column(TIMESTAMP, server_default=func.now())

    predictions = relationship(
    "SustainabilityPrediction",
    back_populates="company"
)


class SustainabilityPrediction(Base):

    __tablename__ = "sustainability_predictions"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id"))

    energy_consumption = Column(Float)

    water_consumption = Column(Float)

    waste_generated = Column(Float)

    recycling_rate = Column(Float)

    renewable_energy = Column(Float)

    transport_emissions = Column(Float)

    carbon_emissions = Column(Float)

    sustainability_score = Column(Float)

    recommendations = Column(Text)

    prediction_date = Column(TIMESTAMP, server_default=func.now())

    company = relationship(
    "Company",
    back_populates="predictions"
)
    
from sqlalchemy import Column, Integer, String

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    fullname = Column(
        String(255),
        nullable=False
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    company = Column(
        String(255)
    )

    password = Column(
        String(255),
        nullable=False
    )


