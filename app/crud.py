"""
crud.py — All database read/write operations live here.

KEY CONCEPTS:
- CRUD: Create, Read, Update, Delete — the four basic database operations.
  Every app you ever build will have some form of these.

- Why separate crud.py from main.py?
  Separation of concerns. Routes (main.py) handle HTTP logic.
  CRUD functions handle database logic. This makes the code:
    1. Easier to test (you can test DB logic without starting the server)
    2. Easier to reuse (multiple routes can call the same CRUD function)
    3. Easier to read (each file has one clear job)

- db.add()    → stages the new object (like git add)
- db.commit() → writes it to PostgreSQL (like git commit)
- db.refresh()→ re-reads the row from DB so we get server-set values
                like 'id' and 'created_at' that PostgreSQL filled in
"""

from sqlalchemy.orm import Session
from app import models
from app.utils import generate_short_code


def get_url_by_code(db: Session, short_code: str) -> models.URL | None:
    """
    Looks up a URL row by its short_code.
    Returns the URL object if found, or None if it doesn't exist.

    This is the function called on EVERY redirect — it must be fast.
    The index on short_code (defined in models.py) makes this O(log n).
    """
    return db.query(models.URL).filter(models.URL.short_code == short_code).first()


def get_url_by_long_url(db: Session, long_url: str) -> models.URL | None:
    """
    Checks if this long URL has already been shortened before.
    If it has, we return the existing entry instead of creating a duplicate.

    This is called "idempotency" — doing the same thing twice gives the
    same result, not two different entries.
    """
    return db.query(models.URL).filter(models.URL.long_url == long_url).first()


def create_short_url(db: Session, long_url: str) -> models.URL:
    """
    Creates a new short URL entry in the database.

    COLLISION HANDLING:
    We generate a short code, then check if it already exists.
    If it does (extremely rare), we generate a new one and try again.
    The while loop keeps retrying until we find a unique code.

    In practice with 56 billion possibilities, you'll almost never
    loop more than once — but we handle it correctly anyway.
    """
    # Step 1: check if this long URL was already shortened
    existing = get_url_by_long_url(db, long_url)
    if existing:
        return existing  # return the existing record, don't create a duplicate

    # Step 2: generate a unique short code (retry on collision)
    while True:
        short_code = generate_short_code()
        if not get_url_by_code(db, short_code):
            break  # this code doesn't exist yet → we can use it

    # Step 3: create the SQLAlchemy model instance (not saved yet)
    db_url = models.URL(
        short_code=short_code,
        long_url=long_url
    )

    # Step 4: save to database
    db.add(db_url)      # stage the new row
    db.commit()         # write to PostgreSQL
    db.refresh(db_url)  # reload from DB to get server-generated id + created_at

    return db_url
