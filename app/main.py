from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

from app.database import engine, get_db
from app import models, crud, schemas
from app.schemas import URLCreate
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener",
    description="A simple URL shortener built with FastAPI + PostgreSQL",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.post("/shorten", response_model=schemas.URLResponse, status_code=201)
def shorten_url(payload: URLCreate, db: Session = Depends(get_db)):
    long_url = str(payload.long_url)
    db_url = crud.create_short_url(db=db, long_url=long_url)
    return schemas.URLResponse(
        short_code=db_url.short_code,
        long_url=db_url.long_url,
        short_url=f"{BASE_URL}/{db_url.short_code}",
        created_at=db_url.created_at
    )

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_code(db=db, short_code=short_code)
    if not db_url:
        raise HTTPException(
            status_code=404,
            detail=f"Short code '{short_code}' not found"
        )
    return RedirectResponse(url=db_url.long_url, status_code=302)