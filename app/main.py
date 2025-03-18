# from fastapi import FastAPI
# from app.routers import auth  # 🚀 FONTOS: ha a "routers" könyvtárban van
# from app.database import engine, Base

# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# app.include_router(auth.router)
# # port 5433

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")  # Railway-ről tölti be

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
