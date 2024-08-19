from fastapi import FastAPI
from shortener_app.api.v1.endpoints import router as api_router

app = FastAPI()

app.include_router(api_router)
