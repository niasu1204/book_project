# 도서 ORM 모델
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from database.database import Base


class Book(Base):

    __tablename__ = "books"

    book_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    author = Column(
        String(100),
        nullable=False
    )

    publisher = Column(String(100))

    price = Column(Integer, default=0)

    category = Column(String(50))

    stock = Column(Integer, default=0)

    reg_date = Column(
        DateTime,
        server_default=func.now()
    )