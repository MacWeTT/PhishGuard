from fastapi.middleware.cors import CORSMiddleware
from machine_model import checkForPhishing
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(CORSMiddleware)


@app.get("/")
async def root():
    return {"message": "Connection to server successful."}


@app.post("/check-url")
async def check_url(url: str):
    flag = contains_unicode(url)
    try:
        return checkForPhishing(url,flag)
    except Exception as e:
        return {"message": f"An error occured: {e}"}

def contains_unicode(s:str):
    return any(ord(char) > 127 for char in s)