from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

                    ###########          from config import DB_URL

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3',
                             echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    tg_id = mapped_column(BigInteger, primary_key=True)
    nickname = mapped_column(String)
    phone_number = mapped_column(BigInteger)

class Info(Base):
    __tablename__ = 'data'

    id = mapped_column(String, primary_key=True)
    txt_info = mapped_column(String)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)