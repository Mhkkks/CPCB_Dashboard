import pandas as pd

import pandas as pd


def load_csv(file_path):

    df = pd.read_csv(
        file_path,
        na_values=["NA", "--", "null"]
    )

    df.columns = [
        col.strip()
        for col in df.columns
    ]

    return df



def detect_column(columns, possible_names):

    for col in columns:

        for possible in possible_names:

            if possible.lower() in col.lower():
                return col

    return None


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

        # PRIMARY TEMPERATURE
        "temperature": detect_column(
            columns,
            [
                "AT",
                "Temp",
                "Temperature"
            ]
        ),

        # FALLBACK TEMP
        "temp_fallback": detect_column(
            columns,
            [
                "Temp",
                "Temperature"
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


def preprocess_dataset(file_path):

    df = load_csv(file_path)

    detected = detect_required_columns(df)

    date_column = detected["date"]

    if not date_column:
        raise ValueError("Date column not found")

    df[date_column] = pd.to_datetime(
        df[date_column],
        errors='coerce'
    )

    df = df.dropna(subset=[date_column])

    return df, detected

def preprocess_dataframe(
    df,
    date_column,
    value_column
):

    df[date_column] = pd.to_datetime(
        df[date_column],
        errors='coerce'
    )

    df = df.dropna(
        subset=[date_column]
    )

    df[value_column] = pd.to_numeric(
        df[value_column],
        errors='coerce'
    )

    df = df.dropna(
        subset=[value_column]
    )

    return df