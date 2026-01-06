from fastapi import FastAPI

from app.adapters.inbound.api.handlers import router

app = FastAPI(title="Pyfinviz Screener API", version="1.0.0")

app.include_router(router)