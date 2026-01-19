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
EODDATA_BASE_URL = "https://api.eoddata.com/api/real-time/AU"

@app.get("/api/quote/{ticker}")
async def get_live_quote(ticker: str):
    """Fetch live quote data for an ASX ticker."""
    url = f"{EODDATA_BASE_URL}/{ticker.upper()}"
    headers = {"Authorization": EODDATA_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch from EODData")

    try:
        data = response.json()
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid JSON response from EODData")

    # Example data cleaning — adapt to match EODData’s actual JSON structure
    result = {
        "ticker": ticker.upper(),
        "name": data.get("Name", ""),
        "last_price": data.get("LastPrice", None),
        "change": data.get("Change", None),
        "change_percent": data.get("ChangePercent", None),
        "volume": data.get("Volume", None),
        "timestamp": data.get("Timestamp", None),
    }
    return JSONResponse(content=result)
