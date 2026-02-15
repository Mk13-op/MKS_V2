import os
import asyncio
from dotenv import load_dotenv
import initialize_db
import test_engine 

load_dotenv(override=True)

async def bootstrap():
    print("--- MKS_V2 System Bootstrapping ---")
    initialize_db.setup_database()
    
    fmp_key = os.getenv("FMP_API_KEY") 
    if fmp_key:
        print("[SUCCESS] API Key detected and loaded.")
    else:
        print("[WARNING] API Key not found in .env!")
    
    print("[SUCCESS] Environment and Database ready.")

async def run_system():
    # The Live Watchlist
    watchlist = ["NVDA", "AAPL", "MSFT", "TSLA", "PLTR"]
    
    # 1. Fetch live data
    live_data = await test_engine.fetch_market_data(watchlist)
    
    # 2. Analyze live data
    test_engine.run_analysis(live_data)

if __name__ == "__main__":
    async def start():
        await bootstrap()
        await run_system()

    asyncio.run(start())