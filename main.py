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
EODDATA_BASE_URL = "https://ws.eoddata.com/data.asmx/QuoteList"

@app.get("/api/quote/{ticker}")
async def get_live_quote(ticker: str):
    """Fetch live quote data for an ASX ticker using EODData."""
    if not EODDATA_API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")

    # Correct parameters for EODData .asmx service
    params = {
        "Token": EODDATA_API_KEY,
        "Exchange": "ASX",
        "Symbols": ticker.upper()
    }

    url = "https://ws.eoddata.com/data.asmx/QuoteList"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"EODData returned status {r.status_code}")

    return {
        "status_code": r.status_code,
        "text_snippet": r.text[:400]
    }
