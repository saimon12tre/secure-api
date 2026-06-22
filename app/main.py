from fastapi import FastAPI
from app.routers import auth
from app.database import engine
from app.models.user import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure API",
    description="REST API with security focus",
    version="1.0.0"
)

app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}