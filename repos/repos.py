from abc import ABC, abstractmethod

from sqlalchemy import inspect, select, text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import selectinload

from .models import User, Base, Book, Issue
from .database import async_session, async_engine


class BaseRepository(ABC):
    session: AsyncSession = async_session()
    engine: AsyncEngine = async_engine

    @abstractmethod
    async def read_object(self, **kwargs):
        """ Read objects """

    @abstractmethod
    async def insert_object(self, obj: Base):
        """ Insert objects """

    @abstractmethod
    async def delete_object(self, **kwargs):
        """ Delete objects """

    async def _create_table(self):
        async with self.session as conn:
            await conn.run_sync(Base.metadata.create_all())

    async def _has_table(self, model):
        async with self.engine.connect() as conn:
            tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
            if model.__tablename__ not in tables:
                await self._create_table()

    async def _commit(self, obj: Base):
        async with self.session as session:
            session.add(obj)
            await session.commit()


class BookRepository(BaseRepository):
    model: Book = Book

    async def update_object(self, *, book_title: str, book_author: str, book_publication_year: int, **kwargs):
        obj = await self.read_object(
            title=book_title,
            author=book_author,
            publication_year=book_publication_year
        )
        for item in obj:
            for attribute, value in kwargs.items():
                setattr(item, attribute, value)

            await self._commit(item)

    async def read_object(self, **kwargs):
        """ In this model you can get the object only by follow variables:
         - id: User id in table (primary key)
         - first_name: User's first name
         - last_name: User's last name
         - email: User's email """
        async with self.session as session:
            query = select(self.model).options(selectinload(self.model.issues))
            for attribute, value in kwargs.items():
                get_attr = getattr(self.model, attribute)
                query = query.filter(get_attr == value)
            obj = await session.execute(query)

            return obj.scalars().all()

    async def insert_object(self, obj: Base):
        await self._has_table(self.model)
        await self._commit(obj)

    async def delete_object(self, **kwargs):
        obj = await self.read_object(**kwargs)

        for item in obj:
            async with self.session as session:
                await session.delete(item)
                await session.commit()


class UserRepository(BaseRepository):
    model: User = User

    async def update_object(self, *, user_first_name: str, user_last_name: str, user_email: str, **kwargs):
        obj = await self.read_object(
            first_name=user_first_name,
            last_name=user_last_name,
            email=user_email
        )
        for item in obj:
            for attribute, value in kwargs.items():
                setattr(item, attribute, value)

            await self._commit(item)

    async def read_object(self, **kwargs):
        """ In this model you can get the object only by follow variables:
        - id: Book id in table (primary key)
        - title: Book title
        - author: Book author
        - publication_year: Year of publication of book """
        async with self.session as session:
            query = select(self.model).options(selectinload(self.model.issues))
            for attribute, value in kwargs.items():
                get_attr = getattr(self.model, attribute)
                query = query.filter(get_attr == value)
            obj = await session.execute(query)

            return obj.scalars().all()

    async def insert_object(self, obj: Base):
        await self._has_table(self.model)
        await self._commit(obj)

    async def delete_object(self, **kwargs):
        obj = await self.read_object(**kwargs)

        for item in obj:
            async with self.session as session:
                await session.delete(item)
                await session.commit()


class IssueRepository(BaseRepository):
    model: Issue = Issue

    async def read_object(self, **kwargs):
        """ In this model you can get the object only by follow variables:
        - id: Issue id in table (primary key)
        - book_id: Book id (foreign key of books table)
        - user_id: User id (foreign key of users table)
        - issue_date: Date of issue (format: datetime.date.today())
        - return_period: Date when book must be returned (format: issue_date + 30 days)"""
        async with self.session as session:
            query = select(self.model).options(selectinload(self.model.book)).options(selectinload(self.model.user))
            for attribute, value in kwargs.items():
                get_attr = getattr(self.model, attribute)
                query = query.filter(get_attr == value)
            obj = await session.execute(query)

            return obj.scalars().all()

    async def insert_object(self, obj: Base):
        await self._has_table(self.model)
        await self._commit(obj)

    async def delete_object(self, **kwargs):
        obj = await self.read_object(**kwargs)

        for item in obj:
            async with self.session as session:
                await session.delete(item)
                await session.commit()
