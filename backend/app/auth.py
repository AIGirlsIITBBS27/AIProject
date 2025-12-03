# app/auth.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.database import SessionLocal
from app.models import Register, Login
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class SignupIn(BaseModel):
    name: str
    dob: str          # expect 'YYYY-MM-DD' from frontend (ISO date)
    gender: str | None = None
    country: str | None = None
    email: EmailStr
    phone: str | None = None
    username: str
    password: str


@router.post("/signup")
def signup(data: SignupIn, db: Session = Depends(get_db)):
    
    existing = db.query(Login).filter(Login.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

  
    dob_date = None
    if data.dob:
        try:
            dob_date = datetime.strptime(data.dob, "%Y-%m-%d").date()
        except Exception:
            raise HTTPException(status_code=400, detail="dob must be YYYY-MM-DD")

    reg = Register(
        name=data.name,
        dob=dob_date,
        gender=data.gender,
        country=data.country,
        email=str(data.email),
        phone=data.phone,
    )
    db.add(reg)
    db.commit()
    db.refresh(reg)


    login_row = Login(
        username=data.username,
        password=data.password, 
        register_id=reg.id,
    )
    db.add(login_row)
    db.commit()
    db.refresh(login_row)

    return {
        "msg": "User registered successfully",
        "register_id": reg.id,
        "username": login_row.username,
    }


class LoginIn(BaseModel):
    username: str
    password: str
    

@router.post("/login")
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(Login).filter(Login.username == data.username).first()
    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    reg = db.query(Register).filter(Register.id == user.register_id).first()
    profile = {
        "id": reg.id,
        "name": reg.name,
        "dob": reg.dob.isoformat() if reg and reg.dob else None,
        "gender": reg.gender,
        "country": reg.country,
        "email": reg.email,
        "phone": reg.phone,
    } if reg else None

    return {
        "msg": "Login successful",
        "username": user.username,
        "register_id": user.register_id,
        "profile": profile,
    }
    
class ForgotPasswordIn(BaseModel):
        name: str
        dob: str   


@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordIn, db: Session = Depends(get_db)):
   
    user = (
        db.query(Register)
        .filter(Register.name == data.name)
        .filter(Register.dob == data.dob)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="No user found with given details")

   
    login = db.query(Login).filter(Login.register_id == user.id).first()

    if not login:
        raise HTTPException(status_code=404, detail="Login details not found")

    return {
        "msg": "User found",
        "username": login.username,
        "password": login.password,   
    }

