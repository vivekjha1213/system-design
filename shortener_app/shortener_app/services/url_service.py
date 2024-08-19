from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
import secrets
import validators
from datetime import datetime

from shortener_app.models.models import URL
from shortener_app.schemas.schemas import URLBase_Schema, URLInfo_Schema


def create_url_service(url: URLBase_Schema, db: Session) -> URLInfo_Schema:
    """Service to create a new URL entry in the database."""
    if not validators.url(url.target_url):
        raise HTTPException(
            status_code=400, detail="Your provided URL is not valid")

    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    
    db_url = URL(
        target_url=url.target_url,
        key=key,
        secret_key=secret_key,
        created_at=datetime.now(),
        updated_at=datetime.now() 
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url, URLInfo_Schema(
        url=f"http://127.0.0.1:8000/{db_url.key}",  
        admin_url=f"http://127.0.0.1:8000/admin/{db_url.secret_key}",   
        secret_key=db_url.secret_key,
        target_url=db_url.target_url,
        is_active=db_url.is_active,
        clicks=db_url.clicks,
        created_at=db_url.created_at,
        updated_at=db_url.updated_at,
    )


def forward_to_target_url_service(url_key: str, db: Session):
    """Service to forward request to the target URL based on the URL key."""
    db_url = db.query(URL).filter(
        URL.key == url_key, URL.is_active == True).first()
    if db_url:
        return RedirectResponse(db_url.target_url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")
