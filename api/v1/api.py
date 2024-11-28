from fastapi import APIRouter

from api.v1.endpoints import predict_betting_expenses, ranking


api_router = APIRouter()
api_router.include_router(
    predict_betting_expenses.router, prefix="/predict-betting-expenses", tags=["bets"]
)
api_router.include_router(
    ranking.router, prefix="/ranking", tags=["ranking"]
)


# /api/v1/predict-betting-expenses
