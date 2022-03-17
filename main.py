from fastapi import FastAPI

from db.database import engine, Base
from routers.accounts import auth

Base.metadata.create_all(engine)

app = FastAPI()


app.include_router(auth.router)
