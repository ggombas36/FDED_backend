from fastapi import FastAPI
from app.routers import auth  # 🚀 FONTOS: ha a "routers" könyvtárban van
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
# port 5433