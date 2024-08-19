from pydantic import BaseModel


class URLBase_Schema(BaseModel):
    target_url: str


class URL_Schema(URLBase_Schema):
    is_active: bool
    clicks: int

    class Config:
        orm_mode = True


class URLInfo_Schema(URL_Schema):
    url: str
    admin_url: str
