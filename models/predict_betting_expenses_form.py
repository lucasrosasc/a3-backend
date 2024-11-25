from dataclasses import dataclass


@dataclass
class PredictBettingExpensesForm:
    name: str
    age: int
    gender: bool
    mensal_rent: float
    social_class: int
    bets_frequency: int
