from fastapi import FastAPI

app = FastAPI(
    title="Secure API", 
    description="REST API with security focus",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}