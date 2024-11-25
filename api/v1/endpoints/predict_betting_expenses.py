from fastapi import APIRouter, HTTPException, Depends
from fastapi import status
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from uuid import UUID
from sqlalchemy.orm import Session

from models.predict_betting_expenses_form import PredictBettingExpensesForm
from models.prediction import Prediction
from responses.predict_betting_expenses_response import PredictBettingExpensesResponse
from core.database import get_db

router = APIRouter()

# POST Bets
@router.post("", status_code=status.HTTP_200_OK, response_model=PredictBettingExpensesResponse)
async def post_predict_betting_expenses(
    predict_betting_expenses_form: PredictBettingExpensesForm,
    db: Session = Depends(get_db)
):
    # Data simulation based on the information provided
    data = {
        "age": [18, 25, 30, 35, 40, 45, 50, 55, 60],
        "social_class": [1, 2, 1, 2, 3, 1, 3, 2, 3],  # 1: A/B, 2: C, 3: D/E
        "gender": [0, 1, 0, 1, 1, 0, 1, 0, 0],  # 0: Male, 1: Female
        "bets_frequency": [1, 3, 2, 5, 4, 1, 0, 1, 2],  # Number of bets per week
        "mensal_income": [
            2000,
            3000,
            2500,
            4000,
            3500,
            1500,
            1000,
            2000,
            800,
        ],  # Monthly rent in R$
        "bets_spent": [200, 300, 150, 400, 250, 100, 90, 60, 30],  # Monthly spent in R$
    }

    # Dataframe creation
    df = pd.DataFrame(data)

    # Separation of independent and dependent variables
    X = df[["age", "social_class", "gender", "bets_frequency", "mensal_income"]]
    y = df["bets_spent"]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Creation of the linear regression model with regularization (Ridge)
    ridge_model = Ridge(alpha=1.0)
    ridge_model.fit(X_train, y_train)

    # Predictions on the test set
    y_pred = ridge_model.predict(X_test)

    # Calculation of the coefficient of determination R^2
    r2 = r2_score(y_test, y_pred)

    # Function for forecasting expenses with checking negative values
    def predict_spend(age, social_class, gender, bets_frequency, mensal_income):
        input_data = np.array([[age, social_class, gender, bets_frequency, mensal_income]])
        predicted_gasto = ridge_model.predict(input_data)
        return max(predicted_gasto[0], 0)  # Ensures the value is not negative

    try:
        name = predict_betting_expenses_form.name
        if not name.strip():
            raise ValueError("O nome não pode estar em branco.")

        age = int(predict_betting_expenses_form.age)
        if not (18 <= age <= 100):
            raise ValueError("age deve estar entre 18 e 100.")

        social_class = int(predict_betting_expenses_form.social_class)
        if social_class not in [1, 2, 3]:
            raise ValueError("Classe social deve ser 1, 2 ou 3.")

        gender = int(predict_betting_expenses_form.gender)
        if gender not in [0, 1]:
            raise ValueError("Gênero deve ser 0 ou 1.")

        bets_frequency = int(predict_betting_expenses_form.bets_frequency)
        if not (0 <= bets_frequency <= 7):
            raise ValueError("A frequência de apostas deve ser entre 0 e 7.")

        mensal_income = float(predict_betting_expenses_form.mensal_income)
        if mensal_income < 0:
            raise ValueError("A renda mensal deve ser um valor positivo.")
        # Prediction and result
        expected_expense = predict_spend(
            age, social_class, gender, bets_frequency, mensal_income
        )
        
        # Convert numpy values to Python native types
        expected_expense_float = float(expected_expense)
        r2_float = float(r2)
        
        new_prediction = Prediction(
            name=name,
            age=age,
            social_class=social_class,
            gender=gender,
            bets_frequency=bets_frequency,
            mensal_income=mensal_income,
            loss=expected_expense_float,
            r2=r2_float
        )
        db.add(new_prediction)
        db.commit()
        db.refresh(new_prediction)
        
        return PredictBettingExpensesResponse(
            id=new_prediction.id,
            name=new_prediction.name,
            age=new_prediction.age,
            social_class=new_prediction.social_class,
            gender=new_prediction.gender,
            bets_frequency=new_prediction.bets_frequency,
            mensal_income=new_prediction.mensal_income,
            loss=new_prediction.loss,
            r2=new_prediction.r2
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{prediction_id}", response_model=PredictBettingExpensesResponse)
async def get_prediction(prediction_id: UUID, db: Session = Depends(get_db)):
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found"
        )
    
    return PredictBettingExpensesResponse(
        id=prediction.id,
        name=prediction.name,
        age=prediction.age,
        social_class=prediction.social_class,
        gender=prediction.gender,
        bets_frequency=prediction.bets_frequency,
        mensal_income=prediction.mensal_income,
        loss=prediction.loss,
        r2=prediction.r2
    )
