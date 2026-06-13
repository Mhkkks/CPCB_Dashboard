import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from sklearn.linear_model import (
    LinearRegression
)
from app.config import (
    UPLOAD_DIR,
    OUTPUT_DIR,
    PLOTS_DIR,
    EXCEL_DIR
)

from app.visualization.pm25_histograms import (
    filter_time_intervals
)

def generate_correlation_analysis(
    data_2018,
    data_2023,
    location
):

    morning_data_2018, afternoon_data_2018, night_data_2018, midnight_data_2018 = (
        filter_time_intervals(
            data_2018,
            'From Date'
        )
    )

    morning_data_2023, afternoon_data_2023, night_data_2023, midnight_data_2023 = (
        filter_time_intervals(
            data_2023,
            'From Date'
        )
    )

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(15, 12)
    )

    axes = axes.flatten()

    intervals = [
        'Morning',
        'Afternoon',
        'Night',
        'Midnight'
    ]

    data_2018_intervals = [
        morning_data_2018,
        afternoon_data_2018,
        night_data_2018,
        midnight_data_2018
    ]

    data_2023_intervals = [
        morning_data_2023,
        afternoon_data_2023,
        night_data_2023,
        midnight_data_2023
    ]

    for i, interval in enumerate(intervals):

        ax = axes[i]

        loc_data_2018 = (
            data_2018_intervals[i]
            .copy()
        )

        loc_data_2023 = (
            data_2023_intervals[i]
            .copy()
        )

        loc_data_2018 = loc_data_2018.dropna(
            subset=['HI', 'PM2.5']
        )

        loc_data_2023 = loc_data_2023.dropna(
            subset=['HI', 'PM2.5']
        )

        if len(loc_data_2018) == 0 and len(loc_data_2023) == 0:

            ax.set_title(
                f'{location} - {interval} (No Data)'
            )

            continue

        # -------------------------
        # Scatter plots
        # -------------------------

        if not loc_data_2018.empty:

            sns.scatterplot(
                x='HI',
                y='PM2.5',
                data=loc_data_2018,
                ax=ax,
                s=10,
                color='blue',
                label='2018'
            )

        if not loc_data_2023.empty:

            sns.scatterplot(
                x='HI',
                y='PM2.5',
                data=loc_data_2023,
                ax=ax,
                s=10,
                color='red',
                label='2023'
            )

        # -------------------------
        # Regression 2018
        # -------------------------

        if len(loc_data_2018) > 1:

            x_2018 = (
                loc_data_2018['HI']
                .values
                .reshape(-1, 1)
            )

            y_2018 = (
                loc_data_2018['PM2.5']
                .values
            )

            reg_2018 = (
                LinearRegression()
                .fit(x_2018, y_2018)
            )

            x_range_2018 = np.linspace(
                x_2018.min(),
                x_2018.max(),
                100
            ).reshape(-1, 1)

            y_pred_2018 = (
                reg_2018.predict(
                    x_range_2018
                )
            )

            ax.plot(
                x_range_2018,
                y_pred_2018,
                color='blue'
            )

        # -------------------------
        # Regression 2023
        # -------------------------

        if len(loc_data_2023) > 1:

            x_2023 = (
                loc_data_2023['HI']
                .values
                .reshape(-1, 1)
            )

            y_2023 = (
                loc_data_2023['PM2.5']
                .values
            )

            reg_2023 = (
                LinearRegression()
                .fit(x_2023, y_2023)
            )

            x_range_2023 = np.linspace(
                x_2023.min(),
                x_2023.max(),
                100
            ).reshape(-1, 1)

            y_pred_2023 = (
                reg_2023.predict(
                    x_range_2023
                )
            )

            ax.plot(
                x_range_2023,
                y_pred_2023,
                color='red'
            )

        ax.set_title(
            f'{location} - {interval}'
        )

        ax.set_xlabel(
            'Heat Index (HI)'
        )

        ax.set_ylabel(
            'PM2.5'
        )

        ax.grid(
            True,
            linestyle='--',
            alpha=0.6
        )

    plt.tight_layout()

    safe_location = (
        location
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
    )

    plot_path = (
        PLOTS_DIR /
        f"{safe_location}_correlation.png"
    )

    plt.savefig(
        plot_path,
        dpi=300
    )

    plt.close()

    return (
        f"/outputs/plots/{plot_path.name}"
    )

