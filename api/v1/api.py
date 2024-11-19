from fastapi import APIRouter

from api.v1.endpoints import bets


api_router = APIRouter()
api_router.include_router(bets.router, prefix="/bets-form", tags=["bets"])


# /api/v1/bets-form
