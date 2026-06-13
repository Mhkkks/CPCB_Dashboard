import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime

from app.config import (
    PLOTS_DIR,
    EXCEL_DIR
)


# ---------------------------------------------------
# TIME INTERVALS
# ---------------------------------------------------

morning_start = datetime.strptime(
    "06:00",
    "%H:%M"
).time()

afternoon_start = datetime.strptime(
    "12:00",
    "%H:%M"
).time()

night_start = datetime.strptime(
    "18:00",
    "%H:%M"
).time()

midnight_start = datetime.strptime(
    "00:00",
    "%H:%M"
).time()


# ---------------------------------------------------
# FILTER TIME INTERVALS
# ---------------------------------------------------

def filter_time_intervals(
    df,
    date_column
):

    import pandas as pd

    from datetime import time

    # =========================
    # ENSURE DATETIME
    # =========================

    df = df.copy()

    df[date_column] = pd.to_datetime(

        df[date_column],

        errors='coerce'
    )

    df = df.dropna(
        subset=[date_column]
    )

    # =========================
    # TIME INTERVALS
    # =========================

    morning_start = time(6, 0)
    morning_end = time(12, 0)

    afternoon_start = time(12, 0)
    afternoon_end = time(18, 0)

    night_start = time(18, 0)
    night_end = time(23, 59)

    midnight_start = time(0, 0)
    midnight_end = time(6, 0)

    morning_data = df[
        (
            df[date_column].dt.time >= morning_start
        )
        &
        (
            df[date_column].dt.time < morning_end
        )
    ]

    afternoon_data = df[
        (
            df[date_column].dt.time >= afternoon_start
        )
        &
        (
            df[date_column].dt.time < afternoon_end
        )
    ]

    night_data = df[
        (
            df[date_column].dt.time >= night_start
        )
        &
        (
            df[date_column].dt.time <= night_end
        )
    ]

    midnight_data = df[
        (
            df[date_column].dt.time >= midnight_start
        )
        &
        (
            df[date_column].dt.time < midnight_end
        )
    ]

    return (
        morning_data,
        afternoon_data,
        night_data,
        midnight_data
    )


# ---------------------------------------------------
# PLOT DOUBLE HISTOGRAM
# ---------------------------------------------------

def plot_double_histogram(

    data1,
    data2,

    column_name,

    label1,
    label2,

    subplot_title,

    xlim

):

    data1_filtered = (
        data1[column_name]
        .dropna()
    )

    data1_filtered = data1_filtered[
        (data1_filtered > 0)
        &
        (data1_filtered <= 700)
    ]

    data2_filtered = (
        data2[column_name]
        .dropna()
    )

    data2_filtered = data2_filtered[
        (data2_filtered > 0)
        &
        (data2_filtered <= 700)
    ]

    bins = np.linspace(
        xlim[0],
        xlim[1],
        20
    )

    plt.hist(
        data1_filtered,
        bins=bins,
        alpha=0.5,
        label=label1,
        edgecolor='black'
    )

    plt.hist(
        data2_filtered,
        bins=bins,
        alpha=0.5,
        label=label2,
        edgecolor='black'
    )

    plt.title(
        subplot_title,
        fontsize=12
    )

    plt.xlabel(
        'PM2.5 [µg/m³]'
    )

    plt.ylabel(
        'Frequency'
    )

    plt.legend()

    plt.grid(
        True,
        linestyle='--',
        alpha=0.6
    )

    plt.xlim(xlim)


# ---------------------------------------------------
# GENERATE PM2.5 HISTOGRAMS
# ---------------------------------------------------

