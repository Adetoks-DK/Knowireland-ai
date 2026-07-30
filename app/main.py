from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .models import Base

from .routers import company
from .routers import auth
from .routers import predictions
from .routers import dashboard
from .routers import analytics
from .routers import benchmarking


# CREATE DATABASE TABLES


Base.metadata.create_all(bind=engine)



# CREATE FASTAPI APPLICATION


app = FastAPI(
    title="KnowIreland Sustainability AI",
    description="Sustainability intelligence API for KnowIreland.ie",
    version="1.0.0"
)



# CORS CONFIGURATION


origins = [
    "https://knowireland.ie",
    "https://www.knowireland.ie",

    # Local development
    "http://localhost",
    "http://127.0.0.1:8000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# API HEALTH CHECK


@app.get("/")
def root():
    return {
        "application": "KnowIreland Sustainability AI",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "KnowIreland AI"
    }



# ROUTERS


app.include_router(company.router)

app.include_router(auth.router)

app.include_router(predictions.router)

app.include_router(dashboard.router)

app.include_router(analytics.router)

app.include_router(benchmarking.router)