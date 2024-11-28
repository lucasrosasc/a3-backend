from sqlalchemy import func
from typing import List
from dataclasses import dataclass
from fastapi import APIRouter,  Depends
from sqlalchemy.orm import Session

from models.prediction import Prediction
from core.database import get_db

router = APIRouter()


@dataclass
class AgeRankingResponse:
    age: int
    total_loss: float
    average_loss: float
    count: int

@dataclass
class GenderRankingResponse:
    gender: int
    total_loss: float
    average_loss: float
    count: int

@dataclass
class SocialClassRankingResponse:
    social_class: int
    total_loss: float
    average_loss: float
    count: int

@dataclass
class BetsFrequencyRankingResponse:
    bets_frequency: int
    total_loss: float
    average_loss: float
    count: int

@dataclass
class AllRankingsResponse:
    age_rankings: List[AgeRankingResponse]
    gender_rankings: List[GenderRankingResponse]
    social_class_rankings: List[SocialClassRankingResponse]
    bets_frequency_rankings: List[BetsFrequencyRankingResponse]

@router.get("/age", response_model=List[AgeRankingResponse])
async def get_age_ranking(db: Session = Depends(get_db)):
    """
    Returns aggregated statistics of losses by age for visualization purposes.
    Includes total loss, average loss, and count of predictions for each age.
    """
    rankings = (
        db.query(
            Prediction.age,
            func.sum(Prediction.loss).label('total_loss'),
            func.avg(Prediction.loss).label('average_loss'),
            func.count(Prediction.id).label('count')
        )
        .group_by(Prediction.age)
        .order_by(Prediction.age)
        .all()
    )
    
    return [
        AgeRankingResponse(
            age=rank.age,
            total_loss=float(rank.total_loss),  # Convert Decimal to float
            average_loss=float(rank.average_loss),  # Convert Decimal to float
            count=rank.count
        )
        for rank in rankings
    ]

@router.get("/gender", response_model=List[GenderRankingResponse])
async def get_gender_ranking(db: Session = Depends(get_db)):
    """
    Returns aggregated statistics of losses by gender for visualization purposes.
    Includes total loss, average loss, and count of predictions for each gender.
    """
    rankings = (
        db.query(
            Prediction.gender,
            func.sum(Prediction.loss).label('total_loss'),
            func.avg(Prediction.loss).label('average_loss'),
            func.count(Prediction.id).label('count')
        )
        .group_by(Prediction.gender)
        .order_by(Prediction.gender)
        .all()
    )
    
    return [
        GenderRankingResponse(
            gender=rank.gender,
            total_loss=float(rank.total_loss),
            average_loss=float(rank.average_loss),
            count=rank.count
        )
        for rank in rankings
    ]

@router.get("/social-class", response_model=List[SocialClassRankingResponse])
async def get_social_class_ranking(db: Session = Depends(get_db)):
    """
    Returns aggregated statistics of losses by social class for visualization purposes.
    Includes total loss, average loss, and count of predictions for each social class.
    """
    rankings = (
        db.query(
            Prediction.social_class,
            func.sum(Prediction.loss).label('total_loss'),
            func.avg(Prediction.loss).label('average_loss'),
            func.count(Prediction.id).label('count')
        )
        .group_by(Prediction.social_class)
        .order_by(Prediction.social_class)
        .all()
    )
    
    return [
        SocialClassRankingResponse(
            social_class=rank.social_class,
            total_loss=float(rank.total_loss),
            average_loss=float(rank.average_loss),
            count=rank.count
        )
        for rank in rankings
    ]

@router.get("/bets-frequency", response_model=List[BetsFrequencyRankingResponse])
async def get_bets_frequency_ranking(db: Session = Depends(get_db)):
    """
    Returns aggregated statistics of losses by bets frequency for visualization purposes.
    Includes total loss, average loss, and count of predictions for each bets frequency.
    """
    rankings = (
        db.query(
            Prediction.bets_frequency,
            func.sum(Prediction.loss).label('total_loss'),
            func.avg(Prediction.loss).label('average_loss'),
            func.count(Prediction.id).label('count')
        )
        .group_by(Prediction.bets_frequency)
        .order_by(Prediction.bets_frequency)
        .all()
    )
    
    return [
        BetsFrequencyRankingResponse(
            bets_frequency=rank.bets_frequency,
            total_loss=float(rank.total_loss),
            average_loss=float(rank.average_loss),
            count=rank.count
        )
        for rank in rankings
    ]

@router.get("/all", response_model=AllRankingsResponse)
async def get_all_rankings(db: Session = Depends(get_db)):
    """
    Returns all rankings (age, gender, social class, bets frequency) in a single response.
    """
    age_rankings = await get_age_ranking(db)
    gender_rankings = await get_gender_ranking(db)
    social_class_rankings = await get_social_class_ranking(db)
    bets_frequency_rankings = await get_bets_frequency_ranking(db)
    
    return AllRankingsResponse(
        age_rankings=age_rankings,
        gender_rankings=gender_rankings,
        social_class_rankings=social_class_rankings,
        bets_frequency_rankings=bets_frequency_rankings
    )
