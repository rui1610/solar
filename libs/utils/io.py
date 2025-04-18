import pandas as pd


def read_csv_file(file_path: str) -> pd.DataFrame:
    """
    Read a CSV file and return its content as a pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        print(f"File {file_path} is empty.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return pd.DataFrame()


def write_csv_file(file_path: str, data: pd.DataFrame) -> None:
    """
    Write a pandas DataFrame to a CSV file.
    """
    try:
        data.to_csv(file_path, index=False)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")


def append_to_csv_file(file_path: str, data: pd.DataFrame) -> None:
    """
    Append a pandas DataFrame to a CSV file.
    """
    try:
        data.to_csv(file_path, mode="a", header=False, index=False)
    except Exception as e:
        print(f"An error occurred while appending to the file: {e}")
