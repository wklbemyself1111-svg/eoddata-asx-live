from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI(
    title="EODData ASX Live API",
    description="Proxy service fetching live ASX stock data from EODData.",
    version="1.0.0",
)

# Store your API key here or in an environment variable
EODDATA_API_KEY = os.getenv("EODDATA_API_KEY", "ftmeSPWEKbrFQzbJAmRryxAk")
EODDATA_BASE_URL = "https://restapi.eoddata.com/api/real-time"

@app.get("/api/quote/{ticker}")
async def get_live_quote(ticker: str):
    if not EODDATA_API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")

    url = f"{EODDATA_BASE_URL}/ASX/{ticker.upper()}?token={EODDATA_API_KEY}"

    async with httpx.AsyncClient() as client:
        r = await client.get(url)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"EODData returned {r.status_code}")

    try:
        data = r.json()
    except Exception:
        raise HTTPException(status_code=500, detail=f"Invalid response: {r.text[:200]}")

    return data
