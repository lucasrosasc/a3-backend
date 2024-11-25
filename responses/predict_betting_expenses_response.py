from dataclasses import dataclass
from uuid import UUID


@dataclass
class PredictBettingExpensesResponse:
    id: UUID
    name: str
    age: int
    social_class: int
    gender: int
    bets_frequency: int
    mensal_rent: float
    loss: float
    r2: float
