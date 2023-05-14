# from starlette.requests import Request
from fastapi import FastAPI, File, Query
from starlette.responses import Response
import functools
from model import CNN
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Humor hound",
    description="""Sarcasm detection app implementing fine-tuned DistilBERT model from HuggingFace""",
    version="0.1.0"
)

@functools.cache
def load_model():
    model = CNN()
    return model

model = load_model()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}


@app.post("/predict")
def predict(user_input: str = Query(..., min_length=3)):
    prediction = model._predict(user_input)
    return {"prediction": prediction}
    