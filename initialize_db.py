import duckdb

def setup_database():
    """Initializes high-performance optimized DuckDB schema."""
    con = duckdb.connect('mks_storage.duckdb')
    
    # 1. Metadata Table (Static info about the company)
    con.execute("""
        CREATE TABLE IF NOT EXISTS tickers (
            symbol TEXT PRIMARY KEY,
            name TEXT,
            sector TEXT,
            exchange TEXT
        )
    """)

    # 2. Performance Table (Optimized for math/filtering)
    # We use DOUBLE for ratings and math-heavy numbers
    con.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            symbol TEXT,
            rs_rating DOUBLE,
            volume_delta DOUBLE,
            FOREIGN KEY (symbol) REFERENCES tickers (symbol)
        )
    """)

    # 3. Create an INDEX for lightning-fast lookups by Symbol
    con.execute("CREATE INDEX IF NOT EXISTS idx_symbol ON signals (symbol)")
    
    print("[SUCCESS] Optimized Schema with Indexes applied.")
    con.close()

if __name__ == "__main__":
    setup_database()