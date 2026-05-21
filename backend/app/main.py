from fastapi import FastAPI

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

app.mount(

    "/outputs",

    StaticFiles(directory="outputs"),

    name="outputs"
)