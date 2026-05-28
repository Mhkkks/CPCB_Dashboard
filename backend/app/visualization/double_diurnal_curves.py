import matplotlib.pyplot as plt

from app.config import PLOTS_DIR


def load_and_process_csv(
    df,
    date_column,
    value_column
):

    import pandas as pd

    # =========================
    # SAFE COPY
    # =========================

    df = df.copy()

    # =========================
    # FORCE DATETIME
    # =========================

    df[date_column] = pd.to_datetime(

        df[date_column],

        errors='coerce'
    )

    # =========================
    # FORCE NUMERIC
    # =========================

    df[value_column] = pd.to_numeric(

        df[value_column],

        errors='coerce'
    )

    # =========================
    # REMOVE BAD ROWS
    # =========================

    df = df.dropna(

        subset=[
            date_column,
            value_column
        ]
    )

    # =========================
    # EXTRACT HOUR
    # =========================

    df['Hour'] = (

        df[date_column]
        .dt.hour
    )

    # =========================
    # GROUP BY HOUR
    # =========================

    hourly_mean = (

        df[
            df[value_column] != 0
        ]

        .groupby('Hour')[value_column]

        .agg(['mean', 'std'])
    )

    return (
        hourly_mean
        .sort_index()
    )


def generate_double_diurnal_curves(
    hi_2018,
    hi_2023,
    pm_2018,
    pm_2023,
    date_column,
    pm_column,
    location
):

    hourly_mean_hi_2023 = (
        load_and_process_csv(
            hi_2023,
            date_column,
            'HI'
        )
    )

    hourly_mean_hi_2018 = (
        load_and_process_csv(
            hi_2018,
            date_column,
            'HI'
        )
    )

    hourly_mean_pm25_2023 = (
    load_and_process_csv(
        pm_2023,
        date_column,
        pm_column
    )
)

    hourly_mean_pm25_2018 = (
        load_and_process_csv(
            pm_2018,
            date_column,
            pm_column
        )
    )

    fig, ax1 = plt.subplots(
        figsize=(16, 10)
    )

    ax1.errorbar(
        hourly_mean_hi_2023.index,
        hourly_mean_hi_2023['mean'],
        yerr=hourly_mean_hi_2023['std'],
        fmt='-o',
        capsize=5,
        label='HI 2023'
    )

    ax1.errorbar(
        hourly_mean_hi_2018.index,
        hourly_mean_hi_2018['mean'],
        yerr=hourly_mean_hi_2018['std'],
        fmt='-s',
        capsize=5,
        label='HI 2018'
    )

    ax1.set_xlabel(
        'Hour of Day'
    )

    ax1.set_ylabel(
        'Heat Index (HI) in °F'
    )

    ax1.set_ylim(0, 150)

    ax1.grid(
        True,
        linestyle='--',
        alpha=0.7
    )

    ax2 = ax1.twinx()

    ax2.errorbar(
        hourly_mean_pm25_2023.index,
        hourly_mean_pm25_2023['mean'],
        yerr=hourly_mean_pm25_2023['std'],
        fmt='-^',
        capsize=5,
        label='PM2.5 2023'
    )

    ax2.errorbar(
        hourly_mean_pm25_2018.index,
        hourly_mean_pm25_2018['mean'],
        yerr=hourly_mean_pm25_2018['std'],
        fmt='-v',
        capsize=5,
        label='PM2.5 2018'
    )

    ax2.set_ylabel(
        'PM2.5 Concentration'
    )

    ax2.set_ylim(0, 300)

    lines, labels = (
        ax1.get_legend_handles_labels()
    )

    lines2, labels2 = (
        ax2.get_legend_handles_labels()
    )

    ax1.legend(
        lines + lines2,
        labels + labels2,
        loc='upper left'
    )

    plt.title(
        f'Heat Index and PM2.5 Levels at {location}'
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
        f"{safe_location}_double_diurnal.png"
    )

    plt.savefig(
        plot_path,
        dpi=300
    )

    plt.close()

    return (

    f"http://127.0.0.1:8000/outputs/plots/{plot_path.name}"
)