import asyncio
import aiohttp
import polars as pl
import duckdb
import os

# CONFIGURATION
API_KEY = "IcXDTO4XhroLQpEcvV2ge0ja9I6HUTqsHERE"  # Replace with your actual key
DB_PATH = "market_data.duckdb"
BASE_URL = "https://financialmodelingprep.com/api/v3"

async def initialize_market_universe():
    print("🚀 Initializing Market Universe...")
    
    async with aiohttp.ClientSession() as session:
        # 1. Fetch the Master List from FMP
        url = f"{BASE_URL}/stock/list?apikey={API_KEY}"
        async with session.get(url) as response:
            if response.status != 200:
                print(f"❌ Error fetching data: {response.status}")
                return
            
            data = await response.json()
            
    # 2. Process with Polars (The Rust Engine)
    # We filter for major US exchanges only to keep the 1-99 ratings relevant
    df = pl.DataFrame(data)
    
    universe = df.filter(
        (pl.col("exchangeShortName").is_in(["NASDAQ", "NYSE", "AMEX"])) &
        (pl.col("type") == "stock")
    ).select([
        pl.col("symbol").alias("ticker"),
        pl.col("name"),
        pl.col("exchangeShortName").alias("exchange"),
        pl.col("price"),
        pl.col("type")
    ])

    print(f"✅ Filtered Universe: {len(universe)} high-quality tickers identified.")

    # 3. Save to DuckDB (The Storage Layer)
    con = duckdb.connect(DB_PATH)
    
    # Create the master table
    con.execute("CREATE OR REPLACE TABLE tickers AS SELECT * FROM universe")
    
    # Verify
    count = con.execute("SELECT count(*) FROM tickers").fetchone()[0]
    print(f"📂 Database initialized at {DB_PATH}")
    print(f"📊 Total Tickers Stored: {count}")
    con.close()

if __name__ == "__main__":
    asyncio.run(initialize_market_universe())
