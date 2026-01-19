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

    params = {
        "KEY": EODDATA_API_KEY,
        "EXCHANGE": "ASX",
        "SYMBOLS": ticker.upper()
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(EODDATA_BASE_URL, params=params)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail="Failed to fetch data from EODData")

    try:
        data = r.json()
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid JSON response from EODData")

    return JSONResponse(content=data)
