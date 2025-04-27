import seaborn as sns

from libs.constants.charts import (
    COLOR_PALETTE,
    BARPLOT_HEIGHT,
    BARPLOT_WIDTH,
    TEXT_SIZE_BAR_LABELS,
    TEXT_SIZE_TITLE,
    TEXT_SIZE_Y_AXIS,
    TEXT_SIZE_X_AXIS,
    LABELS_COLOR,
)
from IPython.display import set_matplotlib_formats
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt


def createPngBarChart(
    data: list,
    header: str,
    filename: str,
    xValue: str = None,
    yValue: str = None,
    xLabel: str = None,
    yLabel: str = None,
    stacked: bool = False,
    height=BARPLOT_HEIGHT,
    width=BARPLOT_WIDTH,
):
    # merge the dataframes into a single dataframe with the same columns

    sns.set_palette(palette=COLOR_PALETTE)

    # determine the number of the dataframe colums in data
    num_columns = len(data.columns) - 1
    # reduce the COLOR_PALETTE to the number of columns in the data
    this_palette = COLOR_PALETTE[:num_columns]

    ax = data.plot(
        kind="bar",
        stacked=stacked,
        x=xValue,
        figsize=(width, height),
        color=this_palette,
    )

    # set the y-axis to start at 0 until the maximum
    y_max = calculate_ymax(yValue=yValue, data=data)
    divisor, unit = calculate_divisor_and_unit(y_max=y_max)

    sns.despine()
    # See https://blakeaw.github.io/2020-05-25-improve-matplotlib-notebook-inline-res/ for hints to increase resolution
    sns.set_theme(rc={"figure.dpi": 100, "savefig.dpi": 300})
    set_matplotlib_formats("retina")

    # add grid lines to the plot
    ax.grid(axis="y", linewidth=0.5, linestyle=":", color="black", alpha=0.5)

    # set the title of the plot
    ax.set_title(
        header,
        loc="center",
        wrap=True,
        fontsize=TEXT_SIZE_TITLE,
        pad=15,
        color="black",
        alpha=0.5,
        style="italic",
    )

    # get the figure and set the size and layout
    figure = ax.get_figure()

    # ----------------------------------------------
    # define x-axis
    # ----------------------------------------------
    # set the x-axis label
    ax.set_xlabel(xLabel)

    # set the labels for the x-axis to be rotated 90 degrees
    ax.tick_params(axis="x", labelrotation=45, labelsize=TEXT_SIZE_X_AXIS)
    ax.tick_params(axis="y", labelsize=TEXT_SIZE_Y_AXIS)

    for i in range(len(ax.containers)):
        ax.bar_label(
            ax.containers[i],
            label_type="center",
            color=LABELS_COLOR,
            size=TEXT_SIZE_BAR_LABELS,
            padding=1,
            rotation=90,
            # fmt=lambda x: f"{x / divisor:.0f}{unit}",
        )
        i += 1
    # convert the x-axis labels to be in the format of YYYY-MM-DD
    # ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %m %Y"))

    # ----------------------------------------------
    # define y-axis
    # ----------------------------------------------
    # set the y-axis label
    ax.set_ylabel(yLabel, fontsize=TEXT_SIZE_Y_AXIS)

    ax.set_ylim(0, y_max)

    # format the y-axis to use engineering notation (e.g. 1e6 or 4 k)
    ax.yaxis.set_major_formatter(ticker.EngFormatter())

    # add the value of each bar in the center of the bar
    # i = 0

    plt.title(header, fontsize=TEXT_SIZE_TITLE)
    figure.savefig(filename)
    figure.clear()
    figure.clf()
    ax.clear()

    sns.reset_orig()


# Create a PNG file with a bar plot
def createPieChart(
    data,
    header,
    filename,
    xValue,
    yValue,
    xLabel: str = None,
    yLabel: str = None,
    height=BARPLOT_HEIGHT,
    width=BARPLOT_WIDTH,
):
    sns.set_palette(palette=COLOR_PALETTE)

    # determine the number of the colums in data
    num_columns = len(data.columns)

    # reduce the COLOR_PALETTE to the number of columns in the data
    this_palette = COLOR_PALETTE[:num_columns]

    ax = data.plot(
        kind="pie",
        y=yValue,
        figsize=(width / 2, height),
        color=this_palette,
        legend=False,
        autopct="%.0f%%",
    )

    # set the title of the plot
    ax.set_title(
        header,
        loc="center",
        wrap=True,
        fontsize=TEXT_SIZE_TITLE,
        pad=15,
        color="black",
        alpha=0.5,
        style="italic",
    )

    # get the figure and set the size and layout
    figure = ax.get_figure()

    sns.despine()
    sns.set_theme(rc={"figure.dpi": 100, "savefig.dpi": 300})
    set_matplotlib_formats("retina")

    # plt.title(header, fontsize=TEXT_SIZE_TITLE)
    plt.ylabel("")
    figure.savefig(filename)
    figure.clear()
    figure.clf()
    ax.clear()

    sns.reset_orig()


def calculate_divisor_and_unit(y_max):
    divisor = 1
    unit = ""

    if y_max > 999:
        divisor = 1000
        unit = "k"

    if y_max > 999999:
        divisor = 1000000
        unit = "M"

    if y_max > 999999999:
        divisor = 1000000000
        unit = "B"

    return divisor, unit


def calculate_ymax(yValue, data):
    y_max = 0

    if yValue is None:
        # Loop through all columns in the data and find the maximum value
        for column in data.columns:
            if column != "date_retrieval":
                this_max = int(data[column].max())
                y_max = this_max + y_max
    else:
        y_max = data[yValue].max()

    y_max = y_max * 1.1

    return y_max