def generate_pm25_histograms(

    df_2018,
    df_2023,

    date_column,
    pm_column,

    location

):

    # ----------------------------------------
    # SPLIT INTERVALS
    # ----------------------------------------

    morning_data_2018, \
    afternoon_data_2018, \
    night_data_2018, \
    midnight_data_2018 = (

        filter_time_intervals(
            df_2018,
            date_column
        )
    )

    morning_data_2023, \
    afternoon_data_2023, \
    night_data_2023, \
    midnight_data_2023 = (

        filter_time_intervals(
            df_2023,
            date_column
        )
    )

    # ----------------------------------------
    # CREATE FIGURE
    # ----------------------------------------

    plt.figure(
        figsize=(14, 12)
    )

    plt.suptitle(

        f'Comparison of PM2.5 (2018 vs 2023)\n{location}',

        fontsize=18,
        fontweight='bold'
    )

    xlim = (0, 400)

    # ----------------------------------------
    # MORNING
    # ----------------------------------------

    plt.subplot(2, 2, 1)

    plot_double_histogram(

        morning_data_2018,
        morning_data_2023,

        pm_column,

        '2018',
        '2023',

        'Morning (6 AM to 12 PM)',

        xlim
    )

    # ----------------------------------------
    # AFTERNOON
    # ----------------------------------------

    plt.subplot(2, 2, 2)

    plot_double_histogram(

        afternoon_data_2018,
        afternoon_data_2023,

        pm_column,

        '2018',
        '2023',

        'Afternoon (12 PM to 6 PM)',

        xlim
    )

    # ----------------------------------------
    # NIGHT
    # ----------------------------------------

    plt.subplot(2, 2, 3)

    plot_double_histogram(

        night_data_2018,
        night_data_2023,

        pm_column,

        '2018',
        '2023',

        'Night (6 PM to Midnight)',

        xlim
    )

    # ----------------------------------------
    # MIDNIGHT
    # ----------------------------------------

    plt.subplot(2, 2, 4)

    plot_double_histogram(

        midnight_data_2018,
        midnight_data_2023,

        pm_column,

        '2018',
        '2023',

        'Midnight (Midnight to 6 AM)',

        xlim
    )

    plt.subplots_adjust(

        left=0.08,
        right=0.95,

        top=0.90,
        bottom=0.08,

        hspace=0.35,
        wspace=0.25
    )

    # ----------------------------------------
    # SAFE LOCATION NAME
    # ----------------------------------------

    safe_location = (

        location
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
        .replace(",", "")
    )

    # ----------------------------------------
    # SAVE PLOT
    # ----------------------------------------

    plot_path = (

        PLOTS_DIR /
        f"{safe_location}_pm25_histograms.png"
    )

    plt.savefig(

        plot_path,

        dpi=300,

        bbox_inches='tight'
    )

    plt.close()

    # ----------------------------------------
    # EXPORT HISTOGRAM DATA
    # ----------------------------------------

    bins = np.linspace(
        xlim[0],
        xlim[1],
        20
    )

    hist_data = {

        'Bins': bins[:-1]
    }

    intervals = {

        'Morning': (
            morning_data_2018,
            morning_data_2023
        ),

        'Afternoon': (
            afternoon_data_2018,
            afternoon_data_2023
        ),

        'Night': (
            night_data_2018,
            night_data_2023
        ),

        'Midnight': (
            midnight_data_2018,
            midnight_data_2023
        )
    }

    for interval_name, (
        data_2018,
        data_2023
    ) in intervals.items():

        hist_2018, _ = np.histogram(

            data_2018[pm_column]
            .dropna(),

            bins=bins
        )

        hist_2023, _ = np.histogram(

            data_2023[pm_column]
            .dropna(),

            bins=bins
        )

        hist_data[
            f'{interval_name}_2018'
        ] = hist_2018

        hist_data[
            f'{interval_name}_2023'
        ] = hist_2023

    hist_df = pd.DataFrame(
        hist_data
    )

    excel_path = (

        EXCEL_DIR /
        f"{safe_location}_pm25_histogram_data.xlsx"
    )

    hist_df.to_excel(

        excel_path,

        index=False
    )

    # ----------------------------------------
    # RETURN PATHS
    # ----------------------------------------

    return {

    "plot_url":

    f"/outputs/plots/{plot_path.name}",

    "excel_url":

    f"/outputs/excel/{excel_path.name}"
}