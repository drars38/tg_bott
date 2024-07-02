from app.database.models import async_session
from app.database.models import User, Info
from sqlalchemy import select, update, delete, desc


async def set_user(tg_id, nickname,phone_number):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id,
                                                       User.nickname == nickname,
                                                       User.phone_number == phone_number))

        if not user:
            session.add(User(tg_id=tg_id, nickname = nickname , phone_number = phone_number))
            await session.commit()


async def get_info(id):
    async with async_session() as session:
       result = await session.execute(select(Info.txt_info).where(Info.id == id))
       return result.scalar()



async def get_employee() -> list[User]:
    async with async_session() as session:
        result = await session.execute(select(User))
       # print(result.scalars().all())
        return result.scalars().all()
