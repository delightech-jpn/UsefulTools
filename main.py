from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx

app = FastAPI()

GAS_ENDPOINT = "https://script.google.com/macros/s/AKfycbxEMoykB7CFuKLL-BTbqj3bUJX2iTkSj_fAg7jLbvkkijzpMCZK0K97y-I2GsbKFEg/exec"

class Query(BaseModel):
    query: str
    mode: str  # 'ai' or 'history'

@app.post("/search")
async def search(query: Query):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(GAS_ENDPOINT, json=query.dict())
            return response.json()
    except Exception as e:
        return {"error": f"FastAPI error: {str(e)}"}
