# app/models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Register(Base):
    __tablename__ = "register"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255))
    dob = Column(Date)
    gender = Column(String(50))
    country = Column(String(100))
    email = Column(String(255))
    phone = Column(String(20))

    login = relationship("Login", back_populates="register", uselist=False)


class Login(Base):
    __tablename__ = "login"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    register_id = Column(Integer, ForeignKey("register.id"), nullable=False)
    register = relationship("Register", back_populates="login")
