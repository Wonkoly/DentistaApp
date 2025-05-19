from fastapi import FastAPI
from backend.routes import auth

app = FastAPI()

app.include_router(auth.router)

