import pandas as pd
import os


# create a funtion to read a csv file and return a pandas dataframe
def read_csv_file(file_path: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The DataFrame containing the data from the CSV file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    df = pd.read_csv(file_path)

    return df
