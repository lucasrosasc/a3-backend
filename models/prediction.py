from sqlalchemy import Column, Float, String, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from core.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    social_class = Column(Integer, nullable=False)
    gender = Column(Integer, nullable=False)
    bets_frequency = Column(Integer, nullable=False)
    mensal_income = Column(Float, nullable=False)
    loss = Column(Float, nullable=False)
    r2 = Column(Float, nullable=False) 