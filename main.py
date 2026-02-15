import os
from dotenv import load_dotenv
import initialize_db  # Connecting the Data Layer
# import test_engine   # Connecting the Logic Layer (Keep commented until ready)

# Load the "Shield" (Secrets)
load_dotenv()

def bootstrap():
    """Ensure the system is ready to run."""
    print("--- MKS_V2 System Bootstrapping ---")
    
    # 1. Initialize the Database (The Memory)
    # This calls the function inside initialize_db.py
    initialize_db.setup_database()
    
    print("[SUCCESS] Environment, Secrets, and Database loaded.")

def run_engine():
    """Triggers the core logic of the system."""
    print("--- Starting Execution Engine ---")
    # This is where we will call your test_engine.run() logic soon
    pass

if __name__ == "__main__":
    bootstrap()
    run_engine()