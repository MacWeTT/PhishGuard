from fastapi import FastAPI, BackgroundTasks
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
async def check_url(params: dict, background_task: BackgroundTasks):
    background_task.add_task(checkForPhishing(params.url))


@app.get("/prediction-result")
async def get_prediction_results(request_id: str):
    return {"prediction": "Website is legitimate", "accuracy": 0.85}
