from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionLocal, engine, Base
from app.crud import create_user, get_users

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


async def get_db():
    async with SessionLocal() as session:
        yield session


@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/", response_class=HTMLResponse)
async def webpage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/users")
async def api_create_user(name: str, db: AsyncSession = Depends(get_db)):
    return await create_user(db, name)


@app.get("/users")
async def api_get_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)
