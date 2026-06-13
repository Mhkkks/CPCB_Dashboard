from fastapi import FastAPI
from pathlib import Path

from fastapi.middleware.cors import (
    CORSMiddleware
)

from fastapi.staticfiles import (
    StaticFiles
)

from app.api.routes import router

app = FastAPI()

# -----------------------------------
# CORS
# -----------------------------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

app.include_router(router)

from app.config import OUTPUT_DIR

app.mount(
    "/outputs",
    StaticFiles(directory=str(OUTPUT_DIR)),
    name="outputs"
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

app.mount(
    "/",
    StaticFiles(
        directory=str(BASE_DIR / "frontend"),
        html=True
    ),
    name="frontend"
)