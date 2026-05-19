"""
models.py — Defines the shape of our database table using SQLAlchemy ORM.

KEY CONCEPTS:
- ORM (Object Relational Mapper): lets you work with database rows as Python
  objects instead of writing raw SQL. SQLAlchemy is Python's most popular ORM.

- Each class = one table in PostgreSQL.
- Each class attribute with Column() = one column in that table.

Our table looks like this in SQL (SQLAlchemy creates this for us automatically):

    CREATE TABLE urls (
        id          SERIAL PRIMARY KEY,
        short_code  VARCHAR(10) UNIQUE NOT NULL,
        long_url    TEXT NOT NULL,
        created_at  TIMESTAMP DEFAULT now()
    );
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class URL(Base):
    """
    Represents the 'urls' table in PostgreSQL.

    __tablename__ tells SQLAlchemy what to name the table in the DB.
    """
    __tablename__ = "urls"

    id = Column(
        Integer,
        primary_key=True,   # unique identifier for every row, auto-increments
        index=True           # creates a DB index → faster lookups by id
    )

    short_code = Column(
        String(10),
        unique=True,         # no two rows can have the same short_code
        nullable=False,      # this column must always have a value
        index=True           # indexed → very fast lookup when redirecting
    )

    long_url = Column(
        Text,                # TEXT stores strings of unlimited length
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()  # PostgreSQL sets this automatically on insert
    )
