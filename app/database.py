"""
database.py — Sets up the connection between FastAPI and PostgreSQL.

KEY CONCEPTS:
- SQLAlchemy Engine: the "engine" is like a phone line to the database.
  It knows the address (DATABASE_URL) and manages the actual TCP connection pool.

- SessionLocal: a "session" is a temporary workspace for a single request.
  You open it, do your DB work (read/write), then close it.
  Think of it like opening a spreadsheet, editing it, then saving and closing.

- Base: the parent class for all our database models (tables).
  Any class that inherits from Base becomes a table in PostgreSQL.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load variables from the .env file into os.environ
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# create_engine() sets up the connection pool.
# pool_pre_ping=True means SQLAlchemy will test the connection before using it
# (prevents errors if the DB restarted while the app is running).
# psycopg v3 uses "postgresql+psycopg://" instead of "postgresql://"
# We auto-fix the URL here so both formats work
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal is a factory — calling SessionLocal() creates a new session object.
# autocommit=False → we manually commit transactions (safer, more control).
# autoflush=False  → changes aren't sent to DB until we explicitly flush/commit.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class all our ORM models will inherit from.
Base = declarative_base()


def get_db():
    """
    FastAPI Dependency — provides a DB session to any route that needs it.

    This is a Python generator (note the 'yield').
    FastAPI calls it before the route runs, injects the session,
    and then runs the cleanup (db.close()) after the response is sent.

    This pattern guarantees the session is ALWAYS closed, even if an
    exception is raised — similar to a 'with' statement.
    """
    db = SessionLocal()
    try:
        yield db          # hand the session to the route function
    finally:
        db.close()        # always runs, no matter what
