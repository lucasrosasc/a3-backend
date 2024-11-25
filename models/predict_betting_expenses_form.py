from dataclasses import dataclass


@dataclass
class PredictBettingExpensesForm:
    name: str
    age: int
    gender: bool
    mensal_income: float
    social_class: int
    bets_frequency: int
