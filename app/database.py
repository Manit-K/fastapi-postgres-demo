# app/database.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Please configure it in .env or Cloud Run env vars.")

# ถ้าอยากปิด log จาก SQLAlchemy ใน production ให้ตั้ง SQL_ECHO=false (ค่า default = false)
SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() == "true"

engine = create_async_engine(DATABASE_URL, echo=SQL_ECHO)

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
