"""
python tests/test_redis.py
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.redis_client import redis_client  # ✅ updated import

def test_redis_connection():
    try:
        redis_client.set("test_key", "Hello Redis!")
        value = redis_client.get("test_key")
        print(f"✅ Redis connection successful! Value = {value}")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")

if __name__ == "__main__":
    test_redis_connection()
