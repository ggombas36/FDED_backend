from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    name: str
    phone: str
    address: str
    message: str = "Sikeres művelet"  # Default message field

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    phone: str
    address: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
