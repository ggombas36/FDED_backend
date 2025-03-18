from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import SessionLocal  # 🚀 ELLENŐRIZD, HOGY PONTOS AZ IMPORT!
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse
from app.exception import UserExistsError, EmailExistsError
from sqlalchemy.exc import IntegrityError

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user_data.username).first()
    if db_user:
        raise UserExistsError(detail="A felhasználónév már foglalt!")
    
    # Ellenőrizzük, hogy létezik-e már az email
    db_email = db.query(User).filter(User.email == user_data.email).first()
    if db_email:
        raise EmailExistsError(detail="Ez az email cím már regisztrálva van!")

    hashed_password = pwd_context.hash(user_data.password)
    user = User(
        name=user_data.name,
        username=user_data.username,
        email=user_data.email,
        phone=user_data.phone,
        address=user_data.address,
        hashed_password=hashed_password
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Váratlan hiba történt a regisztráció során")

@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not pwd_context.verify(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    return {"message": "Login successful", "user_id": user.id}

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
