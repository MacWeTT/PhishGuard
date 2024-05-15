from fastapi.middleware.cors import CORSMiddleware
from database.databaseUtil import db_dependency
from database.connection import engine, Base
from machine_model import checkForPhishing
from models import Url, UrlResponseDTO
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_headers=["*"])

Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Connection to server successful."}


@app.post("/check-url")
async def check_url(requested_url: str, db: db_dependency):
    try:
        url = db.query(Url).filter(Url.address == requested_url).first()
        if url is not None:
            return UrlResponseDTO(requested_url)
        else:
            return checkForPhishing(requested_url)
    except Exception as e:
        return {"message": f"An error occured: {e}"}
