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


# =====================================================
# COMPUTE HEAT INDEX
# =====================================================

def compute_hi_column(
    df,
    temp_column,
    rh_column
):

    df = df.copy()

    # -------------------------------
    # CLEAN TEMPERATURE
    # -------------------------------

    df["Temperature"] = pd.to_numeric(
        df[temp_column],
        errors="coerce"
    )

    # -------------------------------
    # CLEAN RH
    # -------------------------------
    print("\n========== RAW RH VALUES ==========\n")

    print(
    df[rh_column]
    .head(30)
)

    print("\n===================================\n")
    df["RH"] = pd.to_numeric(
        df[rh_column],
        errors="coerce"
    )

    print("\n========== CLEAN RH VALUES ==========\n")

    print(
    df["RH"]
    .head(30)
)

    print("\n=====================================\n")

    # -------------------------------
    # COMPUTE HI
    # -------------------------------

    hi_values = []

    for _, row in df.iterrows():

        temp = row["Temperature"]

        rh = row["RH"]

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
        errors="coerce"
    )

    return df


# =====================================================
# MAIN ANALYSIS
# =====================================================

def run_full_analysis(

    pm_2018_path,
    pm_2023_path,

    climate_2018_path,
    climate_2023_path,

    location="Research_Location"

):

    # =================================================
    # LOAD FILES
    # =================================================

    pm_2018 = load_csv(pm_2018_path)

    pm_2023 = load_csv(pm_2023_path)

    climate_2018 = load_csv(climate_2018_path)

    climate_2023 = load_csv(climate_2023_path)

    # =================================================
    # DETECT COLUMNS
    # =================================================

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

    # =================================================
    # PM COLUMNS
    # =================================================

    pm_date_2018 = detected_pm_2018["date"]

    pm_date_2023 = detected_pm_2023["date"]

    pm_column_2018 = detected_pm_2018["pm25"]

    pm_column_2023 = detected_pm_2023["pm25"]

    # =================================================
    # CLIMATE COLUMNS
    # =================================================

    climate_date_2018 = (
        detected_climate_2018["date"]
    )

    climate_date_2023 = (
        detected_climate_2023["date"]
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

    # =================================================
    # DEBUG DETECTED COLUMNS
    # =================================================

    print("\n========== DETECTED COLUMNS ==========\n")

    print("PM 2018:", detected_pm_2018)

    print("PM 2023:", detected_pm_2023)

    print("Climate 2018:", detected_climate_2018)

    print("Climate 2023:", detected_climate_2023)

    print("\n======================================\n")

    # =================================================
    # VALIDATION
    # =================================================

    required_columns = [

        pm_date_2018,
        pm_date_2023,

        pm_column_2018,
        pm_column_2023,

        climate_date_2018,
        climate_date_2023,

        temp_column_2018,
        temp_column_2023,

        rh_column_2018,
        rh_column_2023
    ]

    if any(col is None for col in required_columns):

        raise ValueError(
            "Required CPCB columns not detected"
        )

    # =================================================
    # PREPROCESS PM
    # =================================================

    pm_2018 = preprocess_dataframe(
        pm_2018,
        pm_date_2018,
        pm_column_2018
    )

    pm_2023 = preprocess_dataframe(
        pm_2023,
        pm_date_2023,
        pm_column_2023
    )

    # =================================================
    # PREPROCESS CLIMATE
    # =================================================

    climate_2018 = preprocess_dataframe(
        climate_2018,
        climate_date_2018,
        temp_column_2018
    )

    climate_2023 = preprocess_dataframe(
        climate_2023,
        climate_date_2023,
        temp_column_2023
    )

    # =================================================
    # STANDARDIZE DATE COLUMNS
    # =================================================

    pm_2018.rename(
        columns={
            pm_date_2018: "From Date"
        },
        inplace=True
    )

    pm_2023.rename(
        columns={
            pm_date_2023: "From Date"
        },
        inplace=True
    )

    climate_2018.rename(
        columns={
            climate_date_2018: "From Date"
        },
        inplace=True
    )

    climate_2023.rename(
        columns={
            climate_date_2023: "From Date"
        },
        inplace=True
    )

    # =================================================
    # COMPUTE HI
    # =================================================

    hi_2018 = compute_hi_column(
        climate_2018,
        temp_column_2018,
        rh_column_2018
    )

    hi_2023 = compute_hi_column(
        climate_2023,
        temp_column_2023,
        rh_column_2023
    )

    # =================================================
    # DEBUG WEATHER DATA
    # =================================================

    print("\n========== WEATHER DEBUG ==========\n")

    print(
        hi_2018[
            [
                "From Date",
                "Temperature",
                "RH",
                "HI"
            ]
        ].head(20)
    )

    print(
        hi_2023[
            [
                "From Date",
                "Temperature",
                "RH",
                "HI"
            ]
        ].head(20)
    )

    print("\n===================================\n")

    # =================================================
    # SAVE PROCESSED FILES
    # =================================================

    hi_2018.to_csv(
        f"outputs/processed_{location}_2018.csv",
        index=False
    )

    hi_2023.to_csv(
        f"outputs/processed_{location}_2023.csv",
        index=False
    )

    # =================================================
    # STANDARDIZE PM COLUMN
    # =================================================

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

    # =================================================
    # PM HISTOGRAMS
    # =================================================

    pm25_plot = generate_pm25_histograms(

        df_2018=pm_2018,

        df_2023=pm_2023,

        date_column="From Date",

        pm_column="PM2.5",

        location=location
    )

    # =================================================
    # HI HISTOGRAMS
    # =================================================

    hi_plot = generate_hi_histograms(

        df_2018=hi_2018,

        df_2023=hi_2023,

        date_column="From Date",

        location=location
    )

    # =================================================
    # DOUBLE DIURNAL
    # =================================================

    diurnal_plot = generate_double_diurnal_curves(

        hi_2018=hi_2018,

        hi_2023=hi_2023,

        pm_2018=pm_2018,

        pm_2023=pm_2023,

        date_column="From Date",

        pm_column="PM2.5",

        location=location
    )
    # ==========================================
# FORCE DATETIME BEFORE MERGE
# ==========================================

    pm_2018["From Date"] = pd.to_datetime(

    pm_2018["From Date"],

    errors="coerce"
)

    pm_2023["From Date"] = pd.to_datetime(

    pm_2023["From Date"],

    errors="coerce"
)

    hi_2018["From Date"] = pd.to_datetime(

    hi_2018["From Date"],

    errors="coerce"
)

    hi_2023["From Date"] = pd.to_datetime(

    hi_2023["From Date"],

    errors="coerce"
)

# ==========================================
# DEBUG TYPES
# ==========================================

    print("\n========== MERGE DTYPES ==========\n")

    print(
    pm_2018["From Date"].dtype
)

    print(
    hi_2018["From Date"].dtype
)

    print(
    pm_2023["From Date"].dtype
)

    print(
    hi_2023["From Date"].dtype
)

    print("\n==================================\n")

    # =================================================
    # CORRELATION DATA
    # =================================================

    corr_2018 = pm_2018.merge(

    hi_2018[
        [
            "From Date",
            "HI"
        ]
    ],

    on="From Date",

    how="inner"
)

    corr_2023 = pm_2023.merge(

    hi_2023[
        [
            "From Date",
            "HI"
        ]
    ],

    on="From Date",

    how="inner"
)

    # =================================================
    # CORRELATION PLOT
    # =================================================

    correlation_plot = (
        generate_correlation_analysis(
            corr_2018,
            corr_2023,
            location
        )
    )

    # =================================================
    # RETURN
    # =================================================

    return {

        "pm25_histograms": pm25_plot,

        "hi_histograms": hi_plot,

        "double_diurnal_curves": diurnal_plot,

        "correlation_analysis": correlation_plot
    }