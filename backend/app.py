from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from models.facts import MarketingRequest
# from services.marketing_service import analyze_marketing_strategy


app = FastAPI()

#CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
