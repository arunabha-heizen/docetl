from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.api.routes import router
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Document Verification Microservice")

app.include_router(router, prefix="/api/v1")

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("app/templates/index.html", "r") as f:
        return f.read()

@app.get("/health")
def health_check():
    return {"status": "ok"}
