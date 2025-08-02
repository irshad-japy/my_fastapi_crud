
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db.db import get_db

app = FastAPI()

@app.get("/ping-db")
def ping_database(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"message": "Database connection successful ✅"}
    except Exception as e:
        return {"error": str(e)}

