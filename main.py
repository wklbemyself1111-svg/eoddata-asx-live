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
    """Diagnose EODData request problems."""
    if not EODDATA_API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")

    params = {
        "KEY": EODDATA_API_KEY,
        "EXCHANGE": "ASX",
        "SYMBOLS": ticker.upper()
    }

    url = "https://ws.eoddata.com/data.asmx/QuoteList"

    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(url, params=params)
        except Exception as e:
            # network-level error
            raise HTTPException(status_code=500, detail=f"Network error: {e}")

    return {
        "status_code": r.status_code,
        "headers": dict(r.headers),
        "text_snippet": r.text[:400]
    }
