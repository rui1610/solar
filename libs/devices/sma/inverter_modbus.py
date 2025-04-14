import dataclasses
from dotenv import dotenv_values
from libs.constants.files import FILE_CONFIG_SECRETS
from pymodbus.client import ModbusTcpClient
from libs.constants.sma_inverter import CHANNELS_METADATA, CHANNELS_TO_USE


CONFIG = dotenv_values(FILE_CONFIG_SECRETS)


@dataclasses.dataclass
class Measurement:
    """
    Class to manage the measurement data.
    """

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

    def getValues(self):
        """
        Get the values from the SMA inverter.
        """
        # Read holding registers

        self.values = []

        for device in CHANNELS_TO_USE:
            for modbusRegister in device["channels"]:
                register = getModbusRegister(modbusRegister)
                if register is not None:
                    lengthRegister = int(register["modbus_address_length"])
                    response = self.client.read_holding_registers(
                        address=modbusRegister, count=lengthRegister, slave=3
                    )
                    if not response.isError():
                        # Convert register values (e.g. Float32)
                        raw_data = response.registers
                        value = (raw_data[0] << 16) + raw_data[1]
                        thisMeasurement = buildMeasurement(
                            raw=register,
                            raw_value=value,
                            device=device,
                        )
                        self.values.append(thisMeasurement)

                    else:
                        print("Error reading register")
                else:
                    print(f"Register {modbusRegister} not found in metadata")


def getModbusRegister(modbus_register: int) -> dict:
    for register in CHANNELS_METADATA:
        if register["modbus_address"] == str(modbus_register):
            return register
    return None


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

    multiplier = float(step_size)
    unit = raw.get("unit")
    value = raw_value * multiplier
    name = device.get("device_name") + " - " + raw.get("name")
    channel = raw.get("modbus_channel")

    return Measurement(channel=channel, name=name, unit=unit, value=value)
