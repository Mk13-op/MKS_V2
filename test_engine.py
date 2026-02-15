import asyncio
import aiohttp
import os
import polars as pl
import duckdb

async def fetch_market_data(tickers: list):
    """Fetches live market data using Asynchronous Parallel Requests (Free-Tier Bypass)."""
    print(f"1. [Network] Launching parallel free-tier requests for: {tickers}...")
    
    api_key = os.getenv("FMP_API_KEY")
    if api_key:
        api_key = api_key.strip()
    else:
        print("[CRITICAL] FMP_API_KEY not found!")
        return None

    # We use the Free-Tier single quote endpoint
    base_url = "https://financialmodelingprep.com/stable/quote"
    
    # Define how to fetch a SINGLE stock
    async def fetch_single(session, ticker):
        url = f"{base_url}?symbol={ticker}&apikey={api_key}"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data[0] if data else None
            else:
                print(f"[WARNING] Failed to fetch {ticker}. Status: {response.status}")
                return None

    # Fire all requests simultaneously
    async with aiohttp.ClientSession() as session:
        # Create a "task" for every ticker in your watchlist
        tasks = [fetch_single(session, ticker) for ticker in tickers]
        
        # 'gather' runs them all at the exact same millisecond
        results = await asyncio.gather(*tasks)
        
        # Filter out any failed requests
        valid_data = [r for r in results if r]
        
        if valid_data:
            print(f"[SUCCESS] Live data secured for {len(valid_data)} stocks.")
            return valid_data
        else:
            print("[ERROR] Failed to retrieve data for any tickers.")
            return None