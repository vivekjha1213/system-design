import secrets
import string
from sqlalchemy.orm import Session
from . import crud

def create_random_key(length: int = 8) -> str:
    """Generates a random string key of specified length."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def create_unique_random_key(db: Session) -> str:
    """Generates a unique random key that does not exist in the database.

    Args:
        db (Session): The database session.

    Returns:
        str: A unique random key.
    """
    key = create_random_key()
    while crud.get_db_url_by_key(db, key):
        key = create_random_key()
    return key
