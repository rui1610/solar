from libs.io.csv import read_csv_file
from libs.constants.files import FOLDER_DATA_DEVICES_SMA, FOLDER_PNG_FILES
from pathlib import Path
from libs.charts.create_png import createPngBarChart
from libs.dates.date_conversion import convert_date


def fetch_data(file, xValue, yValue):
    # file = Path(FOLDER_DATA_DEVICES_SMA, "Zaehlerstand Bezugszaehler.csv")
    data = read_csv_file(file)
    # reduce the data to the columns timestamp, diff
    data = data[[xValue, yValue]]

    if xValue == "timestamp":
        # convert the column timestamp to a datetime object
        data["timestamp"] = data["timestamp"].apply(
            lambda x: convert_date(x, target_format="datetime")
        )
    return data


def create_png_file(file, x_label, y_label, x_value, y_value):
    data = fetch_data(file, x_value, y_value)

    # Create the folder if it does not exist
    Path(FOLDER_PNG_FILES).mkdir(parents=True, exist_ok=True)

    # Create the PNG file
    png_file = Path(FOLDER_PNG_FILES, f"{file.stem}.png")
    createPngBarChart(
        data=data,
        header=file.stem,
        filename=png_file,
        xValue=x_value,
        yValue=y_value,
        xLabel=x_label,
        yLabel=y_label,
        height=5,
        width=10,
        # show_table=False,
    )


create_png_file(
    file=Path(FOLDER_DATA_DEVICES_SMA, "Zaehlerstand Bezugszaehler.csv"),
    x_label="Datum",
    y_label="Wh",
    x_value="timestamp",
    y_value="diff",
)

create_png_file(
    file=Path(FOLDER_DATA_DEVICES_SMA, "Tagesertrag.csv"),
    x_label="Datum",
    y_label="Wh",
    x_value="timestamp",
    y_value="value",
)

create_png_file(
    file=Path(FOLDER_DATA_DEVICES_SMA, "Zaehlerstand Einspeisezaehler.csv"),
    x_label="Datum",
    y_label="Wh",
    x_value="timestamp",
    y_value="diff",
)
