from fastapi import (
    APIRouter,
    UploadFile,
    File
)

import shutil

from app.config import UPLOAD_DIR

from app.services.analysis_service import (
    run_full_analysis
)

router = APIRouter()


@router.post("/run-analysis")
async def run_analysis(

    place1_2018: UploadFile = File(...),

    place1_2023: UploadFile = File(...),

    place2_2018: UploadFile = File(...),

    place2_2023: UploadFile = File(...)

):

    # ----------------------------------------
    # SAVE FILES
    # ----------------------------------------

    files = {

        "place1_2018": place1_2018,

        "place1_2023": place1_2023,

        "place2_2018": place2_2018,

        "place2_2023": place2_2023
    }

    saved_paths = {}

    for key, file in files.items():

        path = UPLOAD_DIR / file.filename

        with open(path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        saved_paths[key] = path

    # ----------------------------------------
    # RUN ANALYSIS
    # ----------------------------------------

    place1_results = run_full_analysis(

        pm_2018_path=saved_paths["place1_2018"],

        pm_2023_path=saved_paths["place1_2023"],

        climate_2018_path=saved_paths["place1_2018"],

        climate_2023_path=saved_paths["place1_2023"],

        location="Place_1"
    )

    place2_results = run_full_analysis(

        pm_2018_path=saved_paths["place2_2018"],

        pm_2023_path=saved_paths["place2_2023"],

        climate_2018_path=saved_paths["place2_2018"],

        climate_2023_path=saved_paths["place2_2023"],

        location="Place_2"
    )

    return {

        "message": "Research analysis completed successfully",

        "place1_results": place1_results,

        "place2_results": place2_results
    }