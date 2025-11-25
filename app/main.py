# app/main.py
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.database import SessionLocal, engine, Base
from app.crud import create_user, get_users

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


async def get_db():
    async with SessionLocal() as session:
        yield session


@app.on_event("startup")
async def init_db():
    # สร้างตารางจาก models ทั้งหมด (เช่น User) ตอน start container
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/", response_class=HTMLResponse)
async def webpage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/healthz")
async def healthcheck(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"database error: {e}")


@app.post("/users")
async def api_create_user(name: str, db: AsyncSession = Depends(get_db)):
    return await create_user(db, name)


@app.get("/users")
async def api_get_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)
