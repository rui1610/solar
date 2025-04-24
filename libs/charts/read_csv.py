# This script reads the CSV files and prepares the data for the charts

import pandas as pd
from pathlib import Path

from libs.constants.files import (
    FILE_CSV_TF_BTP_DOWNLOADS,
    FILE_CSV_TF_CF_DOWNLOADS,
    FILE_CSV_CF_CF_DOWNLOADS,
)


# # Read the CSV file and prepare the data for the charts
# def prepare_tf_btp_stats_info(filename: Path):
#     # Read the CSV file into a DataFrame: df
#     df = pd.read_csv(filename)

#     # convert the date_retrieval column to a datetime object
#     df["date_retrieval"] = pd.to_datetime(df["date_retrieval"])

#     # filter the data to only include the newest entry and group it by date_retrieval on a monthly basis based on the date format YYYY-MM-TT HH:MM:SS
#     df["date_retrieval"] = pd.to_datetime(df["date_retrieval"])
#     df = df.groupby(pd.Grouper(key="date_retrieval", freq="ME")).last().reset_index()

#     # rename the df column for the date to only contain the year and month in the format MMM YY
#     df["date_retrieval"] = df["date_retrieval"].dt.strftime("%b %y")

#     return df


def prepare_downloads_numbers(filename, column_name, legend_name):
    df = pd.read_csv(filename)

    # get only the date_retrieval and all_time columns
    df = df[["date_retrieval", column_name]]

    # convert the date_retrieval column to a datetime object
    df["date_retrieval"] = pd.to_datetime(df["date_retrieval"])

    # filter the data to only include the newest entry and group it by date_retrieval on a monthly basis based on the date format YYYY-MM-TT HH:MM:SS
    df["date_retrieval"] = pd.to_datetime(df["date_retrieval"])
    df = df.groupby(pd.Grouper(key="date_retrieval", freq="ME")).last().reset_index()

    # copy the date_retrieval column to a new column date_retrieval_copy
    # df["date_retrieval_string"] = df["date_retrieval"]

    df = df.rename(columns={column_name: legend_name})

    return df


# -----------------------------------------------------------------------------------------------------------
# Read the collected data for the TF downloads and prepare the data for the charts
# -----------------------------------------------------------------------------------------------------------
def prepare_tf_download_numbers(time_selection: str = "all_time"):
    df_btp = prepare_downloads_numbers(
        FILE_CSV_TF_BTP_DOWNLOADS, time_selection, "SAP BTP"
    )
    df_cf = prepare_downloads_numbers(
        FILE_CSV_TF_CF_DOWNLOADS, time_selection, "Cloudfoundry (SAP)"
    )

    df_cf_cf = prepare_downloads_numbers(
        FILE_CSV_CF_CF_DOWNLOADS, time_selection, "Cloudfoundry (CF)"
    )

    # merge the two dataframes on the date_retrieval column
    #df_btp_cf = pd.merge(df_btp, df_cf, on="date_retrieval", how="outer")

    df = pd.merge(df_btp, df_cf_cf, on="date_retrieval", how="outer")

    # sort by the date_retrieval column
    df = df.sort_values(by=["date_retrieval"])

    # rename the df column for the date to only contain the year and month in the format MMM YY
    df["date_retrieval"] = df["date_retrieval"].dt.strftime("%b %y")

    return df


def prepare_tf_download_numbers_versions(
    filename_csv, time_selection: str = "this_year", combine_rc_beta: bool = True
):
    df = pd.read_csv(filename_csv)

    # remove all columns except for the this_yead and version columns
    df = df[[time_selection, "version"]]

    # order the df by the version column
    df = df.sort_values(by=time_selection)

    # set the version column as the index
    df = df.set_index("version")

    if combine_rc_beta:
        # sum the values of all rows that contain the string rc or beta in the index
        df.loc["temp"] = (
            df[df.index.str.contains("rc")].sum()
            + df[df.index.str.contains("beta")].sum()
        )

        # remove all rows from the df that contain the string rc or beta in the index
        df = df[~df.index.str.contains("rc")]
        df = df[~df.index.str.contains("beta")]

        # rename the row Temp to "Beta and RC"
        df = df.rename(index={"temp": "Beta & RC"})

    return df


# Read the CSV file and prepare the data for the charts
def prepare_tf_btp_version_info(filename: Path):
    # Read the CSV file into a DataFrame: df
    df = pd.read_csv(filename)

    # order the df by the version column
    df = df.sort_values(by=["version"])

    return df


