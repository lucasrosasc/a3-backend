from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.configs import settings
from core.database import engine
from models.prediction import Base
from api.v1.api import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Predict Betting Expenses - API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://a3-matematica-react.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# /api/v1/predict-betting-expenses
# /api/v1/predict-betting-expenses/:result_id
# /api/v1/ranking/age
# /api/v1/ranking/gender
# /api/v1/ranking/social-class
# /api/v1/ranking/bets-frequency
# /api/v1/ranking/all
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
