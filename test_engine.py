import polars as pl
import duckdb
import aiohttp
import asyncio

async def test_network():
    # Verify the async network library is available
    print("1. [Network] aiohttp installed and ready for async FMP fetching.")

def test_data_handoff():
    # Create a fast Polars DataFrame (Rust engine)
    print("2. [Polars] Generating test dataframe...")
    df = pl.DataFrame({
        "Ticker": ["NVDA", "AAPL", "MSFT"],
        "RS_Rating": [99, 85, 92]
    })
    
    # Hand the data over to DuckDB (C++ engine) and query it via SQL
    print("3. [DuckDB] Executing SQL on Polars memory...")
    result = duckdb.sql("SELECT Ticker FROM df WHERE RS_Rating > 90").pl()
    
    print("\n--- TEST COMPLETE: ENGINE OPERATIONAL ---")
    print("Top Stocks Identified:\n", result)

async def main():
    print("INITIALIZING SNAPDRAGON X ELITE DIAGNOSTIC...\n")
    await test_network()
    test_data_handoff()

if __name__ == "__main__":
    asyncio.run(main())
    