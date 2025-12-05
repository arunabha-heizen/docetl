from fastapi import FastAPI
from app.api.routes import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Document Verification Microservice")

app.include_router(router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}
