from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from motor.motor_asyncio import AsyncIOMotorClient
import os

from app.candidates import router as candidates_router
from app.core.exceptions import CandidateNotFoundError, InvalidCandidateDataError, DuplicateEmailError
from app.core.database import db_obj

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup Mongo Client Connection using parameters safely
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    db_obj.client = AsyncIOMotorClient(mongo_url)
    yield
    db_obj.client.close()

app = FastAPI(
    title="Candidate Management API", 
    version="1.0.0", 
    description="Feature-Driven Architecture with MongoDB Atlas",
    lifespan=lifespan
)

app.include_router(candidates_router.router)

@app.exception_handler(CandidateNotFoundError)
async def candidate_not_found_handler(request: Request, exc: CandidateNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )

@app.exception_handler(DuplicateEmailError)
async def duplicate_email_handler(request: Request, exc: DuplicateEmailError):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )

@app.exception_handler(InvalidCandidateDataError)
async def invalid_candidate_data_handler(request: Request, exc: InvalidCandidateDataError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )
