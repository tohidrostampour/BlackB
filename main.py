from fastapi import FastAPI

from db.database import engine
from db.base import Base
from routers.base import api_router
Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(api_router)