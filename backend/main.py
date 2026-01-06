from fastapi import FastAPI
from pydantic import BaseModel
from checker import check_claim
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Fact Checker IA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Claim(BaseModel):
    text: str

@app.post("/fact-check")
def fact_check(claim: Claim):
    return check_claim(claim.text)
