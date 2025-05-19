from fastapi import FastAPI
from backend.routes import auth, citas
from backend.routes import citas



app = FastAPI()

app.include_router(auth.router)
app.include_router(citas.router)
