from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import checkForPhishing

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Connection to server successful."}


@app.post("/check-url")
async def check_url(params: dict):
    # res = checkForPhishing(params)
    res = True
    if res:
        response = {
            "code": 1,
            "message": "Site is suspicious. Please proceed with caution.",
        }
    else:
        response = {
            "code": 0,
            "message": "Site is not suspicious. You can browse safely.",
        }

    return response


@app.get("/prediction-result")
async def get_prediction_results(request_id: str):
    return {"prediction": "Website is legitimate", "accuracy": 0.85}
