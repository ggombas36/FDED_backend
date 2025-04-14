from fastapi import FastAPI
from app.api.endpoints import auth
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FDED Backend")

app.include_router(auth.router, prefix="/api", tags=["auth"])