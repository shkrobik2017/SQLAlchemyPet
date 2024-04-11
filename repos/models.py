from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped
from datetime import datetime, timedelta, date

Base = declarative_base()

RETURN_PERIOD = date.today() + timedelta(days=30)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True)
    first_name: Mapped[str] = Column(String(50))
    last_name: Mapped[str] = Column(String(50))
    email: Mapped[str] = Column(String(50), nullable=True)


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = Column(Integer, primary_key=True)
    title: Mapped[str] = Column(String(50))
    author: Mapped[str] = Column(String(50))
    publication_year: Mapped[int] = Column(Integer, default=date.year)


class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[int] = Column(Integer, primary_key=True)
    book_id: Mapped[int] = Column(Integer, ForeignKey("books.id"))
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"))
    issue_date: Mapped[datetime.date] = Column(Date, default=date.today())
    return_period: Mapped[datetime.date] = Column(Date, default=(date.today() + timedelta(days=30)))

