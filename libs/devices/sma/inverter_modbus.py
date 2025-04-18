import dataclasses
from dotenv import dotenv_values
from libs.constants.files import FILE_CONFIG_SECRETS, FOLDER_DATA_DEVICES_SMA
from pymodbus.client import ModbusTcpClient
from libs.constants.sma_inverter import CHANNELS_METADATA, CHANNELS_TO_STORE
import datetime
import os
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
class SmaModbus:
    client: ModbusTcpClient = None
    values: list[Measurement] = dataclasses.field(default_factory=list)
    """
    Class to manage the SMA Modbus inverter.
    """

    def __init__(self):
        CONFIG = getEnvironmentVariables()
        host = None
        port = None

        if CONFIG is None:
            host = os.environ.get("SMA_INVERTER_IP")
            port = os.environ.get("SMA_INVERTER_PORT")
        else:
            host = CONFIG["SMA_INVERTER_IP"]
            port = CONFIG["SMA_INVERTER_PORT"]
        self.client = ModbusTcpClient(host=host, port=port)

    def connect(self):
        """
        Connect to the SMA inverter.
        """
        self.client.connect()

    def close(self):
        """
        Close the connection to the SMA inverter.
        """
        self.client.close()

    def getAllValues(self):
        """
        Get all the values from the SMA inverter.
        """
        # Read holding registers
        self.values = []
        for register in CHANNELS_METADATA:
            lengthRegister = int(register["modbus_address_length"])
            address = int(register["modbus_address"])
            if address in CHANNELS_TO_STORE:
                response = self.client.read_holding_registers(
                    address=address, count=lengthRegister, slave=3
                )
                if not response.isError():
                    # Convert register values (e.g. Float32)
                    raw_data = response.registers
                    value = (raw_data[0] << 16) + raw_data[1]
                    fullGroupName = register["group_full"]
                    # get the first string in the group name before the >
                    device = fullGroupName.split(">")[0]
                    thisMeasurement = buildMeasurement(
                        raw=register,
                        raw_value=value,
                        device=device,
                    )
                    self.values.append(thisMeasurement)

                else:
                    print("Error reading register")
        # sort the values by address
        self.values.sort(key=lambda x: x.address)

    # Save all the values from the SMA inverter to a file.
    # Create a CSV file for each address and store the current value with the timestamp.
    # If there is already a file, append the new value to the file.
    # If there is already a value in the file for a day overwrite it with the current value.
    # Use the pandas library to create the CSV file.
    def storeValuesInFiles(self):
        """
        Store the values in files.
        """
        # Create the folder if it does not exist
        Path(FOLDER_DATA_DEVICES_SMA).mkdir(parents=True, exist_ok=True)

        # print(f" - {len(self.values)} values read from the inverter")
        for measurement in self.values:
            thisAddress = int(measurement.address)
            if thisAddress in CHANNELS_TO_STORE:
                print(
                    f"Storing value for address {thisAddress} - {measurement.channel} {measurement.value} {measurement.unit}"
                )
                # Create a filename based on the address and channel
                filename = f"{FOLDER_DATA_DEVICES_SMA}/{measurement.name}.csv"
                # Get the current date
                today = datetime.date.today()

                lines = readLinesFromCsvFile(filename)
                headerLine = buildHeaderForCsvFile()
                dataLine = buildLineForCsvFile(allLines=lines, measurement=measurement)

                # Check if the file exists
                if Path(filename).is_file():
                    # only append the value if the date is different

                    if len(lines) > 1:
                        last_line = lines[-1]
                        last_date = last_line.split(",")[0].split(" ")[0]
                        if last_date == str(today):
                            # If the date is the same, overwrite the value
                            lines[-1] = dataLine
                        else:
                            # If the date is different, add a new line
                            lines.append(dataLine)
                        with open(filename, "w") as f_write:
                            f_write.writelines(lines)
                else:
                    # If the file does not exist, create it and write the header
                    with open(filename, "w") as f:
                        f.write(headerLine)
                        f.write(dataLine)


def readLinesFromCsvFile(filename: str) -> list[str]:
    """
    Read a CSV file and return the values as a list of strings.
    """
    with open(filename, "r") as f:
        lines = f.readlines()
        return lines


def buildLineForCsvFile(measurement: Measurement, allLines: list[str] = None) -> str:
    """
    Build a line for the CSV file.
    """
    # Create a timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a line for the CSV file
    if allLines is None:
        return f"{timestamp},{measurement.address},{measurement.value},0,{measurement.unit}\n"
    else:
        # Get the last value from the line
        last_value = getValueFromPreviousDay(allLines)
        # Create a new line with the new value
        diff = measurement.value - float(last_value)
        line = f"{timestamp},{measurement.address},{measurement.value},{diff},{measurement.unit}\n"

    return line


def getValueFromPreviousDay(allLines: list[str]) -> float:
    """
    Get the value from the previous day.
    """
    # Get the last line of the file

    result = 0.0

    maxDate = None

    for line in allLines:
        # Get the last value from the line
        last_value = line.split(",")[2]
        # Get the date from the line
        date = line.split(",")[0].split(" ")[0]
        # If the date is different, return the value
        if date < str(datetime.date.today()):
            if maxDate is None:
                maxDate = date
                result = float(last_value)
            else:
                if date > maxDate:
                    maxDate = date
                    result = float(last_value)
    return result


def buildHeaderForCsvFile() -> str:
    """
    Build a header for the CSV file.
    """
    # Create a header for the CSV file
    header = "timestamp,address,value,diff,unit\n"
    return header


def buildMeasurement(raw: dict, raw_value: float, device: str) -> Measurement:
    """
    Build a measurement object.
    """
    step_size = raw.get("step_size")
    # replace "," with "." in step_size
    if step_size is not None:
        step_size = step_size.replace(",", ".")
    else:
        step_size = "1"

    if step_size == "-":
        step_size = "1"

    multiplier = float(step_size)
    unit = raw.get("unit")
    value = raw_value * multiplier
    # name = device + " - " + raw.get("name")
    name = raw.get("name")
    channel = raw.get("modbus_channel")
    address = raw.get("modbus_address")

    if raw.get("modbus_dataformat") == "TEMP":
        unit = "°C"
    return Measurement(
        address=address, channel=channel, name=name, unit=unit, value=value
    )


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
