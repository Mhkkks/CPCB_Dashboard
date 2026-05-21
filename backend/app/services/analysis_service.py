import pandas as pd
from app.preprocessing.data_processor import (
    load_csv,
    preprocess_dataframe,
    detect_required_columns
)

from app.heat_index.heat_index_calculator import (
    compute_heat_index
)

from app.visualization.pm25_histograms import (
    generate_pm25_histograms
)

from app.visualization.hi_histograms import (
    generate_hi_histograms
)

from app.visualization.double_diurnal_curves import (
    generate_double_diurnal_curves
)

from app.visualization.correlation_analysis import (
    generate_correlation_analysis
)


def compute_hi_column(
    df,
    temp_column,
    rh_column,
    fallback_temp_column=None
):

    # -----------------------------------
    # CREATE WORKING TEMP COLUMN
    # -----------------------------------

    df["TEMP_USED"] = pd.to_numeric(
        df[temp_column],
        errors='coerce'
    )

    # -----------------------------------
    # USE FALLBACK TEMP IF MAIN TEMP EMPTY
    # -----------------------------------

    if fallback_temp_column:

        fallback_temp = pd.to_numeric(
            df[fallback_temp_column],
            errors='coerce'
        )

        df["TEMP_USED"] = (
            df["TEMP_USED"]
            .fillna(fallback_temp)
        )

    # -----------------------------------
    # CLEAN RH
    # -----------------------------------

    df[rh_column] = pd.to_numeric(
        df[rh_column],
        errors='coerce'
    )

    # -----------------------------------
    # COMPUTE HI
    # -----------------------------------

    hi_values = []

    for _, row in df.iterrows():

        temp = row["TEMP_USED"]

        rh = row[rh_column]

        if pd.isna(temp) or pd.isna(rh):

            hi_values.append(None)

            continue

        try:

            hi = compute_heat_index(
                temp,
                rh
            )

            hi_values.append(hi)

        except Exception:

            hi_values.append(None)

    df["HI"] = hi_values

    df["HI"] = pd.to_numeric(
        df["HI"],
        errors='coerce'
    )

    return df


def run_full_analysis(

    pm_2018_path,
    pm_2023_path,

    climate_2018_path,
    climate_2023_path,

    location="Research_Location"

):

    # ----------------------------------------
    # LOAD FILES
    # ----------------------------------------

    pm_2018 = load_csv(pm_2018_path)

    pm_2023 = load_csv(pm_2023_path)

    climate_2018 = load_csv(climate_2018_path)

    climate_2023 = load_csv(climate_2023_path)

    # ----------------------------------------
    # DETECT COLUMNS
    # ----------------------------------------

    detected_pm_2018 = detect_required_columns(
        pm_2018
    )

    detected_pm_2023 = detect_required_columns(
        pm_2023
    )

    detected_climate_2018 = detect_required_columns(
        climate_2018
    )

    detected_climate_2023 = detect_required_columns(
        climate_2023
    )

    # ----------------------------------------
    # EXTRACT DETECTED COLUMNS
    # ----------------------------------------

    date_column_2018 = (
        detected_pm_2018["date"]
    )

    date_column_2023 = (
        detected_pm_2023["date"]
    )

    pm_column_2018 = (
        detected_pm_2018["pm25"]
    )

    pm_column_2023 = (
        detected_pm_2023["pm25"]
    )

    temp_column_2018 = (
        detected_climate_2018["temperature"]
    )

    temp_column_2023 = (
        detected_climate_2023["temperature"]
    )

    rh_column_2018 = (
        detected_climate_2018["humidity"]
    )

    rh_column_2023 = (
        detected_climate_2023["humidity"]
    )

    # ----------------------------------------
    # VALIDATION
    # ----------------------------------------

    required_columns = [
        date_column_2018,
        date_column_2023,
        pm_column_2018,
        pm_column_2023,
        temp_column_2018,
        temp_column_2023,
        rh_column_2018,
        rh_column_2023
    ]

    if any(col is None for col in required_columns):

        raise ValueError(
            "Required CPCB columns not detected"
        )

    # ----------------------------------------
    # PREPROCESS PM FILES
    # ----------------------------------------

    pm_2018 = preprocess_dataframe(
        pm_2018,
        date_column_2018,
        pm_column_2018
    )

    pm_2023 = preprocess_dataframe(
        pm_2023,
        date_column_2023,
        pm_column_2023
    )

    # ----------------------------------------
    # PREPROCESS CLIMATE FILES
    # ----------------------------------------

    climate_2018 = preprocess_dataframe(
        climate_2018,
        date_column_2018,
        temp_column_2018
    )

    climate_2023 = preprocess_dataframe(
        climate_2023,
        date_column_2023,
        temp_column_2023
    )

    # ----------------------------------------
    # CLEAN RH
    # ----------------------------------------

    climate_2018[rh_column_2018] = (
        climate_2018[rh_column_2018]
        .astype(float)
    )

    climate_2023[rh_column_2023] = (
        climate_2023[rh_column_2023]
        .astype(float)
    )

    # ----------------------------------------
    # COMPUTE HI
    # ----------------------------------------

    fallback_temp_2018 = (
    detected_climate_2018["temp_fallback"]
)

    hi_2018 = compute_hi_column(
    climate_2018,
    temp_column_2018,
    rh_column_2018,
    fallback_temp_2018
)

    fallback_temp_2023 = (
    detected_climate_2023["temp_fallback"]
)

    hi_2023 = compute_hi_column(
    climate_2023,
    temp_column_2023,
    rh_column_2023,
    fallback_temp_2023
)

    # ----------------------------------------
