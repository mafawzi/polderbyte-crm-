import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .database import engine, Base
from .routers import auth, companies, contacts, deals, activities, ai_endpoints

load_dotenv()

# Creates tables if they don't exist yet. For production schema changes,
# switch to Alembic migrations instead of relying on this.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRM API", version="1.0.0")

origins = os.getenv("FRONTEND_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(contacts.router)
app.include_router(deals.router)
app.include_router(activities.router)
app.include_router(ai_endpoints.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "CRM API"}


@app.get("/health")
def health():
    return {"status": "healthy"}
