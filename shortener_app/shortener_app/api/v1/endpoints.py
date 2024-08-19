from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from shortener_app.schemas.schemas import URLBase_Schema, URLInfo_Schema
from shortener_app.services.url_service import create_url_service, forward_to_target_url_service
from shortener_app.utils.dependencies import get_db

router = APIRouter()


@router.get("/health",response_class=RedirectResponse, include_in_schema=False)
def health_check():
    return RedirectResponse("/docs")


@router.post("/url", response_model=URLInfo_Schema)
def create_url(url: URLBase_Schema, db: Session = Depends(get_db)):
    return create_url_service(url, db)


@router.get("/{url_key}", response_model=URLInfo_Schema)
def forward_to_target_url(url_key: str, db: Session = Depends(get_db)):
    return forward_to_target_url_service(url_key, db)