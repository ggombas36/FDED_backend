from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import SessionLocal  # 🚀 ELLENŐRIZD, HOGY PONTOS AZ IMPORT!
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse
from app.exception import UserExistsError, EmailExistsError
from sqlalchemy.exc import IntegrityError
from app.auth.jwt import create_access_token
from datetime import timedelta

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

# @router.post("/login")
# def login(user_data: UserLogin, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == user_data.email).first()
#     if not user or user.password != user_data.password:
#         raise HTTPException(status_code=400, detail="Invalid credentials")

#     # Token generálása 4 órára
#     access_token_expires = timedelta(hours=4)
#     access_token = create_access_token(
#         data={"sub": user.email}, expires_delta=access_token_expires
#     )

#     return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    try:
        # Felhasználó keresése email alapján
        user = db.query(User).filter(User.email == user_data.email).first()
        
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Hibás email cím vagy jelszó"
            )
        
        # Jelszó ellenőrzése a hash-elt jelszóval
        if not pwd_context.verify(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Hibás email cím vagy jelszó"
            )
        
        # Token generálása 4 órára
        access_token_expires = timedelta(hours=4)
        access_token = create_access_token(
            data={
                "sub": user.email,
                "user_id": user.id,
                "username": user.username
            },
            expires_delta=access_token_expires
        )
        
        # Sikeres bejelentkezés válasz
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
        }
        
    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug log
        raise HTTPException(
            status_code=500,
            detail="Hiba történt a bejelentkezés során"
        )

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Felhasználó nem található"
            )
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "phone": user.phone,
            "address": user.address,
            # Ne adjuk vissza a jelszó hash-t biztonsági okokból
        }
    except Exception as e:
        print(f"Get user error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Hiba történt a felhasználó lekérése során"
        )