# SAVE PROCESSED FILES
# ----------------------------------------

    hi_2018.to_csv(
    f"outputs/processed_{location}_2018.csv",
    index=False
)

    hi_2023.to_csv(
    f"outputs/processed_{location}_2023.csv",
    index=False
)

    print("\n========== RAW WEATHER DATA ==========\n")

    print(
    climate_2018[
        [temp_column_2018, rh_column_2018]
    ].head(20)
)

    print(
    climate_2023[
        [temp_column_2023, rh_column_2023]
    ].head(20)
)

    print("\n======================================\n")
    print("\n========== HI DEBUG ==========\n")
    

    print("HI 2018 rows:")
    print(len(hi_2018))

    print("\nHI 2023 rows:")
    print(len(hi_2023))

    print("\nHI 2018 sample:")
    print(
    hi_2018[
        [temp_column_2018, rh_column_2018, "HI"]
    ].head()
)

    print("\nHI 2023 sample:")
    print(
    hi_2023[
        [temp_column_2023, rh_column_2023, "HI"]
    ].head()
)

    print("\nHI 2018 stats:")
    print(
    hi_2018["HI"].describe()
)

    print("\nHI 2023 stats:")
    print(
    hi_2023["HI"].describe()
)

    print("\n==============================\n")
    # ----------------------------------------
    # PM2.5 HISTOGRAMS
    # ----------------------------------------

    pm25_plot = generate_pm25_histograms(

    df_2018=pm_2018,

    df_2023=pm_2023,

    date_column=date_column_2018,

    pm_column=pm_column_2018,

    location=location
)

    # ----------------------------------------
    # HI HISTOGRAMS
    # ----------------------------------------

    hi_plot = hi_plot = generate_hi_histograms(

    df_2018=hi_2018,

    df_2023=hi_2023,

    date_column=date_column_2018,

    location=location
)

    # ----------------------------------------
    # DOUBLE DIURNAL CURVES
    # ----------------------------------------

    # Rename PM columns for diurnal curves

    pm_2018.rename(
    columns={
        pm_column_2018: "PM2.5"
    },
    inplace=True
)

    pm_2023.rename(
    columns={
        pm_column_2023: "PM2.5"
    },
    inplace=True
)

    
    diurnal_plot = (
    generate_double_diurnal_curves(

        hi_2018=hi_2018,

        hi_2023=hi_2023,

        pm_2018=pm_2018,

        pm_2023=pm_2023,

        date_column=date_column_2018,

        pm_column="PM2.5",

        location=location
    )
)


    # ----------------------------------------
    # PREPARE CORRELATION DATA
    # ----------------------------------------

    corr_2018 = pm_2018.merge(

        hi_2018[
            [date_column_2018, "HI"]
        ],

        on=date_column_2018
    )

    corr_2023 = pm_2023.merge(

        hi_2023[
            [date_column_2023, "HI"]
        ],

        on=date_column_2023
    )

    # Rename PM columns
    corr_2018.rename(
        columns={
            pm_column_2018: "PM2.5"
        },
        inplace=True
    )

    corr_2023.rename(
        columns={
            pm_column_2023: "PM2.5"
        },
        inplace=True
    )

    # Rename date columns
    corr_2018.rename(
        columns={
            date_column_2018: "From Date"
        },
        inplace=True
    )

    corr_2023.rename(
        columns={
            date_column_2023: "From Date"
        },
        inplace=True
    )

    # ----------------------------------------
    # CORRELATION ANALYSIS
    # ----------------------------------------

    correlation_plot = (
        generate_correlation_analysis(
            corr_2018,
            corr_2023,
            location
        )
    )

    # ----------------------------------------
    # RETURN RESULTS
    # ----------------------------------------

    return {

        "pm25_histograms": pm25_plot,

        "hi_histograms": hi_plot,

        "double_diurnal_curves": diurnal_plot,

        "correlation_analysis": correlation_plot
    }