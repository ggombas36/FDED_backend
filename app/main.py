import os
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.routers import auth  # 🚀 FONTOS: Ha "routers" mappában van
from app.database import Base  # 🚀 FONTOS: "database.py"-ból importáljuk

# 1️⃣ Betöltjük a DATABASE_URL-t Railway-ről
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ ERROR: A DATABASE_URL változó nincs beállítva!")

# 2️⃣ Létrehozzuk az adatbázis kapcsolatot
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3️⃣ Létrehozzuk az adatbázis táblákat
Base.metadata.create_all(bind=engine)  # 🚀 Itt van a jó helyen!

# 4️⃣ Létrehozzuk a FastAPI appot
app = FastAPI()

# 5️⃣ Routerek hozzáadása
app.include_router(auth.router)