def get_all_tf_btp_versions(filename):
    # Read the CSV file into a DataFrame: df
    df = pd.read_csv(filename)

    # get all columns from df
    columns = df.columns

    # remove column date_retrieval from the columns
    columns = columns.drop("date_retrieval")

    # remove all columns from columns that start with rc
    # columns = columns[~columns.str.startswith("rc")]

    return columns


# Read the CSV file and prepare the data for the charts
def prepare_tf_btp_stats_sum_info_monthly(filename, version):
    # Read the CSV file into a DataFrame: df
    df = pd.read_csv(filename)

    # convert the date_retrieval column to a datetime object
    df["date_retrieval"] = pd.to_datetime(df["date_retrieval"])

    # filter the data to only include the newest entry and group it by date_retrieval on a monthly basis based on the date format YYYY-MM-TT HH:MM:SS
    df["date_retrieval"] = pd.to_datetime(df["date_retrieval"])
    df = df.groupby(pd.Grouper(key="date_retrieval", freq="ME")).sum().reset_index()

    # rename the df column for the date to only contain the year and month in the format MMM YY
    df["date_retrieval"] = df["date_retrieval"].dt.strftime("%b %d %y")

    if version is not None:
        # rename the df column for the version to the column name value
        df = df.rename(columns={version: "value"})

        # remove all colums from df except for date_retrieval and value
        df = df[["date_retrieval", "value"]]

    return df


# Read the CSV file and prepare the data for the charts
def prepare_tf_btp_stats_sum_info_weekly(filename):
    # Read the CSV file into a DataFrame: df
    df = pd.read_csv(filename)

    # convert the date_retrieval column to a datetime object
    df["date_retrieval"] = pd.to_datetime(df["date_retrieval"])

    # filter the data to only include the newest entry and group it by date_retrieval on a monthly basis based on the date format YYYY-MM-TT HH:MM:SS
    df["date_retrieval"] = pd.to_datetime(df["date_retrieval"])
    df = df.groupby(pd.Grouper(key="date_retrieval", freq="W")).sum().reset_index()

    # rename the df column for the date to only contain the year and month in the format MMM YY
    df["date_retrieval"] = df["date_retrieval"].dt.strftime("%b %d %y")

    return df


# def prepare_stats_info(filename: Path, freq: str, agg_func: str):
#     # Read the CSV file into a DataFrame: df
#     df = pd.read_csv(filename)

#     # convert the date_retrieval column to a datetime object
#     df["date_retrieval"] = pd.to_datetime(df["date_retrieval"])

#     # filter the data to only include the newest entry and group it by date_retrieval on a monthly basis based on the date format YYYY-MM-TT HH:MM:SS
#     df = df.groupby(pd.Grouper(key="date_retrieval", freq=freq))

#     if agg_func == 'last':
#         df = df.last().reset_index()
#     elif agg_func == 'sum':
#         df = df.sum().reset_index()

#     # rename the df column for the date to only contain the year and month in the format MMM YY
#     df["date_retrieval"] = df["date_retrieval"].dt.strftime("%b %y")

#     return df

# BTP TF Exporter Downloads
def prepare_bt_tf_overall_downloads_numbers(filename):
    df = pd.read_csv(filename)

    # get only the date_retrieval and all_time columns

    # filter the data to only include the newest entry and group it by date_retrieval on a monthly basis based on the date format YYYY-MM-TT HH:MM:SS
    df["date_retrieval"] = pd.to_datetime(df["date_retrieval"])
    df['date_retrieval'] = df['date_retrieval'].dt.to_period('M')
    df = df.sort_values(by='date_retrieval').drop_duplicates(subset=['date_retrieval', 'binary'], keep='last')
    df = df.groupby(["date_retrieval"])["download_count"].sum().reset_index()
    return df


# BTP TF Exporter Downloads
def prepare_bt_tf_versionwise_downloads_numbers(filename):
    df = pd.read_csv(filename)
    df["date_retrieval"] = pd.to_datetime(df["date_retrieval"])
    df = df.sort_values(by='date_retrieval').drop_duplicates(subset=['date_retrieval', 'binary'], keep='last')
    df = df[["release", "download_count"]]
    df = df.groupby(["release"])["download_count"].sum().reset_index().set_index("release")
    return df