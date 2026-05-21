def celsius_to_fahrenheit(celsius):

    return celsius * 9/5 + 32


def compute_heat_index(
    temperature_celsius,
    RH
):

    if temperature_celsius is None or RH is None:

        return None

    temperature = celsius_to_fahrenheit(
        temperature_celsius
    )

    if temperature < 80:

        return temperature

    if RH <= 0 or RH > 100:

        return None

    heat_index = (

        -42.379

        + 2.04901523 * temperature

        + 10.14333127 * RH

        - 0.22475541 * temperature * RH

        - 6.83783e-3 * temperature**2

        - 5.481717e-2 * RH**2

        + 1.22874e-3 * temperature**2 * RH

        + 8.5282e-4 * temperature * RH**2

        - 1.99e-6 * temperature**2 * RH**2
    )

    return round(heat_index, 2)