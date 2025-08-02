"""
python tests/test_db_connection.py
"""

import sys
import os

# ✅ Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Import get_db from app.db.db
from app.db.db import get_db
from sqlalchemy import text

def test_db():
    db = next(get_db())
    try:
        db.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_db()
