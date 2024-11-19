from fastapi import APIRouter
from fastapi import status

from models.bets_form import BetsForm

router = APIRouter()


# POST Bets
@router.post("", status_code=status.HTTP_201_CREATED, response_model=BetsForm)
async def post_bets_form(bets_form: BetsForm):
    return bets_form
