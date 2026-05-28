import pandas as pd

from pathlib import Path


# =====================================================
# FILE LOADER
# =====================================================

def load_csv(file_path):

    file_path = str(file_path)

    extension = (
        Path(file_path)
        .suffix
        .lower()
    )

    # =================================================
    # EXCEL FILES
    # =================================================

    if extension in [".xlsx", ".xls"]:

        try:

            df = pd.read_excel(
                file_path
            )

            df.columns = [

                str(col).strip()

                for col in df.columns
            ]

            print(
                "Loaded Excel file successfully"
            )

            return df

        except Exception as e:

            raise ValueError(
                f"Excel loading failed: {e}"
            )

    # =================================================
    # CSV FILES
    # =================================================

    encodings = [

        "utf-8",

        "utf-16",

        "latin1",

        "cp1252"
    ]

    separators = [

        ",",

        ";",

        "\t"
    ]

    last_error = None

    for encoding in encodings:

        for sep in separators:

            try:

                df = pd.read_csv(

                    file_path,

                    encoding=encoding,

                    sep=sep,

                    engine="python",

                    on_bad_lines="skip",

                    na_values=[
                        "NA",
                        "--",
                        "null",
                        "None"
                    ]
                )

                # Reject broken parses

                if len(df.columns) <= 1:
                    continue

                df.columns = [

                    str(col).strip()

                    for col in df.columns
                ]

                print(

                    f"Loaded CSV successfully | "
                    f"encoding={encoding} | "
                    f"separator='{sep}'"
                )

                return df

            except Exception as e:

                last_error = e

                continue

    raise ValueError(

        f"Could not load file.\n"
        f"Last error: {last_error}"
    )


# =====================================================
# SAFE COLUMN DETECTION
# =====================================================

def detect_column(
    columns,
    possible_names
):

    normalized_columns = {

        str(col).lower().strip(): col

        for col in columns
    }

    # =================================================
    # EXACT MATCH FIRST
    # =================================================

    for possible in possible_names:

        possible_clean = (
            possible
            .lower()
            .strip()
        )

        for normalized, original in normalized_columns.items():

            if normalized == possible_clean:

                return original

    # =================================================
    # SAFE PARTIAL MATCH
    # =================================================

    for possible in possible_names:

        possible_clean = (
            possible
            .lower()
            .strip()
        )

        for normalized, original in normalized_columns.items():

            normalized_safe = (
                normalized
                .replace(" ", "")
            )

            # Prevent:
            # Temp -> Timestamp

            if (
                possible_clean in normalized_safe
                and
                "timestamp" not in normalized_safe
            ):

                return original

    return None


# =====================================================
# DETECT REQUIRED CPCB COLUMNS
# =====================================================

def detect_required_columns(df):

    columns = df.columns

    detected = {

        "date": detect_column(

            columns,

            [
                "Timestamp",
                "From Date",
                "Date"
            ]
        ),

        "pm25": detect_column(

            columns,

            [
                "PM2.5",
                "PM25"
            ]
        ),

        "temperature": detect_column(

            columns,

            [
                
                "Temperature",
                "Temp",
                "AT"
            ]
        ),

        "humidity": detect_column(

            columns,

            [
                "RH",
                "Humidity"
            ]
        )
    }

    return detected


# =====================================================
# FULL DATASET PREPROCESSING
# =====================================================

def preprocess_dataset(file_path):

    df = load_csv(file_path)

    detected = detect_required_columns(df)

    print("\n========== DETECTED COLUMNS ==========\n")

    print(detected)

    print("\n======================================\n")

    date_column = detected["date"]

    pm25_column = detected["pm25"]

    temperature_column = detected["temperature"]

    humidity_column = detected["humidity"]

    if not date_column:

        raise ValueError(
            "Date column not found"
        )

    # =================================================
    # STANDARDIZE COLUMN NAMES
    # =================================================

    rename_map = {}

    if date_column:

        rename_map[
            date_column
        ] = "From Date"

    if pm25_column:

        rename_map[
            pm25_column
        ] = "PM2.5"

    if temperature_column:

        rename_map[
            temperature_column
        ] = "Temperature"

    if humidity_column:

        rename_map[
            humidity_column
        ] = "RH"

    df = df.rename(
        columns=rename_map
    )

    # =================================================
    # DATETIME CONVERSION
    # =================================================

    df["From Date"] = pd.to_datetime(

        df["From Date"],

        errors='coerce'
    )

    # =================================================
    # NUMERIC CONVERSION
    # =================================================

    numeric_columns = [

        "PM2.5",

        "Temperature",

        "RH"
    ]

    for col in numeric_columns:

        if col in df.columns:

            df.loc[:, col] = pd.to_numeric(

                df[col],

                errors='coerce'
            )

    # =================================================
    # REMOVE INVALID DATES
    # =================================================

    df = df.dropna(
        subset=["From Date"]
    )

    # =================================================
    # DEBUG OUTPUT
    # =================================================

    print("\n========== CLEANED DATA SAMPLE ==========\n")

    print(df.head())

    print("\n=========================================\n")

    return df, detected


# =====================================================
# LIGHTWEIGHT PREPROCESSING
# =====================================================

def preprocess_dataframe(
    df,
    date_column,
    value_column
):

    df = df.copy()

    # =================================================
    # DATETIME
    # =================================================

    df[date_column] = pd.to_datetime(

        df[date_column],

        errors='coerce'
    )

    # =================================================
    # NUMERIC
    # =================================================

    df.loc[:, value_column] = pd.to_numeric(

        df[value_column],

        errors='coerce'
    )

    # =================================================
    # DROP INVALIDS
    # =================================================

    df = df.dropna(

        subset=[
            date_column,
            value_column
        ]
    )

    return df