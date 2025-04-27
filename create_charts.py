from libs.io.csv import read_csv_file
from libs.constants.files import FOLDER_DATA_DEVICES_SMA, FOLDER_PNG_FILES
from pathlib import Path
from libs.charts.create_png import createPngBarChart
from libs.dates.date_conversion import convert_date

file = Path(FOLDER_DATA_DEVICES_SMA, "Zaehlerstand Bezugszaehler.csv")
data_sma_bezug = read_csv_file(file)
# reduce the data to the columns timestamp, diff
data_sma_bezug = data_sma_bezug[["timestamp", "diff"]]

file = Path(FOLDER_DATA_DEVICES_SMA, "Tagesertrag.csv")
data_sma_tagesertrag = read_csv_file(file)
# reduce the data to the columns timestamp, diff
data_sma_tagesertrag = data_sma_tagesertrag[["timestamp", "value"]]
# rename the columns
data_sma_tagesertrag = data_sma_tagesertrag.rename(
    columns={
        "value": "diff",
    }
)

file = Path(FOLDER_DATA_DEVICES_SMA, "Zaehlerstand Einspeisezaehler.csv")
data_sma_einspeisung = read_csv_file(file)
# reduce the data to the columns timestamp, diff
data_sma_einspeisung = data_sma_einspeisung[["timestamp", "diff"]]

# merge the dataframes data_sma_tagesertrag, data_sma_einspeisung and data_sma_bezug into a single dataframe with the same columns
data = data_sma_tagesertrag.merge(
    data_sma_einspeisung,
    how="outer",
    on="timestamp",
    suffixes=("_tagesertrag", "_einspeisung"),
).merge(
    data_sma_bezug,
    how="outer",
    on="timestamp",
    suffixes=("_einspeisung", "_bezug"),
)
# rename the columns
data = data.rename(
    columns={
        "diff_tagesertrag": "Tagesertrag",
        "diff_einspeisung": "Einspeisung",
        "diff": "Bezug",
    }
)


# convert the column timestamp to a datetime object
data["timestamp"] = data["timestamp"].apply(
    lambda x: convert_date(x, target_format="datetime")
)

png_file = Path(FOLDER_PNG_FILES, "sma.png")
createPngBarChart(
    data=data,
    header="SMA",
    filename=png_file,
    xValue="timestamp",
    yValue="Einspeisung",
    xLabel="Datum",
    yLabel="Wh",
    height=5,
    width=10,
    # show_table=False,
)

data = data
