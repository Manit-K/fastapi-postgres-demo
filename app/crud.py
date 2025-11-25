from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User

async def create_user(db: AsyncSession, name: str):
    new_user = User(name=name)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()
