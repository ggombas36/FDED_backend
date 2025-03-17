from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    message: str

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
