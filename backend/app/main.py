from fastapi import FastAPI, Path

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

# -----------------------------------
# ROUTES
# -----------------------------------

app.include_router(router)

# -----------------------------------
# STATIC FILES
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent

app.mount(
    "/",
    StaticFiles(directory=str(BASE_DIR / "frontend"), html=True),
    name="frontend"
 )