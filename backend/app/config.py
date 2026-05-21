from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"

OUTPUT_DIR = BASE_DIR / "outputs"

PLOTS_DIR = OUTPUT_DIR / "plots"

EXCEL_DIR = OUTPUT_DIR / "excel"

for folder in [
    UPLOAD_DIR,
    OUTPUT_DIR,
    PLOTS_DIR,
    EXCEL_DIR
]:
    folder.mkdir(parents=True, exist_ok=True)