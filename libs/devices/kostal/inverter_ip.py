import dataclasses
from dotenv import dotenv_values
from libs.constants.files import FILE_CONFIG_SECRETS
from pathlib import Path


@dataclasses.dataclass
class Measurement:
    """
    Class to manage the measurement data.
    """

    address: int
    channel: int
    name: str
    unit: str
    value: float = None


@dataclasses.dataclass
class KostalInverter:
    client: ModbusTcpClient = None
    values: list[Measurement] = dataclasses.field(default_factory=list)
    """
    Class to manage the SMA Modbus inverter.
    """

    def __init__(self):
        CONFIG = getEnvironmentVariables()


def getEnvironmentVariables():
    """
    Get the environment variables from the .env file.
    """
    # Load the environment variables from the .env file

    # Check if the file exists
    if not Path(FILE_CONFIG_SECRETS).is_file():
        print(f"File {FILE_CONFIG_SECRETS} does not exist")
        return None

    env = dotenv_values(FILE_CONFIG_SECRETS)
    return env
